About

In TF2 items are dropped for players every hour or so, with a weekly limit on the number of items that can drop. This has led to people creating idling accounts to collect their drops for the week. TF2 Drop Monitor is a python script that monitors your TF2 accounts for new drops. It does so via polling using the Steam web API. It makes checking your loot an easy process, since everything is nicely laid out. You don't have to check each account's backpack individually.
Installation

TF2DropMonitor is available on GitHub. First you need to clone a copy to your local machine.
> git clone https://github.com/wryyl/TF2DropMonitor
Configuration

Next edit TF2DropMonitor.ini. 
accounts is a comma-separated list of your accounts you wish to monitor.
api_key is your Steam API key. You can get your key here.
poll_minutes defines the frequency of checks done in minutes.
logging defines whether to log your drops or not. 1 to enable logging.
html_dir is the directory to which the html output will be generated. This can be a relative or absolute path. Remember that style.css and the base index.html provided in the output folder has to be in the directory you choose.
[General]
accounts=account1,account2,account3
api_key=YOUR_API_KEY
poll_minutes=3
logging=0
html_dir=output

Once all this is configured, you simply have to run the TF2DropMonitor.py
chmod u+x TF2DropMonitor.py
./TF2DropMonitor.py

Something I also did was make an init script. Here's mine:
#!/bin/bash
# tf2drops daemon
# chkconfig: 345 82 22
# description: Monitors TF2 idle accounts for new drops.
# processname: tf2drops

DAEMON_PATH="/scripts/TF2DropMonitor"

DAEMON="/scripts/TF2DropMonitor/TF2DropMonitor.py"

NAME=tf2drops
DESC="Monitors TF2 idle accounts for new drops."
PIDFILE=/var/run/$NAME.pid
SCRIPTNAME=/etc/init.d/$NAME

case "$1" in
start)
    printf "%-50s" "Starting $NAME..."
    cd $DAEMON_PATH
    PID=`$DAEMON > /dev/null 2>&1 & echo $!`
    #echo "Saving PID" $PID " to " $PIDFILE
        if [ -z $PID ]; then
            printf "%s\n" "Fail"
        else
            echo $PID > $PIDFILE
            printf "%s\n" "Ok"
        fi
;;
status)
        printf "%-50s" "Checking $NAME..."
        if [ -f $PIDFILE ]; then
            PID=`cat $PIDFILE`
            if [ -z "`ps axf | grep ${PID} | grep -v grep`" ]; then
                printf "%s\n" "Process dead but pidfile exists"
            else
                echo "Running"
            fi
        else
            printf "%s\n" "Service not running"
        fi
;;
stop)
        printf "%-50s" "Stopping $NAME"
            PID=`cat $PIDFILE`
            cd $DAEMON_PATH
        if [ -f $PIDFILE ]; then
            kill -HUP $PID
            printf "%s\n" "Ok"
            rm -f $PIDFILE
        else
            printf "%s\n" "pidfile not found"
        fi
;;

restart)
    $0 stop
    $0 start
;;

*)
        echo "Usage: $0 {status|start|stop|restart}"
        exit 1
esac

Edit the path variables at the top then save it to /etc/init.d/tf2drops. Now all you have to do is run service tf2drops start or /etc/init.d/tf2drops start to run TF2DropMonitor as a service.

