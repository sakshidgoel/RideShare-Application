#!/usr/bin/env python
from flask import Flask,render_template,jsonify,request,abort,Response
import threading
import os
import time
import sqlite3
import requests
import re
import math
import csv
import docker
import datetime
import json
import pika
import sys
import uuid
from kazoo.client import KazooClient
from kazoo.client import KazooState
import logging




logging.basicConfig()



app = Flask(__name__)

zk = KazooClient(hosts='zoo:2181')
zk.start()
zk.ensure_path("/orchestrator")

ipaddr = "http://107.22.137.199"
ipaddr_user = "http://54.84.201.252"
ipaddr_ride = "http://3.214.234.217"

master_container_detail={}
slave_container_detail={}

first_request = True

first_zoo_event_req = True

crash_pid_flag = 0



@zk.ChildrenWatch("/orchestrator")
def f(ch):
    print()
    print("Orchestrator:(f()) Event Just got Triggered!")
    global first_zoo_event_req
    global crash_pid_flag
    if(first_zoo_event_req):
        first_zoo_event_req = False


    else:
        print(ch)

        if(crash_pid_flag):
            crash_pid_flag=0
            print("Orchestrator:(f()) Adding a Slave as the previous one crashed!")
            requests.post('http://localhost:80/api/v1/create/slave')

        else:

            m=0
            lowest=-1
            corres_c=""

            for c in ch:
                print("Orchestrator:(f()) Iteration at 'c':",c," & type of 'c':",type(c))

                d,s = zk.get("/orchestrator/"+c)
                m_or_s = d.decode("utf-8").split(",")[0]
                pid = int(d.decode("utf-8").split(",")[1])
                #If data is not empty and data==master
                if(m_or_s == "master"):
                        m=1
                        print("Orchestrator:(f()) Master Exists!")
                else:
                    if(lowest==-1):
                        lowest=pid
                    if(pid<=lowest):
                        lowest=pid
                        corres_c=c

            #Making the first node in the list as the master
            if(m==0):
                print("Orchestrator:(f()) As Master wasn't found, changing Slave to Master")
                strin="master,"+str(lowest)
                zk.set("/orchestrator/"+corres_c,strin.encode('utf-8'))
                print("Orchestrator:(f()) /orchestrator/"+corres_c+" is the New Master!")
                master_container_detail[lowest] = slave_container_detail[lowest]
                slave_container_detail.pop(lowest)
                requests.post('http://localhost:80/api/v1/create/slave')




def crash_slave_scaler():
    global slave_container_detail

    m=-1
    for pid in slave_container_detail:
        if(m<pid):
            m=pid
    if(m>-1):
        resp=slave_delete_con(m)
        if(resp==200):
            return "Scaled-down by 1!"

    return "Couldn't Scale Down!"




def scaler():
    n=1
    with open("request_count.json","r") as file:
        j = json.load(file)

    total_requests = j["total_requests"]

    if(total_requests!=0):
        n = math.ceil(total_requests/5)

    j["total_requests"]=0

    with open("request_count.json","w") as file:
        json.dump(j,file)

    timer = threading.Timer(60.0, scaler)
    timer.start()

    run=1
    while(run):
        print()
        print("Orchestrator:(scaler()) master_container_detail:",master_container_detail)
        print("Orchestrator:(scaler()) slave_container_detail:",slave_container_detail)

        if(len(slave_container_detail)==n):
            run=0

        if(len(slave_container_detail)<n):
            x=requests.post('http://localhost:80/api/v1/create/slave')
            if(x):
                print("Slave Added")
        if(len(slave_container_detail)>n):
            x=crash_slave_scaler()
            if(x):
                print("Slave Killed")

class writeResponseObject(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='rmq'))

        self.channel = self.connection.channel()

        req = self.channel.queue_declare(queue='writeQ',durable = True)
        self.request_queue = req.method.queue

        result = self.channel.queue_declare(queue='writeResponseQ', durable = True)
        self.callback_queue = result.method.queue


        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)


    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=self.request_queue,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(n))
        while self.response is None:
            self.connection.process_data_events()

        self.connection.close()
        print(self.response)
        return self.response




class ResponseObject(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='rmq'))

        self.channel = self.connection.channel()

        req = self.channel.queue_declare(queue='readQ',durable = True)
        self.read_queue = req.method.queue

        result = self.channel.queue_declare(queue='responseQ', durable = True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)


    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=self.read_queue,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(n))
        while self.response is None:
            self.connection.process_data_events()

        self.connection.close()
        print(self.response)
        return self.response



