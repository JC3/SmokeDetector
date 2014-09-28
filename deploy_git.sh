git pull origin master
autostartscript="nocrash.sh"
startPID=pgrep -f $autostartscript
pkill -P $startPID
pkill -f $autostartscript
python $autostartscript
