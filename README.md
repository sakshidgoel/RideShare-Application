# RideShare-Application

## Introduction
The objective of the project is to build a Rideshare application with a mini DBaaS system.  
Database-as-a-service is a database service that typically runs on a cloud architecture. Key characteristics are:
  1. Self-service
  2. On-demand
  3. Dynamic
  4. Security
  5. Automation  
  
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
  
  ## Contact
  For any queries, email at dprajwala11@gmail.com / sanjanashekar99@gmail.com / sakshidgoel@gmail.com / abhijeetmurthy@gmail.com
