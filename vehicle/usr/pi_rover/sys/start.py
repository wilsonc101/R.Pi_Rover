DAEMON_1="/usr/pi_rover/app/pi_rover"
PIDFILE_1="/var/run/pi_rover.pid"

case "$1" in
  start)
    echo "Preparing GPS...."
    /usr/bin/killall gpsd
    /usr/sbin/gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock -n
    echo "....done"

    echo "Starting Pi Rover...."
    /sbin/start-stop-daemon --start --pidfile $PIDFILE_1 -b --make-pidfile --exec $DAEMON_1
    echo "....done"
    ;;

  stop)
    echo "Stopping Pi Rover...."
    /sbin/start-stop-daemon --stop --pidfile $PIDFILE_1
    echo "....done"
    ;;

  restart)
    echo "Stopping Pi Rover...."
    /sbin/start-stop-daemon --stop --pidfile $PIDFILE_1
    echo "....done"

    sleep 2s
    
    echo
    echo "Starting Pi Rover...."
    /sbin/start-stop-daemon --start --pidfile $PIDFILE_1 -b --make-pidfile --exec $DAEMON_1
    echo "....done"
    ;;




  *)
    echo "Usage: /etc/init.d/pi_rover {start|stop|restart}"
    exit 1
    ;;





esac

exit 0
