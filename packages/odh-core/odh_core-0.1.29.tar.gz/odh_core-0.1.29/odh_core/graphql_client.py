import asyncio
import logging

import backoff
from gql import Client as gql_client
from gql import gql
from gql.transport.aiohttp import AIOHTTPTransport
from graphql import DocumentNode

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


# # Tracelog for aiohttp
# # from: https://stackoverflow.com/a/64954315
# async def on_request_end(session, context, params):
#     trace_log = logging.getLogger("aiohttp.client")
#     trace_log.debug(
#         f"Request: {params.method} {params.url} "
#         f"Response: status:{params.response.status} {await params.response.text()}"
#     )

# trace_config = aiohttp.TraceConfig()
# trace_config.on_request_end.append(on_request_end)

# session = (
#     aiohttp.ClientSession(
#         base_url="https://graph.microsoft.com/",
#         headers=settings.jsonheaders,
#         trust_env=True,
#         # log all requests made by the session
#         trace_configs=[trace_config],
#     ),
# )


class GraphQLClient:
    """GraphQL client with session management.

    .. todo::
        - Add support for trace logging

    """

    def __init__(
        self,
        url: str,
        headers: dict = None,
        ssl: bool = True,
        timeout: int = 10,
    ) -> None:
        """Initialize GraphQL client.

        Args:
        ----
            url (str): GraphQL server URL
            headers (dict, optional): HTTP headers to send with each request
            ssl (bool, optional): Verify SSL certificate
            timeout (int, optional): Timeout in seconds

        """
        self._client = gql_client(
            transport=AIOHTTPTransport(
                url=url,
                headers=headers,
                ssl=ssl,
                timeout=timeout,
            ),
            fetch_schema_from_transport=True,
        )
        self._session = None

    async def connect_async(self):
        retry_connect = backoff.on_exception(
            backoff.expo,  # wait generator (here: exponential backoff)
            Exception,  # which exceptions should cause a retry (here: everything)
            max_value=300,  # max wait time in seconds
        )
        self._session = await self._client.connect_async(
            reconnecting=True,
            retry_connect=retry_connect,
        )
        log.info(f"Connected to GraphQL server: {self._client.transport.url}")

    async def close_async(self):
        await self._client.close_async()
        log.info(f"Connection closed to GraphQL server: {self._client.transport.url}")

    async def execute_async(self, query: DocumentNode, variable_values: dict = None):
        """Execute a GraphQL query."""
        if not isinstance(query, DocumentNode):
            raise TypeError("query must be a gql object")

        if variable_values is None:
            result = await self._session.execute(query)
        else:
            result = await self._session.execute(query, variable_values)
        return result

    async def lock_acquire_async(
        self,
        lock_name: str,
        ttl_seconds: int = 30,
        await_release: bool = False,
    ):
        """Create a lock in the Hasura DB, lock will release after TTL expires
        or when release is called.
        """
        while True:
            query = gql(
                """
                mutation InsertLock($id: String = "", $ttl_seconds: Int = 30) {
                    insert_lock_table(objects: {id: $id, ttl_seconds: $ttl_seconds},
                    on_conflict: {constraint: lock_table_pkey}) {
                        affected_rows
                    }
                }
                """,
            )
            variables = {"id": lock_name, "ttl_seconds": ttl_seconds}
            lock = await self.execute_async(query, variable_values=variables)
            if lock["insert_lock_table"]["affected_rows"] == 1:
                return True
            elif await_release:
                query = gql(
                    """
                    query LockRelease($id: String = "") {
                        lock_table(where: {id: {_eq: $id}}) {
                            id
                            ttl_seconds
                        }
                    }
                    """,
                )
                variables = {"id": lock_name}
                lock = await self.execute_async(query, variable_values=variables)
                await asyncio.sleep(lock["lock_table"][0]["ttl_seconds"])
            else:
                return False

    async def lock_refresh_async(self, lock_name: str):
        """Create a lock in the Hasura DB, lock will release after TTL expires
        or when release is called.
        """
        query = gql(
            """
            mutation RefreshLock($id: String = "", $created_at: timestamptz = now) {
                update_lock_table_by_pk(pk_columns: {id: $id}, _set: {created_at: $created_at}) {
                    id
                }
            }
            """,
        )
        variables = {"id": lock_name}
        lock = await self.execute_async(query, variable_values=variables)
        return lock["update_lock_table_by_pk"]["id"] == lock_name

    async def lock_release_async(self, lock_name: str):
        """Release the lock in the Hasura DB."""
        query = gql(
            """
            mutation DeleteLock($id: String = "") {
                delete_lock_table(where: {id: {_eq: $id}}) {
                    affected_rows
                }
            }
            """,
        )
        variables = {"id": lock_name}
        lock = await self.execute_async(query, variable_values=variables)
        if lock["delete_lock_table"]["affected_rows"] == 1:
            return True
        else:
            return False
