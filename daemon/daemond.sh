#!/bin/sh

case "$1" in
  start)
     python ./daemon.py
   ;;
  stop)
   ;;
  force-reload|restart)
   ;;
  status)
   ;;
 *)
   echo "Usage: /etc/init.d/daemond {start|stop|restart|force-reload|status}"
   exit 1
  ;;
esac

exit 0
