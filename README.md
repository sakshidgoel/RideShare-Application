# RideShare-Application

## Introduction
The objective of the project is to build a Rideshare application with a mini DBaaS system.  
Database-as-a-service is a database service that typically runs on a cloud architecture. Key characteristics are:
  1. Self-service
  2. On-demand
  3. Dynamic
  4. Security
  5. Automation  
  
This project has been broken down into four parts:
  1) Assignment_0
  2) Assignment_1
  3) Assignment_2
  4) Assignment_3
  5) Project

---

## Assignment_0

### Deliverables
The deliverables for this assignment are as follows:
  + Create an Amazon EC2 instance
  + Install a web server on this instance (Apache2/Nginx/Caddy)
  + Create a mock-up web page
  + View this page from a browser (understand public IP/DNS of an instance)
  
### What is Amazon EC2?
Amazon Elastic Compute Cloud (EC2) is a web service that provides resizable compute capacity in the cloud. Once can use it to launch as many or as few virtual servers as they need, configure security and networking, and manage storage. It’s designed to make web-scale computing easier for developers.

### What is an EC2 instance?
An instance is a virtual server which can be rented by a subscriber/user and can be used to deploy various applications. The instances are charged per hour with different rates based on the type of the instance chosen. These instances can be terminated when they are not needed anymore.

### Launching an instance
1) Create an AWS account and log in to it.
2) On clicking on the 'AWS Educate Starter Account', a new page will be loaded.
3) Click on the 'AWS Console' button.
4) On this page, open the 'All services' tab and select EC2 under it.
5) Make sure that the AWS region on the top right corner of the EC2 dashboard is US East (N. Virginia).
6) From the side menu, select Instances.
7) Click on the 'Launch Instance' button and select the 'Ubuntu Server 18.04 LTS' with the 64-bit (x86) specification.
8) Next choose the 'General pupose t2.micro' instance type.
9) You can skip the next three steps by using the default selections.
10) Next, click on review and launch and then launch your instance.
11) On clicking on the 'Launch' option, you'll be asked to create a key pair. Choose to create a new key pair and give a key pair name and download it and store it in a secure and accessible location, as it cannot be downloaded after it is created. (A key pair consists of a public key that AWS stores and a private key file that you store. Together, they allow you to connect to your instance securely).
12) Once it is downloaded, you can click on "Launch Instance" and you'll have your instance ready.

### Connecting to an Instance
You can give the launched instance whatever name you want. To run and connect to the instance, follow the following steps:
1) Click on the instance and then open the 'Actions' dropdown tab.
2) Select Instance State and then click on 'Start'. It takes few minutes for your instance to start running.
3) Next click on the connect button on top and you'll get a command which looks like the following:  
```ssh -i "rides.pem" ubuntu@ec2-3-214-71-187.compute-1.amazonaws.com```
4) Open your command prompt in the location that has your private .pem file and paste your command and run it. 
5) You will be logged in onto your instance, where you can launch your application and use it like any other ubuntu machine.

### Public IP vs Elastic IP
  + Public IP addresses are dynamic, i.e. if you start/stop your instance, it gets reassigned a new piblic IP each time. 
  + Elastic IP addresses are allocated to your account and stay the same, which can be attached to an instance. They are also considered as static public IP addresses.

### Setting an Elastic IP for an instance
1) Under Network and security, click Elastic IPs
2) In the loaded screen, click on Allocate Elastic IP address and then choose the Amazon's pool of IPv4 address radio button.
3) Once a new IPv4 address is allocated, check the box for it and open the 'Actions' dropdown to choose 'Associate Elastic IP address'.
4) In the 'Resource type', choose Instance and choose the instance you want to associate this ipv4 address with from the dropdown on the Instance field.
5) If you have any other Elastic IP address assigned to this instance before and you need to re-associate, you have to enable the checkbox of 'Reassociation'.
6) Click Associate and a new elastic IPv4 will be assigned to your instance.

---

## Assignment_1

In this portion of the development, our main focus is on completing the backend processing of _RideShare_ using REST APIs on the AWS instance, using Flask. When creating items on the AWS instance, we will be storing it in an SQLite database, using SQLAlchemy. We must deploy the flask application on an application server like gunicorn which runs on top of a web server like nginx using wsgi.

