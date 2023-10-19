import asyncio
from datetime import datetime
from functools import lru_cache
import inspect
import logging
import operator
import pkgutil
import random
import sys
from typing import List, Type
from importlib import import_module

import yaml
from dateutil import parser
from pyrogram.enums import ChatType
from pyrogram.handlers import MessageHandler, EditedMessageHandler, RawUpdateHandler
from pyrogram.types import Message, InlineKeyboardMarkup, ReplyKeyboardMarkup
from rich import box
from rich.live import Live
from rich.panel import Panel
from rich.table import Column, Table
from rich.text import Text

from ..utils import batch, flatten, idle, time_in_range, async_partial, next_random_datetime
from ..log import logger, formatter
from . import __name__
from .link import Link
from .log import TelegramStream
from .tele import Client, ClientsSession
from .bots.base import BaseBotCheckin

logger = logger.bind(scheme="telegram")


def get_spec(type: str):
    """服务模块路径解析."""
    if type == "checkiner":
        sub = "bots"
        suffix = "checkin"
    elif type == "monitor":
        sub = "monitor"
        suffix = "monitor"
    elif type == "messager":
        sub = "messager"
        suffix = "messager"
    else:
        raise ValueError(f"{type} is not a valid service.")
    return sub, suffix


@lru_cache
def get_names(type: str, allow_ignore=False) -> List[str]:
    """列出服务中所有可用站点."""
    sub, _ = get_spec(type)
    results = []
    typemodule = import_module(f"{__name__}.{sub}")
    for _, mn, _ in pkgutil.iter_modules(typemodule.__path__):
        module = import_module(f"{__name__}.{sub}.{mn}")
        if allow_ignore or (not getattr(module, "__ignore__", False)):
            results.append(mn)
    return results


def get_cls(type: str, names: List[str] = None) -> List[Type]:
    """获得服务特定站点的所有类."""
    sub, suffix = get_spec(type)
    if names == None:
        names = get_names(type)
    results = []
    for name in names:
        try:
            module = import_module(f"{__name__}.{sub}.{name.lower()}")
            for cn, cls in inspect.getmembers(module, inspect.isclass):
                if (name.lower().replace("_", "") + suffix).lower() == cn.lower():
                    results.append(cls)
        except ImportError:
            all_names = get_names(type)
            logger.warning(f'您配置的 "{type}" 不支持站点 "{name}", 请从以下站点中选择:')
            logger.warning(", ".join(all_names))
    return results


def extract(clss: List[Type]) -> List[Type]:
    """对于嵌套类, 展开所有子类."""
    extracted = []
    for cls in clss:
        ncs = [c for c in cls.__dict__.values() if inspect.isclass(c)]
        if ncs:
            extracted.extend(ncs)
        else:
            extracted.append(cls)
    return extracted


async def dump_message(client: Client, message: Message, table: Table):
    """消息调试工具, 将消息更新列到 table 中."""
    text = message.text or message.caption
    if text:
        text = text.replace("\n", " ")
        if not text:
            return
    else:
        return
    if message.from_user:
        user = message.from_user
        sender_id = str(user.id)
        sender_icon = "👤"
        if message.outgoing:
            sender = Text("Me", style="bold red")
            text = Text(text, style="red")
        else:
            sender = user.name
            if user.is_bot:
                sender_icon = "🤖"
                sender = Text(sender, style="bold yellow")
    else:
        sender = sender_id = sender_icon = None

    chat_id = "{: }".format(message.chat.id)
    if message.chat.type == ChatType.GROUP or message.chat.type == ChatType.SUPERGROUP:
        chat = message.chat.title
        chat_icon = "👥"
    elif message.chat.type == ChatType.CHANNEL:
        chat = message.chat.title
        chat_icon = "📢"
    elif message.chat.type == ChatType.BOT:
        chat = None
        chat_icon = "🤖"
    else:
        chat = chat_icon = None
    others = []
    if message.photo:
        others.append(f"照片: {message.photo.file_unique_id}")
    if message.reply_markup:
        if isinstance(message.reply_markup, InlineKeyboardMarkup):
            key_info = "|".join([k.text for r in message.reply_markup.inline_keyboard for k in r])
            others.append(f"按钮: {key_info}")
        elif isinstance(message.reply_markup, ReplyKeyboardMarkup):
            key_info = "|".join([k.text for r in message.reply_markup.keyboard for k in r])
            others.append(f"按钮: {key_info}")
    return table.add_row(
        f"{client.me.name}",
        "│",
        chat_icon,
        chat,
        chat_id,
        "│",
        sender_icon,
        sender,
        sender_id,
        "│",
        text,
        "|",
        "; ".join(others),
    )


