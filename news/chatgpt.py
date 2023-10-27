import os
import asyncio
import threading
from queue import Queue

import openai
from mylib.log import log

from config import config

openai.api_key = config.openai_api_key

CHAT_GPT_MAX_SECONDS_TO_ANSWER = 20
CHAT_GPT_SECONDS_TO_WAIT_IF_ERROR = 20


async def ask_chatgpt_async_worker(result, result_queue):
    """ask_chatgpt_async_worker"""
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
    result_queue.put(result)


def ask_chatgpt_worker(result, result_queue):
    """ask_chatgpt_worker"""
    asyncio.run(ask_chatgpt_async_worker(result, result_queue))


async def ask_chatgpt(chatgpt_data: dict, log_pid: str = ""):
    """ask_chatgpt"""
    log_pid += "ask_chatgpt: "
    attempt = 0
    is_get_result = False

    while attempt < 5:
        attempt += 1
        log.info(log_pid + f"ChatGPT has started (attempt {attempt})")

        chatgpt_data["error"] = ""
        chatgpt_data["answer"] = ""

        try:
            result_queue = Queue()

            thread = threading.Thread(
                target=ask_chatgpt_worker, args=(chatgpt_data, result_queue)
            )
            thread.start()
            thread.join(timeout=CHAT_GPT_MAX_SECONDS_TO_ANSWER)
            error = chatgpt_data["error"]
            answer = chatgpt_data["answer"]
            if error != "" or answer != "":
                return
            log.warning(log_pid + f"ChatGPT hang on. Restarted {attempt} time(s)")
        except Exception as exception:
            log.warning(log_pid + f" {exception}")

        await asyncio(CHAT_GPT_SECONDS_TO_WAIT_IF_ERROR)

        # chatgpt_timeout = CHAT_GPT_MAX_SECONDS_TO_ANSWER
        # is_get_result = False
        # while chatgpt_timeout > 0:
        #     chatgpt_timeout -= 1
        #     await asyncio.sleep(1)
        #     result = result_queue.get()
        #     if result:
        #         error = result["error"]
        #         if error != "":
        #             # error
        #             log.warning(log_pid + f"ChatGPT error: {error}")
        #             is_get_result = True
        #             chatgpt_data["error"] = error
        #             break
        #         answer = result["answer"]
        #         if answer != "":
        #             # ok
        #             is_get_result = True
        #             chatgpt_data["answer"] = answer
        #             break
        # if is_get_result:
        #     thread.join()
        #     break
        # log.warning(log_pid + f"ChatGPT hang on. Restarted {attempt} time(s)")
        # thread._stop()


async def test_chatgpt():
    chatgpt_data = {
        "answer": "",
        "error": "",
        "messages": [{"role": "user", "content": "2+4="}],
    }
    await ask_chatgpt(chatgpt_data)
    log.info(f"{chatgpt_data}")


if __name__ == "__main__":
    asyncio.run(test_chatgpt())
