import logging
import os

import aiohttp

from odh_core import phonenumber

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class SmsClient:
    def __init__(self, **kwargs) -> None:
        self.session = aiohttp.ClientSession(**kwargs)

    async def send(
        self,
        to_number: str,
        message: str,
        from_number: str,
        twilio_account_sid: str = None,
        twilio_auth_token: str = None,
    ):
        """Send SMS via Twilio.

        Using the http api, we are skipping twilio official python library keep dependencies low.

        Validates phone number with :any:`phonenumber.parse_nr`

        If you are using messaging_service_sid it's the same as from number.

        Args:
            phone_number (str): Phone number to send sms to.
            message (str): Message to send.
            from_number (str): messaging_service_sid or text sender ID, see: https://46elks.se/kb/text-sender-id
        """

        if message is None:
            raise ValueError("message is required")

        if from_number is None:
            raise ValueError("from_number is required")

        if twilio_account_sid is None:
            log.warning("twilio_account_sid is not set, trying to get from env")
            twilio_account_sid = os.environ.get("TWILIO_ACCOUNT_SID", default=None)
            if twilio_account_sid is None:
                raise ValueError(
                    "env TWILIO_ACCOUNT_SID is required or set as argument"
                )

        if twilio_auth_token is None:
            log.warning("twilio_auth_token is not set, trying to get from env")
            twilio_auth_token = os.environ.get("TWILIO_AUTH_TOKEN", default=None)
            if twilio_auth_token is None:
                raise ValueError("env TWILIO_AUTH_TOKEN is required or set as argument")

        log.debug(f"twilio_account_sid: {twilio_account_sid}")
        log.debug(f"twilio_auth_token: {twilio_auth_token}")
        url = f"https://api.twilio.com/2010-04-01/Accounts/{twilio_account_sid}/Messages.json"
        # will raise ValueError if invalid
        to_number = phonenumber.parse_nr(to_number)

        payload = aiohttp.FormData(
            {
                "To": to_number,
                "From": from_number,
                "Body": message,
            }
        )

        auth = aiohttp.BasicAuth(login=twilio_account_sid, password=twilio_auth_token)

        async with self.session.request(
            method="POST", url=url, data=payload, auth=auth
        ) as resp:
            log.debug(await resp.text())
            if resp.status == 201:
                log.info(f"SMS sent to {to_number}")
                return True
            else:
                log.error(f"SMS failed to {to_number}")
                return False

