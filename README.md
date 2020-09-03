<h2>Description of the bot</h2>

This Bot checks your followers in social network Twitter and then everyday sends you a message, if someone starts following or unfollows you.

<h3>Content description</h3>

<b>bot.py</b> - main script. Consists of functions, that describe interaction with user, as well as scheduling function;

<b>get_followers.py</b> - returns a list of current followers;

<b>check_followers.py</b> - gets response from get followers function and compares it with an old list. Returns lists of new followers and unfollowers, if any;

<b>save_followers.py</b> - saves followern in json-file.

<b>add_to_user_list.py</b> - adds new user to the list;

<b>delete_user.py</b> - function to delete user from base;

<b>list_of_users.json</b> - json file with all users;

<b>requirements.txt</b> - requirements to install.

