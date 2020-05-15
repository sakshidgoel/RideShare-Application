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
from flask import Flask, request, jsonify,Response
from sqlalchemy import and_, or_, not_
from sqlalchemy import update


app=Flask(__name__)
basedir= os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'db.sqlite2')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False 
db = SQLAlchemy(app)
ma=Marshmallow(app)

Area = []
f = open('AreaNameEnum.csv')
try:
    enum = csv.reader(f)
    next(f)     # Skip the first 'title' row.
    for row in enum:
    	a = [int(row[0]),row[1]]
    	Area.append(a)
   
finally:
    # Close files and exit cleanly
    f.close()
'''
class User(db.Model):
	__tablename__ ='User'
	id = db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(25),unique=True)
	password=db.Column(db.String(40),unique=True)

	def __init__(self,username,password):
		self.username=username
		self.password=password

class UserSchema(ma.Schema):
	class Meta:
		fields=('id','username','password')

user_schema=UserSchema()
users_schema=UserSchema(many=True)
'''
class Ride(db.Model):
	__tablename__='Ride'
	rideId = db.Column(db.Integer,primary_key=True)
	created_by=db.Column(db.String(25))
	source=db.Column(db.String(50))
	destination=db.Column(db.String(50))
	timestamp=db.Column(db.String(50))
	users=db.Column(db.String(500))

	def __init__(self,created_by,timestamp,source,destination,users):
		self.created_by=created_by
		self.timestamp=timestamp
		self.source=source
		self.destination=destination
		
		self.users=users

class RideSchema(ma.Schema):
	class Meta:
		fields=('rideId','created_by','timestamp','source','destination','users')

ride_schema=RideSchema()
rides_schema=RideSchema(many=True)






# 3. API FOR CREATING A NEW RIDE-working perfectly
@app.route('/api/v1/rides',methods=['POST'])
def addRide():
	
	x = requests.post('http://localhost:80/api/v1/_count1',json={"type":"api"})
	if request.method=='POST':
		
		created_by=request.json['created_by']
		timestamp=request.json['timestamp']
		z=re.match("(0[1-9]|[1-2][0-9]|3[0-1])-(0[1-9]|1[0-2])-[0-9]{4}:[0-5][0-9]-[0-5][0-9]-(2[0-3]|[01][0-9])",timestamp)
		if not z:
			abort(401)
		source=request.json['source']
		destination=request.json['destination']
		if(int(source) in range(1,199) and int(destination) in range(1,199)):

			Exists = db.session.query(User).filter_by(username=created_by)
			if (Exists.scalar() is not None ):
				data={"table" : "Ride" , "method":"post","created_by":created_by,"timestamp":timestamp,"source":source,"destination":destination,"users":created_by}
				response=(requests.post('http://localhost:80/api/v1/db/write',json=data))
				p=(requests.post('http://localhost:80/api/v1/rides/count1',json={"new":"ride"}))
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
	x = requests.post('http://localhost:80/api/v1/_count1',json={"type":"api"})
	if request.method=='GET':
		res=[]
		source=request.args.get('source')
		destination=request.args.get('destination')
		if(int(source) in range(1,199) and int(destination) in range(1,199)):

				rides=db.session.query(Ride).filter(and_(Ride.source==int(source)),(Ride.destination==int(destination)))
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
	
	x = (requests.post('http://localhost:80/api/v1/_count1',json={"type":"api"}))
	
	if request.method=='GET':
		
		ride=db.session.query(Ride).filter_by(rideId=rideId)
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
	x = requests.post('http://localhost:80/api/v1/_count1',json={"type":"api"})
	if request.method=='POST':
		
		ride=db.session.query(Ride).filter_by(rideId=rideId)
		if(ride.scalar() is not None):
			result=rides_schema.dump(ride)
			for i in result:
				users=i['users']
			
			username = request.json['username']
			Exists = db.session.query(User).filter_by(username=username)
			if (Exists.scalar() is not None):

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
	x = requests.post('http://localhost:80/api/v1/_count1',json={"type":"api"})
	if request.method=='DELETE':
		Exists = db.session.query(Ride).filter_by(rideId=rideId)
		if (Exists.scalar() is not None):
			rideId1=int(rideId)
			data={"table":"Ride","method":"delete","rideId":rideId1}
			print (data)
			response=(requests.post('http://54.236.205.77:80/api/v1/db/write',json=data))
			p=(requests.post('http://localhost:80/api/v1/rides/countdel',json={"new":"ride"}))
			return Response(status=200)
		else:
			return Response(status=400)
	else:
		return Response(status=405)

