""" get constants from .env"""
import os

from dotenv import load_dotenv

load_dotenv()


# from config import config
class config:
    """common config constants"""

    openai_api_key: str = os.getenv("openai_api_key")