async def checkin_task(checkiner: BaseBotCheckin, sem, wait=0):
    """签到器壳, 用于随机等待开始."""
    if wait > 0:
        checkiner.log.debug(f"随机启动等待: 将等待 {wait} 分钟以启动.")
    await asyncio.sleep(wait * 60)
    async with sem:
        return await checkiner._start()


async def gather_task(tasks, username):
    return username, await asyncio.gather(*tasks)


async def checkiner(config: dict, instant=False):
    """签到器入口函数."""
    logger.debug("正在启动每日签到模块, 请等待登录.")
    async with ClientsSession.from_config(config) as clients:
        coros = []
        async for tg in clients:
            log = logger.bind(scheme="telechecker", username=tg.me.name)
            if not await Link(tg).auth("checkiner"):
                log.error(f"功能初始化失败: 权限校验不通过.")
                continue
            sem = asyncio.Semaphore(int(config.get("concurrent", 1)))
            clses = extract(get_cls("checkiner", names=config.get("service", {}).get("checkiner", None)))
            checkiners = [
                cls(
                    tg,
                    retries=config.get("retries", 4),
                    timeout=config.get("timeout", 120),
                    nofail=config.get("nofail", True),
                    basedir=config.get("basedir", None),
                    proxy=config.get("proxy", None),
                    config=config.get("checkiner", {}).get(cls.__module__.rsplit(".", 1)[-1], {}),
                )
                for cls in clses
            ]
            tasks = []
            names = []
            for c in checkiners:
                names.append(c.name)
                wait = 0 if instant else random.randint(0, int(config.get("random", 15)))
                task = asyncio.create_task(checkin_task(c, sem, wait))
                tasks.append(task)
            coros.append(asyncio.ensure_future(gather_task(tasks, username=tg.me.name)))
            if names:
                log.debug(f'已启用签到器: {", ".join(names)}')
        while coros:
            done, coros = await asyncio.wait(coros, return_when=asyncio.FIRST_COMPLETED)
            for t in done:
                try:
                    username, results = await t
                except asyncio.CancelledError:
                    continue
                log = logger.bind(scheme="telechecker", username=username)
                failed = []
                ignored = []
                successful = []
                for i, c in enumerate(checkiners):
                    if results[i] == False:
                        failed.append(c)
                    elif results[i] is None:
                        ignored.append(c)
                    else:
                        successful.append(c)
                spec = f"共{len(checkiners)}个"
                if successful:
                    spec += f", {len(successful)}成功"
                if failed:
                    spec += f", {len(failed)}失败"
                if ignored:
                    spec += f", {len(ignored)}跳过"
                if failed:
                    log.error(f"签到失败 ({spec}): {','.join([f.name for f in failed])}")
                else:
                    log.bind(notify=True).info(f"签到成功 ({spec}).")


async def checkiner_schedule(config: dict, start_time=None, end_time=None, instant=False):
    """签到器计划任务."""
    dt = next_random_datetime(start_time, end_time, 0)
    while True:
        logger.bind(scheme="telechecker").info(f"下一次签到将在 {dt.strftime('%m-%d %H:%M %p')} 进行.")
        await asyncio.sleep((dt - datetime.now()).seconds)
        await checkiner(config, instant=instant)


