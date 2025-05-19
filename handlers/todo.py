from telegram import Update
from telegram.ext import ContextTypes
from db.todo_db import add_todo, list_todos, complete_todo
from services.logger import setup_logger
from decorators.decorators import forwarded_only, topic_only, reply_only, auto_delete_message, reply_only_in_topic

# Replace this with your actual topic ID
TOPIC_ID = 2
logger = setup_logger(__name__)

async def todo_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    todos = list_todos()
    logger.debug(f"TODOs: {todos}")
    pending = [todo for todo in todos if not todo['is_done']]
    done = [todo for todo in todos if todo['is_done']]

    text_parts = ["📝 <b>Your TODO List</b>\n"]

    if pending:
        text_parts.append("📌 <b>Pending:</b>")
        text_parts += [f"• {todo['message']}" for todo in pending]
    else:
        text_parts.append("📌 <b>Pending:</b>\n(none)")

    if done:
        text_parts.append("\n✅ <b>Done:</b>")
        text_parts += [f"✅ {todo['message']}" for todo in done]

    await update.message.reply_text("\n".join(text_parts), parse_mode="HTML")

@reply_only_in_topic(TOPIC_ID)
async def complete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    content = msg.text

    if content and content.startswith("/complete"):
        complete_todo(msg.reply_to_message.message_id)
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=msg.reply_to_message.message_id)

    return True

@topic_only(TOPIC_ID)
@forwarded_only
async def check_forwarded_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    content = msg.text or msg.caption or "<no text content>"

    # Step 1: Send new structured TODO message
    sent_msg = await context.bot.send_message(
        chat_id=msg.chat_id,
        text=f"🆕 TODO:\n{content}",
        message_thread_id=TOPIC_ID,
        parse_mode="Markdown"
    )

    # Step 2: Store new message ID
    add_todo(content, sent_msg.message_id)
    logger.debug(f"Added TODO: {content} (Bot Msg ID: {sent_msg.message_id})")

    return True


@topic_only(TOPIC_ID)
@auto_delete_message
async def delete_messages_sent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return True
