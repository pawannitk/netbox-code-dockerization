
# Netbox code dockerization
This is netbox code dockerization repo, here netbox version 4.0.3-dev is being used.
In the netbox-docker repo we can not make own changes to the netbox code as the image is fix so I created a simple dockerization of netbox code.
The new version of netbox can also be used by pulling the latest changes as there is no or minimal changes to exisiting netbox structure.

I have added the database, redis and cache configuration that can be imported from env variables

You need to do the following steps to run the container and create the image

**STEPS TO SETUP**
clone this repository in your local system then navigate to the root folder where docker-compose file is located then run the following command-

1. docker-compose up -d  (make sure docker and docker-compose is already installed in your system)
   
This command will create the image for netbox and use it in netbox, netbox-worker, netbox-housekeepin and pull the image for postgres, redis
This will create the containers in default docker network.
You can see the logs of netbox container using

2. docker-compose logs -f netbox
   
Netbox container will take some time(probably 5 minutes) to get healthy as there are multiple commands running in startup.sh file, you can change that to reduce the time.
Your netbox container is now running, you can access the netbox on http://localhost:8002

You need to create superuser for netbox before loging in to netbox
to create the netbox user run the following command in folder where docker-compose.yml file is located 

3.docker-compose exec netbox /opt/netbox/netbox/manage.py createsuperuser

Thank You
