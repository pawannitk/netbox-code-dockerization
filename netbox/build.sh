#!/bin/bash
# This script will prepare NetBox to run after the code has been upgraded to
# its most recent release.

# This script will invoke Python with the value of the PYTHON environment
# variable (if set), or fall back to "python3". Note that NetBox v4.0+ requires
# Python 3.10 or later.

cd "$(dirname "$0")"

NETBOX_VERSION="$(grep ^VERSION netbox/netbox/settings.py | cut -d\' -f2)"
echo "You are installing (or upgrading to) NetBox version ${NETBOX_VERSION}"

PYTHON="${PYTHON:-python3}"

# Validate the minimum required Python version
COMMAND="${PYTHON} -c 'import sys; exit(1 if sys.version_info < (3, 10) else 0)'"
PYTHON_VERSION=$(eval "${PYTHON} -V")
eval $COMMAND || {
  echo "--------------------------------------------------------------------"
  echo "ERROR: Unsupported Python version: ${PYTHON_VERSION}. NetBox requires"
  echo "Python 3.10 or later. To specify an alternate Python executable, set"
  echo "the PYTHON environment variable. For example:"
  echo ""
  echo "  sudo PYTHON=/usr/bin/python3.10 ./upgrade.sh"
  echo ""
  echo "To show your current Python version: ${PYTHON} -V"
  echo "--------------------------------------------------------------------"
  exit 1
}
echo "Using ${PYTHON_VERSION}"

# Install necessary system packages
COMMAND="pip install --upgrade pip wheel"
echo "Updating pip and installing wheel ($COMMAND)..."
eval $COMMAND || exit 1

# Install required Python packages
COMMAND="pip install -r requirements.txt"
echo "Installing core dependencies ($COMMAND)..."
eval $COMMAND || exit 1

# Install optional packages (if any)
if [ -s "local_requirements.txt" ]; then
  COMMAND="pip install -r local_requirements.txt"
  echo "Installing local dependencies ($COMMAND)..."
  eval $COMMAND || exit 1
elif [ -f "local_requirements.txt" ]; then
  echo "Skipping local dependencies (local_requirements.txt is empty)"
else
  echo "Skipping local dependencies (local_requirements.txt not found)"
fi




