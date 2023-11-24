# HiveInteractiveMenu
Startup file should be PwndMonstersBotClient.py

Very little error catching in place at the moment

For the bot to run you need to install the link with proper permissions created in the discord bot configuration section.  
All names currently match my guild - you can edit if you need to.

You will need to add a new channel with a channel name matching the .env channel name attribute
Bot token and keys need to be added to the .env file.
Bot will only respond to commands in the specified channel. Type !help to see commands and !help *** command name for more details.

DEV - to get git to ignore the .env file if/when you put your keys in
Run "git update-index --skip-worktree .env"
This eliminates tracking of the env file so it will not push your keys into the repo
To undo: "git update-index --no-skip-worktree .env"