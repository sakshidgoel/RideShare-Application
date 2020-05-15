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
An instance is a virtual server which can be rented by a subscriber/user and can be used to deploy various applications. The instances are charged per hour with different rates based on the type of the instance chosen. These instances can be terminated when it is no more used.

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
```
ssh -i "rides.pem" ubuntu@ec2-3-214-71-187.compute-1.amazonaws.com
```
4) Open your command prompt in the location that has your private .pem file and paste this command and run it. 
5) You will be logged in onto your instance, where you can launch your application and use it like any other ubuntu machine.

### Setting an Elastic IP for an instance
1) Under Network and security, click Elastic IPs
2) In the loaded screen, click on Allocate Elastic IP address and then choose the Amazon's pool of IPv4 address radio button.
3) Once a new IPv4 address is allocated, check the box for it and open the 'Actions' dropdown to choose 'Associate Elastic IP address'.
4) In the 'Resource type', choose Instance and choose the instance you want to associate this ipv4 address with from the dropdown on the Instance field.
5) If you have any other Elastic IP address assigned to this instance before and you need to re-associate, you have to enable the checkbox of 'Reassociation'.
6) Click Associate and a new elastic IPv4 will be assigned to your instance.
  
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
  
  ## Contact
  For any queries, email at dprajwala11@gmail.com / sanjanashekar99@gmail.com / sakshidgoel@gmail.com / abhijeetmurthy@gmail.com
