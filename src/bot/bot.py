import re
import logging
from urllib import response
import telebot
import requests
import df_engine.conditions as cnd
import df_engine.responses as rsp
import df_engine.labels as lbl

from typing import Optional, Union
from argparse import ArgumentParser
from df_engine.core.keywords import GLOBAL, TRANSITIONS, RESPONSE
from df_engine.core import Context, Actor


parser = ArgumentParser()
parser.add_argument("--telebot_key",
                    help="token you get from @BotFather",
                    required=True)
args = parser.parse_args()
telebot_key = args.telebot_key
bot = telebot.TeleBot(telebot_key)

URL = "http://127.0.0.1:8888/"

logging.basicConfig(filename="logs.txt",
                    filemode='a',
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_response(context: Context, actor: Actor, *args, **kwargs) -> str:
    try:
        question = context.last_request

        if not re.match(r"^[a-zA-Z0-9\s?]+$", question):
            e = "Error: incorrect question. Question can contain only english letters, numbers and '?'"
            logger.warning(e)
            return e

        res = requests.post(URL, json={"question": question})
        
        answer = res.json()["answer"]
    except Exception as e:
        logger.exception(e)
        answer = e

    return answer

plot = {
    "qa_flow": {
        "answer_node": {
            RESPONSE: generate_response,
            TRANSITIONS: {"answer_node": cnd.true(), }
        },
        "fallback_node": {
            RESPONSE: "incorrect question",
            TRANSITIONS: {"answer_node": cnd.true()}
        }
    }
}

actor = Actor(plot,
              start_label=("qa_flow", "answer_node"),
              fallback_label=("qa_flow", "fallback_node"),
              label_priority=1.0)

ctx = {}

def turn_handler(user_request: str, ctx: Union[Context, str, dict], actor: Actor, true_response: Optional[str] = None):
    ctx = Context.cast(ctx)
    ctx.add_request(user_request)  # append user_request to ctx
    ctx = actor(ctx)  # append actor's response to ctx

    actual_response = ctx.last_response  # get actor's response

    if true_response is not None and true_response != actual_response:
        msg = f"in_request={user_request} -> true_actual_response != actual_response: {true_response} != {actual_response}"
        raise Exception(msg)
    else:
        logger.info(f"request={user_request} -> response={actual_response}")
    return actual_response, ctx


# ____________________________________________________ Bot part _________________________________________________________


@bot.message_handler()
def reply(message):
    response, _ = turn_handler(message.text, ctx, actor)
    bot.send_message(message.chat.id, response)


if __name__ == "__main__":
    bot.infinity_polling()
