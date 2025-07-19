from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from decimal import Decimal
from db.money_db import insert_transaction, get_all_transactions
from utils.money_simplify import simplify_debts

async def money_count_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if ',' not in text or 'EUR' not in text:
        return  # not a valid transaction format

    parts = [p.strip() for p in text.split(',')]
    if len(parts) < 3:
        await update.message.reply_text("Use: Person1 , 50.5 EUR , Person2 , Description (optional)")
        return

    try:
        payer = parts[0]
        amount = Decimal(parts[1].replace('EUR', '').strip())
        payee = parts[2]
        description = ""
        if len(parts) > 3:
            description = parts[3]
    except Exception:
        await update.message.reply_text("Couldn't parse input. Use: Anna , 10.5 EUR , Bob")
        return

    # Save to DB
    insert_transaction(payer, payee, float(amount), description)

    # Load & simplify
    all_transactions = get_all_transactions()
    simplified = simplify_debts(all_transactions)

    # Format response
    msg = "*💰 Simplified Debts:*\n"
    if not simplified:
        msg += "_Everyone is settled!_\n"
    else:
        for row in simplified:
            msg += f"{row['from']} ➡️ {row['to']}: {row['amount']} EUR\n"

    msg += "\n*📜 Transaction History:*\n"
    for t in all_transactions:
        msg += f"{t['payer']} → {t['payee']}: {t['amount']} EUR | {t['description']}\n"

    await update.message.reply_text(msg, parse_mode='Markdown')