@app.route("/api/v1/db/write",methods=["POST"])
def write_db():
    global first_request
    global slave_container_detail
    global master_container_detail

    if(first_request):
        timer = threading.Timer(60.0, scaler)
        timer.start()
        first_request = False
        with open("request_count.json","w") as file:
            count={}
            count["total_requests"]=0
            json.dump(count,file)

    if(len(master_container_detail)==0 and len(slave_container_detail)==0):
        print("Orchestrator:(write_db()) First Request Received, Spawning a Slave!")
        y = requests.post("http://ipaddr/api/v1/create/slave")
        if(y):
            print()
            print("Orchestrator:(write_db()) Created Initial Slave")

    message = request.get_json()
    writeRespObj = writeResponseObject()
    wresp = writeRespObj.call(message).decode()
    res = json.loads(wresp)

    del(writeRespObj)
    return res["status"]



@app.route("/api/v1/db/read",methods=["POST"])
def read_db():
    global first_request
    global slave_container_detail
    global master_container_detail

    if(first_request):
        timer = threading.Timer(60.0, scaler)
        timer.start()
        first_request = False
        with open("request_count.json","w") as file:
            count={}
            count["total_requests"]=1
            json.dump(count,file)

        return Response(status=400)

    if(len(master_container_detail)==0 and len(slave_container_detail)==0):
        #x = requests.post("http://localhost:80/api/v1/create/master")
        y = requests.post("http://ipaddr/api/v1/create/slave")
        if(y):
            print()
            print("Orchestrator:(read_db()) Created Initial Slave")
            #counting the number of requests
    if(request.get_json()["dual_request_flag"]==1):
        with open("request_count.json","r") as file:
            j = json.load(file)

        total_requests = j["total_requests"]
        j["total_requests"] = total_requests + 1

        with open("request_count.json","w") as file:
            json.dump(j,file)


    message = request.get_json()
    respObj = ResponseObject()

    response = respObj.call(message).decode()
    del(respObj)
    print()
    print(" Orchestrator:(read_db()) Got Response for READ:%r and it's type is:%r" % (response,type(response)))
	#rabbitMQreadcall(message)
    return response

def master_delete_con(ppid):
    v=master_container_detail[ppid]
    v.remove(force= True)
    print()
    print("Orchestrator:(master_delete_con()) Removed Master Container with "+str(ppid)+" Pid!")
    master_container_detail.pop(ppid)
    return 200

def slave_delete_con(ppid):
    global crash_pid_flag
    v=slave_container_detail[ppid]

    v.remove(force= True)
    print()
    print("Orchestrator:(slave_delete_con()) Removed Slave Container with "+str(ppid)+" Pid!")
    slave_container_detail.pop(ppid)
    return 200


@app.route("/api/v1/create/slave",methods=["POST"])
def create_con_slave():
    global slave_container_detail
    #global master_container_detail
    client = docker.from_env()
    client.images.build(path=".", tag="slave")
    client.containers.create("slave",detach=True)

    cont_id = os.popen("hostname").read().strip()
    print()
    print("Orchestrator:(create_con_slave()) Orchestrator's Container ID:",cont_id)
    v=client.containers.run("slave",command="python worker.py",network='zookeeper_amqp_default',links={'rmq':'rmq'},detach=True,volumes_from=[cont_id])
    print ("Orchestrator:(create_con_slave()) New Slave created!")
    ppid = int(v.top()['Processes'][0][2])#Display the running processes of the container
    slave_container_detail[ppid]=v
    print("Orchestrator:(create_con_slave()) PPID is ",ppid)
    return "Created"



@app.route("/api/v1/crash/master",methods=["POST"])
def crash_master():
    global master_container_detail
    if(request.method=="POST"):
        for key in master_container_detail:
            resp=master_delete_con(key)
            if(resp==200):
                return jsonify([key])
        return Response(status=400)
    else:
        return Response(status=405)


@app.route("/api/v1/crash/slave", methods=["POST"])
def crash_slave():
    global slave_container_detail
    global crash_pid_flag
    if(request.method=="POST"):

        m=-1
        for pid in slave_container_detail:
            if(m<pid):
                m=pid
        if(m>-1):
            crash_pid_flag=1
            resp=slave_delete_con(m)
            if(resp==200):
                return jsonify([m])
            return Response(status=400)
        else:
            return Respsonse(status=400)
    else:
        return Response(status=405)


@app.route("/api/v1/list",methods=["GET"])
def list_container_pid():
    global slave_container_detail
    global master_container_detail
    if(request.method=="GET"):
        l=[]
        f = master_container_detail.keys()
        s = slave_container_detail.keys()
        l=sorted(f+s)
        return jsonify(l)
    else:
        return Response(status=405)


if __name__=="__main__":

    app.run(host="0.0.0.0",port=80,debug=False)
