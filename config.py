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
