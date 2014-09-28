git pull origin master
autostartscript="nocrash.sh"
startPID=pgrep $autostartscript
pkill -P $startPID
pkill $autostartscript
python $autostartscript
