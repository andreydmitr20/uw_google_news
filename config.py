""" get constants from .env"""
import os

from dotenv import load_dotenv

load_dotenv()


# from config import config
class config:
    """common config constants"""

    openai_api_key: str = os.getenv("openai_api_key")

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
