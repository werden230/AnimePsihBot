# AnimePsihBot
Bot which can send random anime from shikimori.one
You can check this bot [here](https://t.me/animepsih993_bot)
## Anime database
This bot uses JSON database which I scraped by myself. Maybe later I'll add feature to get anime directly from Shikmori or MyAnimeList website. 
## User data database
Here I use pyMongo module. If you want to use it, check the tutorial how to set up free MongoDB database and paste your token into config.py
## Commands
- /start - start bot, create new user in the database.
- /info - useless information for those who cares.
- /roll - get random anime.
- /filter - setup filters (anime rating, type and genre).
- /cancel - stop setting up filters. 
- /reset - reset filters.
- /favs - get the favourites list.
- /stat - get the number of times you've used /roll command.
## How to setup the bot:
1. Get your bot token from @BotFather
2. Setup your database using MongoDB and get the token
3. Insert both tokens into config.py
4. You are breathtaking!
