# `python-telegram-bot` with redis

## Why?

![To measure my abilities](static/to_measure_my_abilities.png)

But also because I wanted to make it possible to run multiple container instances of the bot,
while having them handle conversations. This requires storing all the conversation states and
context data in some external storage like Redis, not a local `dict`.

## Why not persistence?

In `python-telegram-bot`, data is only pushed and pulled from the persistence storage of choice
in intervals. This means that an `asyncio.Task` that updates data is run every time. Setting an
interval to a small number of seconds might add too much workload for the bot.

Even with persistence, all the data is still stored in the `Application` or a `ConversationHandler`
instance, but synced with an external storage. So I thought that it's probably easier to just write
and read directly from a database.
