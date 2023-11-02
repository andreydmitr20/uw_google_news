""" get constants from .env"""
import os

from dotenv import load_dotenv

load_dotenv()


# from config import config
class config:
    """common config constants"""

    twilio_sid: str = os.getenv("twilio_sid")
    twilio_token: str = os.getenv("twilio_token")
    from_phone: str = os.getenv("from_phone")

    timezone: str = os.getenv("timezone")

    news_api_path: str = os.getenv("news_api_path")
    news_api_user: str = os.getenv("news_api_user")
    news_api_pass: str = os.getenv("news_api_pass")

    openai_api_key: str = os.getenv("openai_api_key")
    webflow_api_token: str = os.getenv("webflow_api_token")

    selenium_host = os.getenv("selenium_host")
    selenium_prefix = os.getenv("selenium_prefix")
    selenium_port = os.getenv("selenium_port")
    selenium_postfix = os.getenv("selenium_postfix")

    db_proto: str = os.getenv("db_proto")
    db_user: str = os.getenv("db_user")
    db_pass: str = os.getenv("db_pass")
    db_host: str = os.getenv("db_host")
    db_name: str = os.getenv("db_name")
    db_port: str = os.getenv("db_port")

    redis_host = os.getenv("redis_host")
    redis_port = os.getenv("redis_port")
