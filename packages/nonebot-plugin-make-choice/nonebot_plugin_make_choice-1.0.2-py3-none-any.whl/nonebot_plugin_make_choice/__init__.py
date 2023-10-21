import random
from nonebot import get_driver
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.params import RegexGroup
from nonebot.plugin import on_regex
from nonebot.plugin import PluginMetadata

from typing import Any, Annotated

from .config import ChoiceConfig

global_config = get_driver().config
config = ChoiceConfig.parse_obj(global_config)

__plugin_meta__ = PluginMetadata(
    name="选择困难症",
    description="选择困难症？Bot帮你选！",
    usage="发送选xx选xx即可触发",
    type="application",
    homepage="https://github.com/SherkeyXD/nonebot-plugin-make-choice",
    supported_adapters={"~onebot.v11"},
    config=ChoiceConfig()
)

choice = on_regex(r'^[选要](\S*)[选要](\S*)', priority=20, block=True)
@choice.handle()
async def make_choice(event : Event, match_group: Annotated[tuple[Any, ...], RegexGroup()]):
    random_choice = random.choice(match_group)
    if random.random() < config.choose_both_chance:
        random_choice = "我全都要！"
    await choice.finish(MessageSegment.reply(id_=event.message_id) + MessageSegment.text(f"建议您选择：\n{random_choice}"))