[INFORMATION]
TF2DropMonitor monitors the inventories of specified accounts for new items. The new items are then written to a html file for easy viewing. The primary purpose of TF2DropMonitor is to allow you to easily view what your idle accounts have found.

It is written in python and the source code is available for you to freely edit, adapt and redistribute. The python library 'steamodd' is used to interact with Steam.


------------------------------------------------------------------
[CONFIGURATION]
Configuration file: TF2DropMonitor.ini

accounts: A list of steamIDs to monitor, separated by commas. The steamIDs must correspond to the custom URL of the account. For instance, if my profile is 'http://steamcommunity.com/id/wryyl', then my steamID is 'wryyl'. The custom URL can be set by editing your steam profile.
    Example: account1,account2,account3

api_key: Your API key. You can get your key at 'http://steamcommunity.com/dev/apikey'. Just enter 'google.com' or something as your domain name. This is needed to retrieve backpack information.
    Example: B8BF6FDG536JLK2AB1BD8184E88MB2C9

poll_minutes: The number of minutes to wait before each inventory check.
    Recommended: 3

logging: Whether to log your drops to a file or not.
    '1' to enable, '0' to disable.

html_dir: Path to where you want to generate the html in. The html will be generated in index.html in this directory.


------------------------------------------------------------------
[NOTES]
In the directory specified by the html_dir variable, ensure that you have the base index.html and style.css inside.

You can set the script to write index.html to your webserver, thereby allowing you to view your item drops online.
