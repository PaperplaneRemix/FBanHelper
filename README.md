# FBanHelper
Helps fed admins deal with their bans easily!

Local config:

`fban_admin_chats` under [userbot] category, put comma between chat IDs

Heroku var:

`ext_userbot_fban_admin_chats` put space between chat IDs

## Usage of this module:

* Fban in reply:

`fban r:<reason>` will use replied user's ID and message (as proof) to fban.

* Fban in reply with user:

`fban <user> r:<reason>` will use replied message (as proof) and gonna fban the specified user.

* Fban multiple users at once:

`fban <user1> <user2> <userx> r:<reason>` will fban all the users at once.

```
Notes:
1. In case if you're a noob (it's not a bad), remove <> and fill them with needed stuff.
2. Unfbanning is same just put 'un' right before fban; unfban <user> r:<reason>.
3. Replied messages will be sent to fban admin chats.
4. r: is shortuct of reason, if reason is more than a word, use r:'<reason>'
5. User should be in redis db, mention the user (or use username if exists) to guarantee un/fbanning.
6. if 5th has met, user's ID will be sent mentioned to make sure Rose'll know the un/fbanned user(s)
```
