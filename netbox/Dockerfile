# Use a base image with Python 3
FROM python:3.10

# Install required system packages
RUN apt-get update && apt-get install -y \
    python3-pip python3-venv python3-dev build-essential libxml2-dev \
    libxslt1-dev libffi-dev libpq-dev libssl-dev zlib1g-dev

# Create a system user for NetBox
RUN adduser --system --group netbox

# Set the working directory
WORKDIR /opt/netbox

# Copy the NetBox source code into the container
COPY . /opt/netbox

# Change ownership of the media, reports, and scripts directories
RUN chown --recursive netbox /opt/netbox/netbox/media/ && \
    chown --recursive netbox /opt/netbox/netbox/reports/ && \
    chown --recursive netbox /opt/netbox/netbox/scripts/

# #for netbox topology views images
RUN mkdir -p /opt/netbox/netbox/static/
RUN chown -R netbox:netbox /opt/netbox/netbox/static/


# Copy and set up the startup script
COPY startup.sh /opt/netbox/startup.sh
RUN chmod +x /opt/netbox/startup.sh
COPY build.sh /opt/netbox/build.sh
RUN chmod +x /opt/netbox/startup.sh

RUN /opt/netbox/build.sh

CMD ["/opt/netbox/startup.sh"]