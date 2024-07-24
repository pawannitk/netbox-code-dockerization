#!/bin/bash
# This script will prepare NetBox to run after the code has been upgraded to
# its most recent release.

# This script will invoke Python with the value of the PYTHON environment
# variable (if set), or fall back to "python3". Note that NetBox v4.0+ requires
# Python 3.10 or later.
# You can remove some of the commands if not needed 

cd "$(dirname "$0")"

NETBOX_VERSION="$(grep ^VERSION netbox/netbox/settings.py | cut -d\' -f2)"
echo "You are installing (or upgrading to) NetBox version ${NETBOX_VERSION}"

PYTHON="${PYTHON:-python3}"


# Apply any database migrations
COMMAND="python netbox/manage.py migrate"
echo "Applying database migrations ($COMMAND)..."
eval $COMMAND || exit 1

# Trace any missing cable paths (not typically needed)
COMMAND="python netbox/manage.py trace_paths --no-input"
echo "Checking for missing cable paths ($COMMAND)..."
eval $COMMAND || exit 1

# Build the local documentation
COMMAND="mkdocs build"
echo "Building documentation ($COMMAND)..."
eval $COMMAND || exit 1

# Collect static files
COMMAND="python netbox/manage.py collectstatic --no-input"
echo "Collecting static files ($COMMAND)..."
eval $COMMAND || exit 1

# Delete any stale content types
COMMAND="python netbox/manage.py remove_stale_contenttypes --no-input"
echo "Removing stale content types ($COMMAND)..."
eval $COMMAND || exit 1

# Rebuild the search cache (lazily)
COMMAND="python netbox/manage.py reindex --lazy"
echo "Rebuilding search cache ($COMMAND)..."
eval $COMMAND || exit 1

# Delete any expired user sessions
COMMAND="python netbox/manage.py clearsessions"
echo "Removing expired user sessions ($COMMAND)..."
eval $COMMAND || exit 1

echo "Upgrade complete!"

COMMAND="python netbox/manage.py runserver 0.0.0.0:8080 --insecure"
echo "Running server with  ($COMMAND)..."
eval $COMMAND || {
  echo "running server failed"
}