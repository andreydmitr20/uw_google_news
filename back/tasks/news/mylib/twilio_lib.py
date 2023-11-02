# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from config import config

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = config.twilio_sid
auth_token = config.twilio_token
client = Client(account_sid, auth_token)

MESSAGE_SID_LENGTH = 34


def send_sms(from_phone: str, to_phone: str, sms_text: str):
    message = client.messages.create(
        body=sms_text,
        from_=from_phone,
        to=to_phone,
    )

    return message.sid


if __name__ == "__main__":
    # print(config.from_phone)
    try:
        sms_sid = send_sms(
            config.from_phone,
            "+16174305286",
            "Test messaging for Nik's myheadlines.ai",
        )
        print(sms_sid)
    except Exception as exception:
        print(f"{exception}")
