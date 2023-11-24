PWND Monsters Bot README

Current design has the bot running on my machine. If the PwndMonsterBot user shows as Active then it is running. The data is stored in two text files on my machine.

balances.txt shows the current users name and point balance, that's it. This can be retrieved with the !display_All or !display_Name commands. This file is overwritten each time a point value is changed. Always has the current balance and that is it.
changelog.txt has a 'blockchain' style log of any changes to anybody's score for any reason. hopefully if we lose the balances file for some reason this will help debug/restore the points.  To view the changelog you can use the !change_Log messages.  Currently an issue if the message is more than 21 lines it will not display.  You can specify a line count or username and line count. If we have a serious problem and lose both files at once somehow then hopefully we can reconstruct based on the messages saved in the pwnd-bot channel.

!add_Brawl ## will locate the correct brawl data and add points based on the algorithm to the user.
!remove_Brawl ## is identical but adds negative points
	This method also will NOT give any points to players whose 'entered_battles' is 0. Haven't tested this yet but hopefully it works. I added a line to send a message calling this out and that message should ping idk also.
!add_Points @name ## will increase or decrease (neg value) a specific user's points by the requested amount

For now if we want to run with this version we can, will just need an officer to use the !add_Points to decrease a member's points when the 'buy' a reward.

I plan to add commands to automate spending points so the whole thing is hands-off for us, but to distribute rewards automatically the bot will need the active keys for the reward account which is an OPSEC question for you and Moertoe if you want.
Alternatively I can make the bot deduct points and send a message to Moertoe with the requested purchase for him to send manually like he does now.