# `python-telegram-bot` with redis

## Why?

![To measure my abilities](static/to_measure_my_abilities.png)

But also because I wanted to make it possible to run multiple container instances of the bot,
while having them handle conversations. This requires storing all the conversation states and
context data in some external storage like Redis, not a local `dict`.

## Why not built-in persistence?

Read about persistence here: [Making your bot persistent](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Making-your-bot-persistent).

In `python-telegram-bot`, data is only pushed and pulled from the persistence storage of choice
*in intervals*. This means that an `asyncio.Task` that updates data is run every time. Setting an
interval to a small number of seconds might add too much workload for the bot, or tasks can overlap.

Even with persistence, all the data is still stored in the `Application` or a `ConversationHandler`
instance, but synced with an external storage. So I thought that it's probably easier to just write
and read directly from a database.

## How to run

Clone the repo and run `docker compose up`.

After making changes to the bot, you can restart it with `docker compose restart telegram-bot`. New changes will be applied thanks to a mount volume in `docker-compose.yaml`.
