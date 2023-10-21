import json
import logging
import os

import aiohttp

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class EmailClient:
    def __init__(self, **kwargs) -> None:
        self.session = aiohttp.ClientSession(**kwargs)

    async def send(
        self,
        to_email: str,
        from_email: str,
        subject: str,
        body: str,
        addresses: dict = None,
    ) -> bool:
        """Send Email via MS Logic App.

        Args:
            to_email (str): Email address to send to.
            from_email (str): Email address to send from.
            subject (str): Subject of email.
            body (str): Body of email.
            addresses (dict, optional): Dictionary map of from email to url post

        Returns:
            bool: True if successful
        """

        if addresses is None:
            log.warning("addresses is not set, trying to get from env")
            addresses = os.environ.get("SEND_EMAIL_ADDRESSES", default=None)
            if addresses is None:
                raise ValueError("addresses is required")
            try:
                addresses = json.loads(addresses)
            except json.JSONDecodeError:
                raise ValueError("addresses is not json")

        try:
            url = addresses[from_email]
        except KeyError:
            raise ValueError("from_email is not addresses")

        payload = {"email": to_email, "subject": subject, "message": body}
        async with self.session.request(method="POST", url=url, json=payload) as r:
            log.info(f"Email sent to {to_email}, status: {r.status}")
            log.debug(await r.text())
            if r.status < 300:
                return True
            else:
                return False