async def monitorer(config: dict):
    """监控器入口函数."""
    logger.debug("正在启动消息监控模块.")
    jobs = []
    async with ClientsSession.from_config(config, monitor=True) as clients:
        async for tg in clients:
            log = logger.bind(scheme="telemonitor", username=tg.me.name)
            if not await Link(tg).auth("monitorer"):
                log.error(f"功能初始化失败: 权限校验不通过.")
                continue
            clses = extract(get_cls("monitor", names=config.get("service", {}).get("monitor", None)))
            names = []
            for cls in clses:
                cls_config = config.get("monitor", {}).get(cls.__module__.rsplit(".", 1)[-1], {})
                jobs.append(
                    asyncio.create_task(
                        cls(
                            tg,
                            nofail=config.get("nofail", True),
                            basedir=config.get("basedir", None),
                            proxy=config.get("proxy", None),
                            config=cls_config,
                        )._start()
                    )
                )
                names.append(cls.name)
            if names:
                log.debug(f'已启用监控器: {", ".join(names)}')
        await asyncio.gather(*jobs)


async def messager(config: dict):
    """自动回复器入口函数."""
    logger.debug("正在启动自动水群模块.")
    messagers = []
    async with ClientsSession.from_config(config, send=True) as clients:
        async for tg in clients:
            log = logger.bind(scheme="telemessager", username=tg.me.name)
            if not await Link(tg).auth("messager"):
                log.error(f"功能初始化失败: 权限校验不通过.")
                continue
            clses = extract(get_cls("messager", names=config.get("service", {}).get("messager", None)))
            for cls in clses:
                cls_config = config.get("messager", {}).get(cls.__module__.rsplit(".", 1)[-1], {})
                messagers.append(
                    cls(
                        {"api_id": tg.api_id, "api_hash": tg.api_hash, "phone": tg.phone_number},
                        username=tg.me.name,
                        nofail=config.get("nofail", True),
                        proxy=config.get("proxy", None),
                        basedir=config.get("basedir", None),
                        config=cls_config,
                    )
                )
    await asyncio.gather(*[m.start() for m in messagers])


async def follower(config: dict):
    """消息调试工具入口函数."""
    columns = [
        Column("用户", style="cyan", justify="center"),
        Column("", max_width=1, style="white"),
        Column("", max_width=2, overflow="crop"),
        Column("会话", style="bright_blue", no_wrap=True, justify="right", max_width=15),
        Column("(ChatID)", style="gray50", no_wrap=True, max_width=20),
        Column("", max_width=1, style="white"),
        Column("", max_width=2, overflow="crop"),
        Column("发信人", style="green", no_wrap=True, max_width=15, justify="right"),
        Column("(UserID)", style="gray50", no_wrap=True, max_width=15),
        Column("", max_width=1, style="white"),
        Column("信息", no_wrap=False, min_width=30, max_width=50),
        Column("", max_width=1, style="white"),
        Column("其他", no_wrap=False, min_width=30, max_width=50),
    ]
    async with ClientsSession.from_config(config) as clients:
        table = Table(*columns, header_style="bold magenta", box=box.SIMPLE)
        func = async_partial(dump_message, table=table)
        async for tg in clients:
            tg.add_handler(MessageHandler(func))
            tg.add_handler(EditedMessageHandler(func))
        with Live(table, refresh_per_second=4, vertical_overflow="visible"):
            await idle()


async def dumper(config: dict):
    async def _dumper(client, update, users, chats):
        print("=" * 50, flush=True, file=sys.stderr)
        print(update, flush=True, file=sys.stderr)

    async with ClientsSession.from_config(config) as clients:
        async for tg in clients:
            tg.add_handler(RawUpdateHandler(_dumper))
        logger.info(f'开始监控账号: "{tg.me.name}" 中的更新.')
        await idle()


class IndentDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


