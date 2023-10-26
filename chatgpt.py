import openai
from config import config
from .mylib.log import log

openai.api_key = config.openai_api_key

MESSAGES = [
    {
        "role": "system",
        "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair.",
    },
    {
        "role": "user",
        "content": "Compose a poem that explains the concept of recursion in programming.",
    },
]


async def ask_chat(messages: list) -> dict:
    error = ""
    answer = ""
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        answer = completion.choices[0].message
        log.info(f"{answer}")
    except Exception as exception:
        error = f"{exception}"
        log.warning(error)
        answer = ""

    return {"messages": messages, "error": error, "answer": answer}
