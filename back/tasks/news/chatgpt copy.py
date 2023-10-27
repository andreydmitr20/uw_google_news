from copy import deepcopy

import os
import time
import threading
from queue import Queue
from unittest import result

import openai
from .mylib.log import log, d
import concurrent.futures


from .config import config

openai.api_key = config.openai_api_key
CHAT_GPT_MAX_SECONDS_TO_ANSWER = 3
CHAT_GPT_SECONDS_TO_WAIT_IF_ERROR = 10
CHAT_GPT_RATE_LIMIT_TEXT = "Rate limit".lower()


def chatgpt_worker(data):
    result = deepcopy(data)
    try:
        # log.info(f" pid:{os.getpid()}")
        d(1)
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=result["messages"],
            timeout=CHAT_GPT_MAX_SECONDS_TO_ANSWER,
        )
        d(2)
        answer = completion.choices[0].message
        d(3)
        result["answer"] = answer["content"]
        # log.info(f"chatgpt_worker: {answer}")

    except Exception as exception:
        d(4)
        error = f"{exception}"
        # log.warning(error)
        result["error"] = error

    # log.info(f"{result}")
    return result


def run_function_with_timeout(func, *args, timeout_seconds):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(func, *args)
        try:
            result = future.result(timeout=timeout_seconds)
            return result
        except concurrent.futures.TimeoutError:
            return None


def ask_chatgpt(chatgpt_data: dict, log_pid: str = "") -> dict:
    """ask_chatgpt"""
    log_pid += "ask_chatgpt: "
    attempt = 0

    while attempt < 5:
        attempt += 1
        log.info(log_pid + f"ChatGPT has started (attempt {attempt})")

        chatgpt_data["error"] = ""
        chatgpt_data["answer"] = ""

        result = run_function_with_timeout(
            chatgpt_worker,
            chatgpt_data,
            timeout_seconds=CHAT_GPT_MAX_SECONDS_TO_ANSWER,
        )
        # log.info(f">{result}")

        if result:
            if result["answer"] != "":
                result["error"] = ""

            # error = result["error"]
            # if error.lower().find(CHAT_GPT_RATE_LIMIT_TEXT) >= 0:
            #     log.warning(
            #         log_pid
            #         + f"ChatGPT rate limit. Waiting {CHAT_GPT_SECONDS_TO_WAIT_IF_ERROR}s. {error}"
            #     )
            break
        else:
            log.warning(log_pid + f"ChatGPT hang on. Restarted {attempt} time(s)")
            time.sleep(CHAT_GPT_SECONDS_TO_WAIT_IF_ERROR)
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