### Deliverables
  + At the end of our development, our application should be able to: 
      1. Add a new user
      2. Delete an existing user
      3. Create a new Ride
      4. Search for an existing ride between a source and a destination
      5. Join an existing ride
      6. Delete a ride
  + Each one of the APIs mentioned below must be implemented with proper status codes.
  + These APIs must be exposed on the public IP address, i.e. deployed on AWS with a static IP on port 80.
  + Deploying a reverse proxy and app server, automated testing, load testing.

### What is Flask?
  + Flask is a web framework. This means flask provides you with tools, libraries, modules and technologies that allow you to build a web application. This web application can be some web pages, a blog, a wiki or a commercial website.
  + It is classified as a microframework because it does not require particular tools or libraries, i.e. it has little to no dependencies to external libraries.

### APIs vs REST APIs
  + API stands for Application Program Interface and is basically a set of routines, protocols and tools for building software applications that allow one application to access the features of another application, i.e. an API specifies how software components should interact.
  + REST stands for Representational State Transfer and determines how the API looks like. It is an architectural style for networked applications on the web, i.e. it is a set of rules or guidelines to build a web API. It is limited to client-server based applications and is designed to take advantage of existing protocols. 

### SQLite and SQLAlchemy
  + SQLite is a relational database management system, that is ACID-compliant and implements most of the SQL standard, generally following PostgreSQL syntax.
  + SQLAlchemy is a popular SQL related python library, which has been used in this project to access the SQLite3 database system.

### Implemented APIs
1. **Add user:**
    + Route: /api/v1/users
    + HTTP Request Method: PUT
2. **Remove user:**
    + Route: /api/v1/users/{username}
    + HTTP Request Method: DELETE
3. **Create a new ride:**
    + Route: /api/v1/rides
    + HTTP Request Method: POST
4. **List all upcoming rides for a given source and destination:**
    + Route: /api/v1/rides?source={source}&destination={destination} 
    + HTTP Request Method: GET 
5. **List all the details of a given ride:**
    + Route: /api/v1/rides/{rideId} 
    + HTTP Request Method: GET 
6. **Join an existing ride:**
    + Route: /api/v1/rides/{rideId} 
    + HTTP Request Method: POST
7.  **Delete a ride:**
    + Route: /api/v1/rides/{rideId} 
    + HTTP Request Method: DELETE 
8. **Write to DB:**
    + Route: /api/v1/db/write 
    + HTTP Request Method: POST 
9. **Read from DB:**
    + Route: /api/v1/db/read 
    + HTTP Request Method: POST 

---

## Assignment_2

In this assignment, the monolithic application built in assignment 1 is split up into two microservices - one catering the user management and another catering to the ride management. These two microservices should be started in separate docker containers (Users and Rides) running on one AWS instance. The microservices will talk to each other via their respective REST interfaces.

### Users Microservice
The APIs on this microservice are:
1) **Add user** (reused API from assignment 1)
2) **Remove user** (reused API from assignment 1)
3) **List all users:**
    + Route: /api/v1/users
    + HTTP Request Method: GET
4) **Clear db:**
    + Route: /api/v1/db/clear
    + HTTP Request Method: POST

### Rides Microservice
The APIs on this microservice are:
1. **Create a new ride** (reused API from assignment 1)
2. **List all upcoming rides for a given source and destination** (reused API from assignment 1)
3. **List all the details of a given ride** (reused API from assignment 1)
4. **Join an existing rid** (reused API from assignment 1)
5.  **Delete a ride** (reused API from assignment 1)
6. **Clear db:**
    + Route: /api/v1/db/clear
    + HTTP Request Method: POST
    
This miroservice must call the **List all users** API on the Users microservice in order to verify a given username actually exists. (Example: when a ride is being created/joined).

### Deliverables
+ Running two microservices with the given container name ("users" and "rides") and tag ("latest") and ENV variable.
+ Exposing 8000 and 8080 on the public IP of the AWS instance.
    + For the rides microservice, map web server port within the container (usually 80) to localhost 8000.
    + For the users microservice, map web server port within the container (usually 80) to localhost 8080.
+ Implementing and calling the “List all users” API from the “rides” container.

### What is Docker?
Docker is an open platform for developing, shipping, and running applications. Docker enables us to separate our applications from our infrastructure so we can deliver software quickly. With Docker, one can manage their infrastructure in the same ways they manage their applications. By taking advantage of Docker’s methodologies for shipping, testing, and deploying code quickly, one can significantly reduce the delay between writing code and running it in production.

