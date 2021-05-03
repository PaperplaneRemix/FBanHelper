# FBan Helper Extension for PaperplaneRemix.
# Copyright (C) 2020 Avinash Reddy <https://github.com/AvinashReddy3108>

import asyncio
from userbot import client, LOGGER
from userbot.utils.events import NewMessage
from userbot.utils.helpers import get_chat_link

plugin_category = "fedadmin"

# Dictionary for holding success messages based on bot's ID.
success_toasts = {609517172: ["New FedBan", "FedBan Reason update", "has already been fbanned", "New un-FedBan"]}


@client.onMessage(
    command=("fban", plugin_category), outgoing=True, regex=r"fban(?: |$|\n)([\s\S]*)"
)
async def fban(event: NewMessage.Event) -> None:
    """
    Fban a user in all your feds.


    `{prefix}fban` in reply or **{prefix}fban user1 user2 [kwargs]**
        **Arguments:** `r`
    """
    match = event.matches[0].group(1)
    args, kwargs = await client.parse_arguments(match)
    reason = kwargs.get("r", None)
    skipped = {}
    fbanned = []
    failed = []

    fban_admin_chats_list = client.config["userbot"].get("fban_admin_chats", None)
    if not fban_admin_chats_list:
        await event.answer(
            "`Atleast one fedadmin chat should be set up for this to work!`"
        )
        return

    fban_admin_chats = set(int(x) for x in fban_admin_chats_list.split(","))

    if not args and event.reply_to_msg_id:
        reply = await event.get_reply_message()
        args.append(reply.sender_id)
    if not args:
        await event.answer("`At least specifiy a user, maybe?`")
        return

    entity = await event.get_chat()
    for chat in fban_admin_chats:
        if event.reply_to_msg_id:
            reply = await event.get_reply_message()
            await reply.forward_to(chat)
        for user in args:
            if isinstance(user, list):
                continue
            try:
                async with client.conversation(chat) as conv:
                    spammer = await client.get_entity(user)
                    await conv.send_message(
                        f'/fban [{spammer.id}](tg://user?id={spammer.id}){" " + reason if reason else ""}'
                    )
                    resp = await conv.get_response()
                    LOGGER.debug(f"FBan: {resp.text}")
                    await client.send_read_acknowledge(conv.chat_id, resp)
                    if resp.sender_id in success_toasts and any(
                        success_toast in resp.message
                        for success_toast in success_toasts[resp.sender_id]
                    ):
                        fbanned.append(user)
                        await asyncio.sleep(0.3)
                    else:
                        failed.append(chat)
                        skipped.update({str(user): failed})
                        continue
            except Exception as error:
                LOGGER.debug(f"FBan failed: {error}")
                failed.append(chat)
                skipped.update({str(user): failed})
    if fbanned:
        text = f"`Successfully FBanned:`\n"
        text += ", ".join((f"`{user}`" for user in fbanned))
        if reason:
            text += f"\n`Reason:` `{reason}`"
        e2 = await get_chat_link(entity, event.id)
        log_msg = text + f"\n`Chat:` {e2}"
        await event.answer(text, log=("fban", log_msg))
    if skipped:
        text = "`Failed FBan requests:`\n"
        text += "\n".join(
            (
                f"`{user}: [{', '.join(str(x) for x in feds)}]`"
                for user, feds in skipped.items()
            )
        )
        await event.answer(text, reply=True)

@client.onMessage(
    command=("unfban", plugin_category), outgoing=True, regex=r"unfban(?: |$|\n)([\s\S]*)"
)
async def unfban(event: NewMessage.Event) -> None:
    """
    Unfban a user in all your feds.


    `{prefix}unfban` in reply or **{prefix}unfban user1 user2 [kwargs]**
        **Arguments:** `r`
    """
    match = event.matches[0].group(1)
    args, kwargs = await client.parse_arguments(match)
    reason = kwargs.get("r", None)
    skipped = {}
    unfbanned = []
    failed = []

    fban_admin_chats_list = client.config["userbot"].get("fban_admin_chats", None)
    if not fban_admin_chats_list:
        await event.answer(
            "`Atleast one fedadmin chat should be set up for this to work!`"
        )
        return

    fban_admin_chats = set(int(x) for x in fban_admin_chats_list.split(","))

    if not args and event.reply_to_msg_id:
        reply = await event.get_reply_message()
        args.append(reply.sender_id)
    if not args:
        await event.answer("`At least specifiy a user, maybe?`")
        return

    entity = await event.get_chat()
    for chat in fban_admin_chats:
        if event.reply_to_msg_id:
            reply = await event.get_reply_message()
            await reply.forward_to(chat)
        for user in args:
            if isinstance(user, list):
                continue
            try:
                async with client.conversation(chat) as conv:
                    spammer = await client.get_entity(user)
                    await conv.send_message(
                        f'/unfban [{spammer.id}](tg://user?id={spammer.id}){" " + reason if reason else ""}'
                    )
                    resp = await conv.get_response()
                    LOGGER.debug(f"unfban: {resp.text}")
                    await client.send_read_acknowledge(conv.chat_id, resp)
                    if resp.sender_id in success_toasts and any(
                        success_toast in resp.message
                        for success_toast in success_toasts[resp.sender_id]
                    ):
                        unfbanned.append(user)
                        await asyncio.sleep(0.3)
                    else:
                        failed.append(chat)
                        skipped.update({str(user): failed})
                        continue
            except Exception as error:
                LOGGER.debug(f"unfban failed: {error}")
                failed.append(chat)
                skipped.update({str(user): failed})
    if unfbanned:
        text = f"`Successfully unfbanned:`\n"
        text += ", ".join((f"`{user}`" for user in unfbanned))
        if reason:
            text += f"\n`Reason:` `{reason}`"
        e2 = await get_chat_link(entity, event.id)
        log_msg = text + f"\n`Chat:` {e2}"
        await event.answer(text, log=("unfban", log_msg))
    if skipped:
        text = "`Failed unfban requests:`\n"
        text += "\n".join(
            (
                f"`{user}: [{', '.join(str(x) for x in feds)}]`"
                for user, feds in skipped.items()
            )
        )
        await event.answer(text, reply=True)
