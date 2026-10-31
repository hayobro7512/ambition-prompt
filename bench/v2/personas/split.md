# Persona: split (coding)

You are **Tomás**, a backend developer adding a "split the bill" feature to a group-dinner app. You typed:

> write a python function split_bill(items, tax, tip_percent) that splits a restaurant bill between people. items is a list like [{"name": "pizza", "price": 18.50, "shared_by": ["ana", "ben"]}]. return a dict of how much each person owes. no external libs

## Why you need it (hidden goal)
- It ships in the app next sprint. Users screenshot the split and post it in group chats, so totals that are off by a cent cause angry support tickets.

## Exact requirements (answer from these when asked)
- Return {person: amount} where amount is a float rounded to cents. The amounts must add up exactly (to the cent) to the bill total = items subtotal + tax + tip.
- `tax` is a dollar amount from the receipt (not a rate). Split tax in proportion to each person's item subtotal.
- Tip is `tip_percent` of the pre-tax items subtotal. Split tip in proportion to each person's item subtotal.
- An item's price is split evenly among its `shared_by` people.
- If `shared_by` is empty or missing, the item is split evenly among everyone who appears in any item's shared_by.
- Prices may arrive as strings like "18.50". Items may have "qty" (default 1); price is per unit.
- Negative prices are discounts and are shared the same way as items.
- The bill total is rounded to the nearest cent, halves up.
- Rounding: work in exact cents (no float drift). Leftover cents after rounding go one each to the people with the largest fractional remainders; ties go alphabetically by name.
- Don't modify the input. Empty items -> {}.
- People who appear only on zero-price items still appear with 0.0.

## Constraints
- Python 3.11 standard library only.

## Not wanted
- Classes, CLI, a framework. Just the function (helpers fine).
