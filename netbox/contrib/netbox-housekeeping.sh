#!/bin/sh
# This shell script invokes NetBox's housekeeping management command, which
# intended to be run nightly. This script can be copied into your system's
# daily cron directory (e.g. /etc/cron.daily), or referenced directly from
# within the cron configuration file.
#
# If NetBox has been installed into a nonstandard location, update the paths
# below.
SLEEP_SECONDS=${HOUSEKEEPING_INTERVAL:=86400}
echo "Interval set to ${SLEEP_SECONDS} seconds"
while true; do
  date
  python /opt/netbox/netbox/manage.py housekeeping
  sleep "${SLEEP_SECONDS}s"
done 