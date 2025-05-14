from telegram import Update
from telegram.ext import ContextTypes
from db.todo_db import add_todo, list_todos, complete_todo
from services.logger import setup_logger
from decorators import forwarded

# Replace this with your actual topic ID
TOPIC_ID = 2
logger = setup_logger(__name__)

async def todo_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    todos = list_todos()
    logger.info(f"TODOs: {todos}")
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

async def complete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        todo_id = int(context.args[0])
        complete_todo(todo_id)
        logger.info(f"Marked TODO {todo_id} as complete.")
        await update.message.reply_text(f"✅ Marked TODO {todo_id} as complete.")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /done <id>")

@forwarded.forwarded_only
async def check_forwarded_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if msg and msg.is_topic_message and msg.message_thread_id == TOPIC_ID:
        content = msg.text or msg.caption or "<no text content>"
        add_todo(content)
        logger.info(f"Added TODO: {content}")
        await msg.reply_text("🆕 Forwarded message added to TODO list!")

