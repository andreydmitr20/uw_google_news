from copy import deepcopy
import psutil
import os
import time
import threading
from queue import Queue
from unittest import result
import multiprocessing as mp

import openai
from .mylib.log import log, d
import concurrent.futures
from openai.error import ServiceUnavailableError, APIError, RateLimitError, Timeout


from .config import config

openai.api_key = config.openai_api_key
CHAT_GPT_MAX_SECONDS_TO_ANSWER = 20
CHAT_GPT_SECONDS_TO_WAIT_IF_ERROR = 20
CHAT_GPT_RATE_LIMIT_TEXT = "Rate limit".lower()

"""
  {
  "id": "chatcmpl-8EKp0lzoyJHriXHT8gZ0eL5qBey1Y",
  "object": "chat.completion",
  "created": 1698427322,
  "model": "gpt-3.5-turbo-0613",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Boulder Weekly reveals winners of Best of Boulder East County 2023, including pARTiculars Art Gallery, Primrose School, Rabbit Hole Recreation, Nissi's, and Longmont Theatre Company."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 761,
    "completion_tokens": 42,
    "total_tokens": 803
  }
}
"""


def ask_chatgpt_worker(chatgpt_data: dict):
    try:
        d(1)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.7,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            n=1,
            stop=None,
            messages=chatgpt_data["messages"],
        )
        d(2)
        # log.info(log_pid + f"==={response}")
        chatgpt_data["answer"] = response["choices"][0]["message"]["content"]
        chatgpt_data["error"] = ""
        return
    except APIError:
        error = f"APIError Exception, retrying..."
        # log.warning(log_pid + error)
    except Timeout:
        error = f"APIError Timeout, retrying..."
        # log.warning(log_pid + error)

    except ServiceUnavailableError:
        error = f"ServiceUnavailableError Exception, retrying..."
        # log.warning(log_pid + error)

        # time.sleep(CHAT_GPT_SECONDS_TO_WAIT_IF_ERROR)
    except RateLimitError:
        error = f"RateLimitError Exception, retrying..."
        # log.warning(log_pid + error)

        # time.sleep(CHAT_GPT_SECONDS_TO_WAIT_IF_ERROR)
    chatgpt_data["error"] = error
    d(3)


def ask_chatgpt(chatgpt_data: dict, log_pid: str = "") -> dict:
    """ask_chatgpt"""
    log_pid += "ask_chatgpt: "
    result = chatgpt_data

    for _ in range(5):
        os_pid = None
        os_pid_creation_time = None
        result["answer"] = ""
        result["error"] = ""
        try:
            spawn = mp.get_context("spawn")
            process = spawn.Process(target=ask_chatgpt_worker, args=(result,))
            process.daemon = True
            process.start()
            os_pid = process.pid
            process_info = psutil.Process(os_pid)
            os_pid_creation_time = process_info.create_time()

            for _ in range(CHAT_GPT_MAX_SECONDS_TO_ANSWER):
                process_info = psutil.Process(os_pid)
                if not process_info.is_running():
                    return result
                time.sleep(1)

        finally:
            process_info = psutil.Process(os_pid)
            if (
                process_info.is_running()
                and process_info.create_time() == os_pid_creation_time
            ):
                os.kill(os_pid)

    result["error"] = "Too much attempts to get data"
    return result


def is_chatgpt_error_rate_limit(error: str) -> bool:
    return error.lower().find(CHAT_GPT_RATE_LIMIT_TEXT) >= 0


def test_chatgpt():
    chatgpt_data = {
        "answer": "",
        "error": "",
        "messages": [{"role": "user", "content": "2+4="}],
    }
    result = ask_chatgpt(chatgpt_data)
    log.info(f"{result}")


if __name__ == "__main__":
    test_chatgpt()
