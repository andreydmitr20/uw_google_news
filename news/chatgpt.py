import asyncio

import openai
from mylib.log import log

from config import config

openai.api_key = config.openai_api_key

TEST_MESSAGES = [
    {
        "role": "system",
        "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair.",
    },
    {
        "role": "user",
        "content": "Compose a poem that explains the concept of recursion in programming.",
    },
]


async def ask_chatgpt(messages: list) -> dict:
    error = ""
    answer = ""
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        answer = completion.choices[0].message
        # log.info(f"{answer}")
    except Exception as exception:
        error = f"{exception}"
        log.warning("chatGPT: " + error)
        answer = ""

    return {"messages": messages, "error": error, "answer": answer}


async def test_chatgpt():
    result = await ask_chatgpt([{"role": "user", "content": "2+4="}])
    log.info(f"{result}")


if __name__ == "__main__":
    asyncio.run(test_chatgpt())