### Docker Images
An image is a read-only template with instructions for creating a Docker container. Often, an image is based on another image, with some additional customization. For example, you may build an image which is based on the ubuntu image, but installs the Apache web server and your application, as well as the configuration details needed to make your application run.

### Docker Containers
+ A container is a runnable instance of an image. You can create, start, stop, move, or delete a container using the Docker API or CLI. You can connect a container to one or more networks, attach storage to it, or even create a new image based on its current state.
+ By default, a container is relatively well isolated from other containers and its host machine. You can control how isolated a container’s network, storage, or other underlying subsystems are from other containers or from the host machine.
+ A container is defined by its image as well as any configuration options you provide to it when you create or start it. When a container is removed, any changes to its state that are not stored in persistent storage disappear.

### Contents of a container folder
1. **Dockerfile:** It is a text file that is used to build the docker image. We will use the ENV parameter in the dockerfile to have the environment variable TEAM_NAME=CC_0139_0148_0905_1736 defined within our containers.
2. **docker-compose.yml:** It is a file that contains the configuration on how many containers to make, what ports to expose, which database, volume to use to externally store the data, etc.
We have one docker-compose file for each microservice.
3. **Database:** Each microservice will have their own database, shared database cannot be used.
4. **requirements.txt:** It contains the required packages that need to be installed in the container image.
5. **AreaNameEnum.csv:** This contains the enums of the localities that constitute the 'source and 'destination' fields in the rides microservice APIs.
5. **app.py:** It includes all the REST APIs and the backend processing part of the application.
6. **Web Server:** If using nginx/apache, each microservice must have their own web server.

---

## Assignment_3

In this section, we have to put the two microservices (containers) into two different AWS EC2 instaces now. Both of them need to be accessible from under the same public IP address and also the same port (80). This is only possible by using a load balancer that supports path-based routing.

### Deliverables
   + Two instances with the two microservices as containers
   + New APIs
   + Setting up the load balancer

### Additional APIs
+ The following API must be added only to the rides instance/microservice:  
    **Get total number of rides:**
     + Route: /api/v1/rides/count
     + HTTP Request Method: GET  

This API will be called on the load balancer public IP and must be routed to the rides instance.
+ The following two APIs must be added to both of the instances/microservices:
  1. **Get total HTTP requests made to microservice:**
      * Route: /api/v1/_count
      * HTTP Request Method: GET
  2. **Reset HTTP requests counter:**
      + Route: /ap1/v1/_count
      + HTTP Request Method: DELETE  

These two APIs above along with the existing **Clear db** APIs will be called on the public IP of each microservice directly and not on the load balancer IP, as these APIs are microservice-specific. Also, API requests should be counted whether they failed or were successful and calls to these two APIs should not be counted towards the HTTP request count returned.

### Load Balancer
A load balancer serves as the single point of contact for clients. The load balancer distributes incoming application traffic across multiple targets, such as EC2 instances, in multiple Availability Zones. This increases the availability of your application. After the load balancer receives a request, it evaluates the listener rules in priority order to determine which rule to apply, and then selects a target from the target group for the rule action.

### Listener
A listener checks for connection requests from clients, using the protocol and port that you configure. You can configure listener rules to route requests to different target groups based on the content of the application traffic. The rules that you define for a listener determine how the load balancer routes requests to its registered targets. Each rule consists of a priority, one or more actions, and one or more conditions. When the conditions for a rule are met, then its actions are performed. You must define a default rule for each listener, and you can optionally define additional rules.

### Target Group
Each target group routes requests to one or more registered targets, such as EC2 instances, using the protocol and port number that you specify. You can register a target with multiple target groups.

### Steps 
1. Create two EC2 instances and make port 22 and 80 accessible for both of them.
2. Place *rides* container in one instamce and the *users* container in the other and make the web servers inside the containers accessible through the public IPs of the instances.
3. The APIs must be ecposed through port 80 of the EC2 instance IP address.
4. Create two AWS target groups, one for each instance.
5. Create an AWS Application Load Balancer with the following rules:
    1. If an incoming request's route matches ```/api/v1/users```, then forward it to the *users* instance using its target group.
    2. For all other routes, forward the request to the *rides* instance using the corresponding target group.
