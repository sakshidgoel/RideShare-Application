from flask import Flask, request , jsonify,Response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
import os
import re
import ast
import requests
import json
import csv
import collections
from flask_api import status
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime
from flask_marshmallow import Marshmallow
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from flask import Flask, jsonify, request, abort,redirect, url_for, session
from flask import Flask, request, jsonify
from sqlalchemy import and_, or_, not_
from sqlalchemy import update

path_csv = "AreaNameEnum.csv"
ipaddr = "http://107.22.137.199"
ipaddr_user = "http://54.84.201.252"
ipaddr_ride = "http://3.214.234.217"
app = Flask(__name__)




# 3. API FOR CREATING A NEW RIDE-working perfectly
@app.route('/api/v1/rides',methods=['POST'])
def addRide():
	if request.method=='POST':
		Exists = db.session.query(User).filter_by(username=username)
		created_by=request.json['created_by']
		timestamp=request.json['timestamp']
		z=re.match("(0[1-9]|[1-2][0-9]|3[0-1])-(0[1-9]|1[0-2])-[0-9]{4}:[0-5][0-9]-[0-5][0-9]-(2[0-3]|[01][0-9])",timestamp)
		if not z:
			abort(401)
		Exists=1
		source=request.json['source']
		destination=request.json['destination']
		if(int(source) in range(1,199) and int(destination) in range(1,199)):

			#Exists = "abc"
			
			if (Exists==1):
				data={"table" : "Ride" , "method":"post","created_by":created_by,"timestamp":timestamp,"source":source,"destination":destination,"users":created_by}
				response=(requests.post(ipaddr+'/api/v1/db/write',json=data))
				return Response(status=201)
			else:
				return Response(status=400)
		else:
			return Response(status=400)
	else:
		return Response(status=405)


#4. to list upcoming rides-working perfectly
@app.route('/api/v1/rides',methods=['GET'])
def upcomingRide():
	if request.method=='GET':
		res=[]
		source=request.args.get('source')
		destination=request.args.get('destination')
		if(int(source) in range(1,199) and int(destination) in range(1,199)):

				data={'table':'Ride','source':source,'destination':destination}
				result = (requests.post(ipaddr+'/api/v1/db/read',json=data))
				result=rides_schema.dump(rides)
				print(result)

				for i in result:
					obj={
					"rideId":i['rideId'],
					"username":i['created_by'],
					"timestamp":i['timestamp']
					}
					res.append(obj)

				return jsonify(res)
		
		else:
			return Response(status=204)
	else:
		return Response(status=405)




# 5. Details of a Ride
@app.route('/api/v1/rides/<rideId>', methods = ['GET'])
def details(rideId):
	
	if request.method=='GET':
		
		data={'table':'Ride','rideId':rideId}
		ride = (requests.post(ipaddr+'/api/v1/db/read',json=data))
		if(ride.scalar() is not None):
			result=rides_schema.dump(ride)
			for i in result:
				users=i['users']
			txt=users.split(';')
			print(txt)

			for i in result:
				i['users']=txt
			print(result)
			return jsonify(result)

		else:
			return Response(status=204)
	
				
		
	else:
		return Response(status=405)


	

# 6. Join an existing ride- works perfectly- needs to be routed to db write
@app.route('/api/v1/rides/<rideId>',methods=['POST'])
def joinride(rideId):
	if request.method=='POST':
		data={"username":username,"table":'User'}
		Exists = (requests.post(ipaddr+'/api/v1/db/read',json=data))
		if (Exists.scalar() is not None):
			data={"table":"Ride","method":"delete","rideId":rideId1}
			print (data)
			response=(requests.post(ipaddr+'/api/v1/db/write',json=data))
		Exists=1
		if(ride.scalar() is not None):
			result=rides_schema.dump(ride)
			for i in result:
				users=i['users']
			
			username = request.json['username']
			#Exists = db.session.query(User).filter_by(username=username)

			if (Exists==1):

				users1 = users+';'+username
			
			
				for i in result:
					i['users']=users1
				for c in db.session.query(Ride).filter_by(rideId=rideId):
					c.users = users1
				
				db.session.flush()
				db.session.commit()
			#db.session.commit()
				return Response(status=200)
			else:
				return Response(status=204)
		else:
				return Response(status=204)
				
		
	else:
		return Response(status=405)

# 7.TO DELETE A RIDE-working perfectly
@app.route('/api/v1/rides/<rideId>',methods=['DELETE'])
def deleteRide(rideId):
	if request.method=='DELETE':
		data={'table':'Ride','rideId':rideId}
		ride = (requests.post(ipaddr+'/api/v1/db/read',json=data))
		if (ride.scalar() is not None):
			rideId1=int(rideId)
			data={"table":"Ride","method":"delete","rideId":rideId1}
			print (data)
			response=(requests.post(ipaddr+'/api/v1/db/write',json=data))
			return Response(status=200)
		else:
			return Response(status=400)
	else:
		return Response(status=405)


		




#assignment 2- clear db


if __name__=='__main__':
	app.run(debug=True,host="0.0.0.0",port=8000)