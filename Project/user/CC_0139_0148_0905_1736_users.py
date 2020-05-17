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

app=Flask(__name__)



# 1. ADD USER API- working perfectly
@app.route('/api/v1/users',methods=['PUT'])
def addUser():
	if request.method=='PUT':
		username=request.json['username']
		password=request.json['password']
		data={"username":username,"table":'User'}
		Exists = (requests.post(ipaddr+'/api/v1/db/read',json=data))

		if (Exists.scalar() is not None ):
			return Response(status=400)
		else:
			length = len(password)
			if (length == 40):
				reg = r'[0-9a-fA-F]+'
				m = re.match(reg,password)
				if not m:
					return Response(status=400)
				data={"table":"users","username":username,"password":password,"join":0}
				response=(requests.post(ipaddr+"/api/v1/db/write",json=data))
				return Response(status=int(response.text))
			else:
				return Response(status=400)
	else:
		return Response(status=405)


# 2. DELETE USER- working perfectly
@app.route('/api/v1/users/<username>',methods=['DELETE'])
def deleteUser(username):
	if request.method=='DELETE':
		data={"username":username,"table":'User'}
		Exists = (requests.post(ipaddr+'/api/v1/db/read',json=data))
		if (Exists.scalar() is not None):
			data={"username":username,"join":3}
			response=(requests.post(ipaddr+'/api/v1/db/write',json=data))
			return Response(status=int(response.text))
		else:
			return Response(status=400)
	else:
		return Response(status=405)




# assignment 2- list users -working perfectly
@app.route("/api/v1/users",methods=["GET"])
def list_users():

    if(request.method=="GET"):
        s=[]
        print("check")
        try:
            data={"table":"users","insert":["username"],"where_flag":0,"dual_request_flag":1}
            req = requests.post(ipaddr+"/api/v1/db/read",json=data)
            return jsonify(req.text.split(","))
        except:
            return Response(status=400)
    else:
        return Response(status=405)



if __name__=='__main__':
	app.run(host="0.0.0.0",port=80,debug=True)
