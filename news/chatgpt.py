from copy import deepcopy

import os
import time
import threading
from queue import Queue

import openai
from mylib.log import log

from config import config

openai.api_key = config.openai_api_key

CHAT_GPT_MAX_SECONDS_TO_ANSWER = 20
CHAT_GPT_SECONDS_TO_WAIT_IF_ERROR = 20


def ask_chatgpt_worker(result):  # , result_queue):
    """ask_chatgpt_worker"""
    try:
        log.info(f"ask_chatgpt_async_worker: pid:{os.getpid()}")

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=result["messages"]
        )
        answer = completion.choices[0].message
        result["answer"] = answer["content"]
        # log.info(f"{answer}")
    except Exception as exception:
        error = f"{exception}"
        # log.warning(log_pid + error)
        result["error"] = error
    # result_queue.put(result)


def ask_chatgpt(chatgpt_data: dict, log_pid: str = ""):
    """ask_chatgpt"""
    log_pid += "ask_chatgpt: "
    attempt = 0

    while attempt < 5:
        attempt += 1
        log.info(log_pid + f"ChatGPT has started (attempt {attempt})")

        chatgpt_data["error"] = "No data"
        chatgpt_data["answer"] = ""
        temp_chatgpt_data = deepcopy(chatgpt_data)
        try:
            # result_queue = Queue()

            thread = threading.Thread(
                target=ask_chatgpt_worker, args=(temp_chatgpt_data,)  # result_queue)
            )
            thread.start()
            thread.join(timeout=CHAT_GPT_MAX_SECONDS_TO_ANSWER)
            # chatgpt_data = result_queue.get()

            error = temp_chatgpt_data["error"]
            answer = temp_chatgpt_data["answer"]
            if answer != "":
                # ok
                chatgpt_data["answer"] = answer
                chatgpt_data["error"] = ""

                # log.info(log_pid + f"answer: {answer}")
                log.info(log_pid + f"ok")

                return
            if error == "":
                log.warning(log_pid + f"ChatGPT hang on. Restarted {attempt} time(s)")
            else:
                if error.lower().find("Rate limit".lower()) >= 0:
                    log.warning(log_pid + f"ChatGPT rate limit error. {error}")
                else:
                    chatgpt_data["error"] = error
                    return
        except Exception as exception:
            log.warning(log_pid + f" {exception}")
        finally:
            temp_chatgpt_data = None

        time.sleep(CHAT_GPT_SECONDS_TO_WAIT_IF_ERROR)


def test_chatgpt():
    chatgpt_data = {
        "answer": "",
        "error": "",
        "messages": [{"role": "user", "content": "2+4="}],
    }
    ask_chatgpt(chatgpt_data)
    log.info(f"{chatgpt_data}")


if __name__ == "__main__":
    test_chatgpt()