async def analyzer(config: dict, chats, keywords, timerange, limit=10000, outputs=1000):
    """历史消息分析工具入口函数."""

    from rich.progress import MofNCompleteColumn, Progress, SpinnerColumn

    def render_page(progress, texts):
        page = Table.grid()
        page.add_row(Panel(progress))
        if texts:
            msgs = sorted(texts.items(), key=operator.itemgetter(1), reverse=True)
            columns = flatten([[Column(max_width=15, no_wrap=True), Column(min_width=2)] for _ in range(4)])
            table = Table(*columns, show_header=False, box=box.SIMPLE)
            cols = []
            for col in batch(msgs, 12):
                col = [(t.split()[0], str(c)) for t, c in col]
                col += [("", "")] * (12 - len(col))
                cols.append(col)
                if len(cols) >= 4:
                    break
            for row in map(list, zip(*cols)):
                table.add_row(*flatten(row))
            page.add_row(table)
        return page

    texts = {}
    if timerange:
        start, end = (parser.parse(t).time() for t in timerange)
    async with ClientsSession.from_config(config) as clients:
        async for tg in clients:
            target = f"{tg.me.name}.msgs.yaml"
            logger.info(f'开始分析账号: "{tg.me.name}", 结果将写入"{target}".')
            pcs = list(Progress.get_default_columns())
            pcs.insert(0, SpinnerColumn())
            pcs.insert(3, MofNCompleteColumn(table_column=Column(justify="center")))
            p = Progress(*pcs, transient=True)
            with Live(render_page(p, texts)) as live:
                updates = 0
                pchats = p.add_task("[red]会话: ", total=len(chats))
                for c in chats:
                    c = c.rsplit("/", 1)[-1]
                    pmsgs = p.add_task("[red]记录: ", total=limit)
                    m: Message
                    async for m in tg.get_chat_history(c, limit=limit):
                        if m.text:
                            if m.from_user and not m.from_user.is_bot:
                                if (not keywords) or any(s in m.text for s in keywords):
                                    if (not timerange) or time_in_range(start, end, m.date.time()):
                                        if m.text in texts:
                                            texts[m.text] += 1
                                        else:
                                            texts[m.text] = 1
                                        updates += 1
                                        if updates % 200 == 0:
                                            live.update(render_page(p, texts))
                        p.advance(pmsgs)
                    p.update(pmsgs, visible=False)
                    p.advance(pchats)
            with open(target, "w+") as f:
                yaml.dump(
                    {
                        "messages": [
                            str(t) for t, _ in sorted(texts.items(), key=operator.itemgetter(1), reverse=True)
                        ][:outputs]
                    },
                    f,
                    default_flow_style=False,
                    encoding="utf-8",
                    allow_unicode=True,
                    Dumper=IndentDumper,
                )


async def notifier(config: dict):
    """消息通知初始化函数."""

    def _filter(record):
        notify = record.get("extra", {}).get("notify", None)
        if notify or record["level"].no == logging.ERROR:
            return True
        else:
            return False

    def _formatter(record):
        notify = record.get("extra", {}).get("notify", False)
        format = formatter(record)
        if notify and notify != True:
            format = format.replace("{message}", "{extra[notify]}")
        return "{level}#" + format

    accounts = config.get("telegram", [])
    notifier = config.get("notifier", None)
    if notifier:
        try:
            if notifier == True:
                notifier = accounts[0]
            elif isinstance(notifier, int):
                notifier = accounts[notifier + 1]
            elif isinstance(notifier, str):
                for a in accounts:
                    if a["phone"] == notifier:
                        notifier = a
                        break
            else:
                notifier = None
        except IndexError:
            notifier = None
    if notifier:
        logger.info(f'计划任务的关键消息将通过 Embykeeper Bot 发送至 "{notifier["phone"]}" 账号.')
        logger.add(
            TelegramStream(
                account=notifier, proxy=config.get("proxy", None), basedir=config.get("basedir", None)
            ),
            format=_formatter,
            filter=_filter,
        )