6. Make sure the security group of the load balancer exposes ports 22 and 80 only.
7. When the *rides* instance makes a call to the *users* instance to check if a user exists, the HHTP request from the *rides* instance must have the *Origin* header set to either the public IP address or public DNS name of the *rides* instance and this call must be made over the load balancer.

---

## Project

+ The project is focused on building a fault tolerant, highly available database as a service for the RideShare application. We will continue to use our users and rides VM, their containers, and the load balancer for the application. In addition now, we will enhance our existing DB APIs to provide this service.
+ The db read/write APIs we had written in the first assignment will be used as endpoints for this DBaaS orchestrator. The same db read/write APIs will now be exposed by the orchestrator. These APIs will not be writing to the database themselves, but will just be publishing the requests to the relevant queues.
+ The users and rides microservices will no longer be using their own databases, they will instead be using the “DBaaS service” that we will create for this project. This will be the only change that has to be made to the existing users and rides microservices. Instead of calling the db read and write APIs on localhost, those APIs will be called on the IP address of the database orchestrator.
+ We will implement a custom database orchestrator engine that will listen to incoming HTTP requests from users and rides microservices and perform the database read and write
according to the given specifications.

### Deliverables
   + Master/slave worker
   + Orchestrator
   + Setting up RabbitMQ, with all queues having correct producer and consumer
   + Perform data replica/sync
   + Scale out/in
   + Fault tolerance (slave + master) using Zookeeper with correct znodes and watch

### Steps
1. Implement orchestrator with RabbitMQ
2. Implement replication/sync
3. Demonstrate scale out/in
4. Implement High Availability with Zookeeper

### Architecture of DBaaS
+ **Orchestrator:** 
   + The orchestrator will listen to incoming requests on port 80. 
   + The orchestrator is responsible for publishing the incoming message into the relevant queue and bringing up new worker containers as desired. We will be using **AMQP**(Advanced Message Queue Protocol) using **RabbitMQ** as a message broker for this project. 
+ **Queues:** There will be four message queues named “readQ”, “writeQ”, “syncQ” and “responseQ”:
   + **ReadQ:** All the read requests will be published to the readQ. 
   + **WriteQ:** All the write requests will be published to the writeQ. 
+ **Workers:** There will be two types of workers running on the instance and they will connect to a common rabbitMQ.:
   + The **master worker** will listen to the “writeQ”. It will pick up all incoming messages on the “writeQ” and actually write them to a persistent database. 
   + The **slave worker** is responsible for responding to all the read requests coming to the DBaaS orchestrator, through the "readQ".  
+ **ResponseQ:** Upon querying the database based on the request, the slave will write the output to the “responseQ”, which will then be picked up by the orchestrator, using the right type of exchange and correctly using channels. 
+ **Round-robin message picking:** If there are multiple instances of the worker running, then the messages from the readQ must be picked up by the slave workers in a round robin fashion. 
+ **Eventual Consistency:** Each worker (slave and master) will have its own copy of the database. The database will not be shared among the workers, which creates the problem of maintaining consistency between the various replicas of the same database. 
   + To solve this issue, we will use an “eventual consistency” model, where after a write has successfully been performed by the master worker, it must eventually be consistent with all the slave workers. 
   + For implementing eventual consistency, the master will write the new db writes on the **syncQ** after every write that master does, which will be picked up by the slaves to update their copy of the database to the lastest.  
+ **High Availability:** DBaaS has to be highly available, hence all the workers will be “watched” for failure by zookeeper, a cluster coordination service. (@zk.ChildrenWatch keeps a watch on the children of a root.) 
   + In case of the failure of a slave, a new slave worker will be started. 
   + In case of failure of the master, the existing slave, with the lowest pid of the container they are running in, will be elected as master, using **zookeeper’s leader election**. And upon that, a new slave node will be brought up by the orchestrator.
   + All the data is copied asynchronously to the new worker.
   + All the workers, therefore, must run the same code, as any of them can be elected as the master.
+ **Scalability:** The orchestrator has to keep a count of all the incoming HTTP requests for the db read APIs. The auto scale timer has to begin after receiving the first request. After every two minutes, depending on how many requests were received, the orchestrator must increase/decrease the number of slave worker containers. The counter has to be reset every two minutes.
   +  0 – 20 requests: 1 slave container must be running.
   + 21 – 40 requests: 2 slave containers must be running. 
   + 41 – 60 requests: 3 slave containers must be running and so on. 
