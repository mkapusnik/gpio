#!/bin/sh

case "$1" in
  start)
     python /home/pi/api/api.py
   ;;
  stop)
   ;;
  force-reload|restart)
   ;;
  status)
   ;;
 *)
   echo "Usage: /etc/init.d/atd {start|stop|restart|force-reload|status}"
   exit 1
  ;;
esac

exit 0