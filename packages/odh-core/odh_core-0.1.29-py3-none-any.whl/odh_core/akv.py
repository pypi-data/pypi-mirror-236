import asyncio
import logging

import aiohttp

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class akv:  # noqa: N801
    """Simple script to get secrets from azure key vault.

    .. todo::
        - Add support to list secrets
        - Better error handling


    Example:
        .. code-block:: python

            import asyncio
            import odh_core

            async def main():
                akvv = odh_core.akv(vault_url="https://demo-valut.vault.azure.net/")

                await akvv.login_device_code()
                secret = await akvv.get_secret("mysecret")
                print(f"{secret=}")

            if __name__ == "__main__":
                asyncio.run(main())


    """
    def __init__(self, sleep_time: int = 3, timeout: int = 5, vault_url: str = "") -> None:  # noqa: D107
        self.sleep_time = sleep_time
        self.timeout = timeout
        self.url = "https://login.microsoftonline.com/common/oauth2"
        self.vault_url = vault_url
        self.status_ok = 200
        self.access_token = None
        self.payload = {
            "grant_type": "device_code",
            # client_id from azure-cli
            # https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/identity/azure-identity/azure/identity/_constants.py
            "client_id": "04b07795-8ddb-461a-bbee-02f9e1bf7b46",
            "resource": "https://vault.azure.net",
        }

        if not self.vault_url:
            raise ValueError("vault_url is required")  # noqa: TRY003, EM101

    async def login_device_code(self) -> bool:
        """Interactive login using device code flow.

        Uses azure cli client_id and common as tenant_id

        .. note::
            Only tested and working on with access to azure-key-vault

        .. note::
            Uses print and input

        Returns:
            bool: True if login was successful

        """
        async with aiohttp.ClientSession() as session:

            # first request is to request device code
            async with session.post(f"{self.url}/devicecode", data=self.payload) as resp:
                data = await resp.json()
                print(data["message"])

            # need to edit payload
            self.payload["grant_type"] = "urn:ietf:params:oauth:grant-type:device_code"
            self.payload["code"] = data["device_code"]

            while True:
                async with session.post(f"{self.url}/token", data=self.payload) as resp:
                    tokendata = await resp.json()
                    if resp.status == self.status_ok:
                        log.debug("token acquired")
                        self.access_token = tokendata["access_token"]
                        return True
                await asyncio.sleep(self.sleep_time)

    async def get_secret(self, secret_name: str):
        """Get secret from azure key vault.

        .. note::
            Only tested and working on with access to azure-key-vault

        """
        url = f"{self.vault_url}/secrets/{secret_name}?api-version=7.1"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, data=self.payload) as resp:
                data = await resp.json()
                return data["value"]


if __name__ == "__main__":
    print("This is a module, import it")