+ **New APIs:** The following APIs need to be implemented in the orchestrator and the crash APIs should return 200 OK with message body as <pid-of-container-killed>:
   + **Kill the master worker:** 
      + Route: api/v1/crash/master
      + HTTP Request Method: POST
   + **Kill the slave with highest pid:**
      + Route: api/v1/crash/slave
      + HTTP Request Method: POST
   + **Sorted list of pids' of the containers of all the workers:**
      + Route: api/v1/worker/list
      + HTTP Request Method: GET
+ **Number of Containers:** Initially, we will be running 5 containers, for "zookeeper", "rabbitmq", "orchestrator", "slave" and "master", which will later be increased/decreased accordingly.
+ **Kazoo:** It has states that can help us take actions when the connection has been stopped, restored or when zookeeper session has expired. The kazaoo states are as follows:
   + LOST: when an instance is first created
   + CONNECTED: when the instance gets connected
   + SUSPENDED: when it needs to transition to a new zookeeper.
+ **Replication:** Since there are one master and one slave initially, the databases are consistent. When a new slave is spawned, a shared volume is created. Since docker does not allow transfering of data from one container to another, it writes to the shared volume and then all databases of the various workers sync according to this. So when a new worker starts, it takes a copy of shared volume from the shared database. 

---

## Functionalities implemented
Following are the expected functionalities that need to be implemented:
  1. Queues for message passing
  2. Eventual consistency handled
  3. High availability and fault-tolerance
  4. Scaling 
  5. Orchestrator, worker set up
  6. Rabbitmq, zookeeper usage

---

## Commands
1. Install Flask
```
pip install Flask
```
2. Install docker
```
sudo sh ./docker_install.sh
```
3. Build the docker images
```
sudo docker-compose build
```
4. Compose the docker image and run the container
```
sudo docker-compose up
```
5. Viewing existing docker images
```
sudo docker image ls
```
6. Push from local system to instance
```
scp -i <.pem file location> -r <location on system> ubuntu@<public DNS of instance>:<location on instance>

scp -i /Desktop/amazon.pem -r ./Desktop/MS2334.txt ubuntu@ec2-54-166-128-20.compute-1.amazonaws.com:~/data/
```
7. Download from instance to local system
```
scp -r -i <.pem file location> ubuntu@<public DNS of instance>:<location on instance> <location on system> 

scp -r -i /Desktop/amazon.pem ubuntu@ec2-54-166-128-20.compute-1.amazonaws.com:~/data/ ./Desktop/MS2334.txt
```

---

## References
1) [Create an AWS EC2 instance](https://www.guru99.com/creating-amazon-ec2-instance.html)
2) [Assign an Elastic IP to your AWS EC2 instance](https://www.cloudbooklet.com/how-to-assign-an-elastic-ip-address-to-your-ec2-instance-in-aws/)
3) [Use python SQLite3 using SQLAlchemy](https://medium.com/@mahmudahsan/how-to-use-python-sqlite3-using-sqlalchemy-158f9c54eb32)
4) [Building Docker Images](https://docs.docker.com/get-started/part2/)
5) [Mapping container port to localhost of AWS instance](https://docs.docker.com/get-started/part2/#run-the-app)
6) [Creating AWS target groups and a load balancer with path routing](https://hackernoon.com/what-is-amazon-elastic-load-balancer-elb-16cdcedbd485)
7) [Zookeeper](http://zookeeper.apache.org/)
8) [RabbitMQ tutorials](https://www.rabbitmq.com/getstarted.html)
9) [Zookeeper container image](https://hub.docker.com/_/zookeeper/)
10) [RabbitMQ container image](https://hub.docker.com/_/rabbitmq/)
11) [Leader Election using Zookeeper](https://www.allprogrammingtutorials.com/tutorials/leader-election-using-apache-zookeeper.php)
12) [AMQP Concepts](https://www.rabbitmq.com/tutorials/amqp-concepts.html)
13) [About DBaaS](http://www.vlss-llc.com/blog/what-is-database-as-a-service-dbaas)
14) [Basics of kazoo](https://kazoo.readthedocs.io/en/latest/basic_usage.html)

---

## Contact
For any comments or questions, please contact us at dprajwala11@gmail.com / sanjanashekar99@gmail.com / abhijeetmurthy@gmail.com / sakshidgoel@gmail.com
