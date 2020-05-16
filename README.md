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
for rides ms, map the port within the container to 8000
for users ms, 8080

1. Running 2 microservices with the given container name and tag and ENV variable
2. Exposing 8000 and 8080 on public ip
3. Implementing and calling the “List all users” API from the “rides” container

### Dockerfile

Dockerfile is a text file that is used to build the image
docker-compose.yml is a file that contains the configuration on how many containers to make, what ports to expose, which database, volume to use to externally store the data etc
We have one docker-compose file for each microservice
Each ms will have own database, no shared db can be used

## Functionalities implemented
Following are the expected functionalities that need to be implemented:
  1. Queues for message passing
  2. Eventual consistency handled
  3. High availability and fault-tolerance
  4. Scaling 
  5. Orchestrator, worker set up
  6. Rabbitmq, zookeeper usage
  
  ## Steps to Run
  1. Install Flask
  ```
  pip install Flask
  ```
  2. Install docker
  ```
  sudo sh ./docker_install.sh
  ```
  3. Set up the containers in the rides, users and orchestrator instances
  ```
  sudo docker-compose build
  sudo docker-compose up
  ```
  
  ## References
  1) [Create an AWS EC2 instance](https://www.guru99.com/creating-amazon-ec2-instance.html)
  2) [Assign an Elastic IP to your AWS EC2 instance](https://www.cloudbooklet.com/how-to-assign-an-elastic-ip-address-to-your-ec2-instance-in-aws/)
  3) [Use python SQLite3 using SQLAlchemy](https://medium.com/@mahmudahsan/how-to-use-python-sqlite3-using-sqlalchemy-158f9c54eb32)
  
  ## Contact
  For any comments or questions, please contact us at dprajwala11@gmail.com / sanjanashekar99@gmail.com / abhijeetmurthy@gmail.com / sakshidgoel@gmail.com