# 8. Write to db
@app.route('/api/v1/db/write',methods=['POST'])
def writetodb():
	req=request.get_json()
	table=req['table']
	method=req['method']
	if (table=="Ride" and method=="post"):
		created_by=req['created_by']
		timestamp=req['timestamp']
		source=req['source']
		destination=req['destination']
		users=req['users']
		newRide=Ride(created_by,timestamp,source,destination,users)
		db.session.add(newRide)
		db.session.commit()
		return Response(status=201)
	elif (table=="User" and method=="put"):
		username=req['username']
		password=req['password']
	
		newUser=User(username,password)
		db.session.add(newUser)
		db.session.commit()
		return Response(status=201)

	elif (table=="User" and method=="delete"):
		#print("hi")
		username=req['username']
		user = User.query.filter_by(username=username).first_or_404()
		#print("######################"+str(user))
		#ri=User.query.get(user)
		db.session.delete(user)
		db.session.commit()
		return Response(status=200)
	
		
	elif(table=="Ride" and method=="delete"):
		ride_Id=req['rideId']
		ri=Ride.query.get(ride_Id)
		db.session.delete(ri)
		db.session.commit()
		#return user_schema.jsonify()
		return Response(status=200)
		

	


# 9. Read db
@app.route('/api/v1/db/read',methods=['POST'])
def Read():
	table = request.json['table']
	where = request.json['where']
	length = len(where)
	if (table=="Ride" and length==1):
		rideId = where[0]
		details = db.session.query(Ride).filter_by(rideId=rideId)
		rideId = details.rideId
		created_by = details.created_by
		users = details.users
		timestamp = details.timestamp
		source = details.source
		destination = details.destination
		users = users.split(';')
		result = {"rideId":rideId,"created_by":created_by,"users": users,"timestamp":timestamp,"source":source,"destination":destination}
		return result
	elif (table=="Ride" and length==2):
		source=where[0]
		destination=where[1]
		upcoming = db.session.query(Ride).filter_by(and_(source=source,destination=destination))
		result = []
		for i in upcoming:
			rideId = i.rideId
			username=i.username
			timestamp=i.timestamp
			up = {"rideId":rideId,"username":username,"timestamp":timestamp}
			result.append(up)
		return result
	elif (table=="User"):
		all_users=User.query.all()
		result=users_schema.dump(all_users)
		return jsonify(result)




#assignment 2- clear db
@app.route('/api/v1/db/clear',methods=['POST'])
def clearDb():
	x = requests.post('http://localhost:80/api/v1/_count1',json={"type":"api"})
	if request.method=='POST':
		
		
		for c in db.session.query(Ride):
			db.session.delete(c)
				
		db.session.flush()
		db.session.commit()
		return Response(status=200)
	else:
		return Response(status=405)

#EXTRA APIS TO CHECK WORKING

@app.route('/api/v1/_count1',methods=['POST'])
def httprequests1():
	
		req = request.get_json()
		print(req)
		type1 = req["type"]
		
		
		f=open("count1.txt","r")
		count=f.read()
		f.close()
		print(count)
		count=int(count)+1
		
		f=open("count1.txt","w").close()
		f=open("count1.txt","w")
		f.write(str(count))
		f.close()
		return Response(status=200)

@app.route('/api/v1/_count',methods=['GET'])
def httprequests():
	if request.method=="GET":
		f=open("count1.txt","r")
		count=f.read()
		f.close()
		c=[]
		c.append(int(count))
		return jsonify(c)
	else:
		return Response(status=405)

@app.route('/api/v1/_count',methods=['DELETE'])
def httprequestsdel():
	if request.method=="DELETE":
		
		
		f=open("count1.txt","w").close()
		f=open("count1.txt","w")
		f.write("0")
		f.close()
		return Response(status=200)
	else:
		return Response(status=405)

@app.route('/api/v1/rides/count1',methods=['POST'])
def countrides1():	
		req = request.get_json()
		
		
		f=open("ride.txt","r")
		count=f.read()
		f.close()
		print(count)
		count=int(count)+1
		
		f=open("ride.txt","w").close()
		f=open("ride.txt","w")
		f.write(str(count))
		f.close()
		return Response(status=200)
@app.route('/api/v1/rides/count1',methods=['GET'])
def countrides():
	if request.method=="GET":
		f=open("ride.txt","r")
		count=f.read()
		f.close()
		c=[]
		c.append(int(count))
		return jsonify(c)
	else:
		return Response(status=405)


@app.route('/api/v1/rides/countdel',methods=['DELETE'])
def countridedel():
	if request.method=="DELETE":
		
		
		req = request.get_json()
		
		
		f=open("ride.txt","r")
		count=f.read()
		f.close()
		print(count)
		count=int(count)-1
		
		f=open("ride.txt","w").close()
		f=open("ride.txt","w")
		f.write(str(count))
		f.close()
		return Response(status=200)

if __name__=='__main__':
	app.run(debug=True,host="0.0.0.0",port=80)