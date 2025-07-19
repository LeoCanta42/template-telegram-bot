from collections import defaultdict
from decimal import Decimal

def simplify_debts(transactions):
    balance = defaultdict(Decimal)

    for t in transactions:
        payer = t["payer"]
        payee = t["payee"]
        amount = Decimal(str(t["amount"]))
        balance[payer] -= amount
        balance[payee] += amount

    creditors = []
    debtors = []

    for person, bal in balance.items():
        if bal > 0:
            creditors.append((person, bal))
        elif bal < 0:
            debtors.append((person, -bal))

    simplified = []
    i, j = 0, 0

    while i < len(debtors) and j < len(creditors):
        debtor, d_amt = debtors[i]
        creditor, c_amt = creditors[j]
        amount = min(d_amt, c_amt)

        simplified.append({
            "from": debtor,
            "to": creditor,
            "amount": float(round(amount, 2))
        })

        d_amt -= amount
        c_amt -= amount

        if d_amt == 0:
            i += 1
        else:
            debtors[i] = (debtor, d_amt)

        if c_amt == 0:
            j += 1
        else:
            creditors[j] = (creditor, c_amt)

    return simplified
