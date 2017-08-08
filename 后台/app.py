#-*- coding:utf-8 -*-
__author__ = 'huyangchun'

#!falsk/bin/python
import os
# from flask import Flask,jsonify
# from flask import make_response
# from flask import request
# from flask import url_for
from flask_cors import CORS
from flask import Flask,jsonify,make_response,request,url_for,abort,g,render_template,redirect
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_content
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,BadSignature,SignatureExpired
import datetime
import random
import uuid
import socket
import json

from flask import abort

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__,static_folder='static')
app.config['SECURITY_KEY'] = 'hard to guess'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =True
CORS(app,supports_credentials=True)
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'
db = SQLAlchemy(app)
auth = HTTPBasicAuth()
class Selling_info(db.Model):
	__tablename__ = 'selling_info'
	sell_id = db.Column(db.BigInteger,nullable = False,primary_key = True)
	username = db.Column(db.String(64),nullable = False)
	buyer = db.Column(db.String(64))
	price = db.Column(db.Float)
	power_size = db.Column(db.Float)
	balance = db.Column(db.BigInteger,default= 0)
	has_dealed_flag = db.Column(db.String,default = 'on')




	def generate_id(self):
		id_temp = int((datetime.datetime.utcnow()-datetime.datetime(1970,1,1)).total_seconds())
		id_head = random.randint(100,1000)
		id_last = str(str(id_head) + str(id_temp))
		self.sell_id = id_last



class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.String(64),nullable = False,unique = True)
	username = db.Column(db.String(64),primary_key = True,unique = True,nullable = False,index = True)
	password_hash = db.Column(db.String(64),nullable = False)
	# user_type = db.Column(db.String(64))
	money = db.Column(db.Float,default = 0)
	email = db.Column(db.String)
	hardware_sign = db.Column(db.String)



	def generate_id(self):
		self.id = str(uuid.uuid1())



	def hash_pwssword(self,password):
		self.password_hash = pwd_content.encrypt(password)
	def verify_password(self,password):
		return pwd_content.verify(password,self.password_hash)


	def generate_auth_token(self,expiration = 60):
		s = Serializer(app.config['SECURITY_KEY'],expires_in=expiration)
		return s.dumps({'id':self.id})

	@staticmethod
	def verify_auth_token(token):
		s = Serializer(app.config['SECURITY_KEY'])
		try:
			data = s.loads(token)
		except SignatureExpired:
			return None
		except BadSignature:
			return None
		user = User.query.get(data['id'])
		return user

	# def is_active(self):
	# 	return True
	# def get_id(self):
	# 	return unicode(self.id)



@auth.verify_password
def verify_password(username_or_token,password):
	user = User.verify_auth_token(username_or_token)
	if not user:
		user = User.query.filter_by(username = username_or_token).first()
		if not user or not user.verify_password(password):
			return False
	g.user = user
	return True
#
# class Selling_info(db.Model):
# 	__tablename__ = 'selling'
# 	id = db.Column(db.Interger,nullable = False)
# 	username = db.Column(db.String(64),unique = True,nullable = False)
# 	balance = db.Column(db.Float)
@app.route('/',methods = ['GET'])
def index():
	return redirect(url_for('static',filename = 'index.html'),301)
@app.route('/api/register/addUsers',methods = ['POST'])
# @db.session
def new_user():
	user_name = request.json.get('username')
	pass_word = request.json.get('password')
	email = request.json.get('email')
	hardware_sign = request.json.get('hardware_sign')

	if user_name is None or pass_word is None:
		return(jsonify({'status':'fialed','msg':'null username or null password'}))
	if User.query.filter_by(username = user_name).first() is not None:
		return (jsonify({'status':'fialed', 'msg': 'user exists'}))

	user = User(username = user_name,email = email,hardware_sign = hardware_sign,money =0.0)
	user.hash_pwssword(pass_word)
	# token = user.generate_auth_token(600)
	user.generate_id()
	db.session.add(user)
	db.session.commit()
	return (jsonify({'status':'success','data':{'username':user.username,'id':user.id}}),201,
			{'Location':url_for('get_user',id = user.id,_external=True)})


@app.route('/api/login',methods = ['POST'])
# @auth.verify_password
def user_login():
	username = request.json.get('username')
	password = request.json.get('password')
	data = {}

	login_info = User.query.filter_by(username = username).first()
	if not login_info:
		return jsonify({"status":"failed","msg":"wrong username"})
	if not login_info.verify_password(password):
		return jsonify({"status":"failed","msg":"wrong password"})
	token = login_info.generate_auth_token(600)
	money = login_info.money
	data['money'] = round(money,2)
	data['token'] = token.decode('ascii')
	return jsonify({"status":"success","data":data})

@app.route('/api/users/<id>')
def get_user(id):
	user = User.query.get(id)
	if not user:
		abort(400)
	return jsonify({'username':user.username})

@app.route('/api/token')
@auth.login_required
def get_auth_token():
	token = g.user.generate_auth_token(600)
	return jsonify({'token':token.decode('ascii'),'duration':600,'id':g.user.id})

@app.route('/api/resource')
@auth.login_required
def get_resouece():
	return jsonify({'data':'hello,%s'%g.user.username})




#获取用户信息
@app.route('/api/getPersonalInfo',methods = ['GET'])
@auth.login_required
def get_personal_info():
	user_info = g.user
	data = {}
	data["username"] = user_info.username
	data["id"] = user_info.id
	data["money"] = round(user_info.money,2)

	return jsonify({"status":"success","data":data})


#推送挂单
@app.route('/api/postSellInfo',methods = ['POST'])
# @auth.login_required

def post_sell_info():
	sell_user = request.json.get('userName')
	sell_pric = request.json.get('price')
	sell_size = request.json.get('size')
	# if sell_user != g.user.username:
	# 	return jsonify({'status':'failed','data':{'msg':'you can only post your own sell info'}})
	sell_info = Selling_info(username = sell_user,price = sell_pric,power_size = sell_size,has_dealed_flag = 'on')
	sell_info.generate_id()
	db.session.add(sell_info)
	db.session.commit()
	return jsonify({'status':'success','data':{'msg':'sell info post success'}})

#获取正在等待交易的挂单
@app.route('/api/getMySellingList',methods = ['POST'])
# @auth.login_required

def get_all_info():
	data = []
	username = request.json.get('userName')
	all_info = Selling_info.query.filter_by(username = username).all()
	for item in all_info:

		item_data = {}
		item_data['id'] = item.sell_id
		item_data['seller'] = item.username
		item_data['price'] = item.price
		item_data['size'] = item.power_size
		if item.has_dealed_flag == 'on':
			item_data['flag'] = 0
		elif item.has_dealed_flag == 'selling':
			item_data['flag'] = 1
		else:
			item_data['flag'] = 2
		data.append(item_data)
		print(item_data)


	# print(all_info)
	# data = json.dumps(data)
	return jsonify({'status':'success','data':data})
# @app.route('/api/resetsellinfo/<sellid>',methods=['POST'])
# @auth.login_required
# def reset_sell_info(sellid):
# 	sellinfo = Selling_info.query.filter_by(sell_id = sellid).first()
# 	if g.user.username != sellinfo.username:
# 		return jsonify({"status":"fialed","msg":"can't reset other's info"})
# 	sell


#获取所有未交易的挂单
@app.route('/api/getAllSelling',methods = ['POST'])

def get_all_selling_list():
	username = request.json.get('userName')
	sell_info = Selling_info.query.all()
	data = []
	for item in sell_info:


		if (item.has_dealed_flag == 'on') and (item.username != username):
			item_data = {}


			item_data['id'] = item.sell_id
			item_data['seller'] = item.username
			item_data['price'] = item.price
			item_data['size'] = item.power_size

			data.append(item_data)
	return jsonify({"status":"success","data":data})



#获取已经交易的挂单
@app.route('/api/getMySoldList')
@auth.login_required

def get_all_sold_info():
	data = {}
	data.setdefault('data',[])
	all_info = Selling_info.query.filter_by(username = g.user.username).all()
	for item in all_info:
		if item.has_dealed_flag == 'selled':
			item_data = {}
			item_data['id'] = item.sell_id
			item_data['username'] = item.username
			item_data['price'] = item.price
			item_data['size'] = item.power_size
			item_data['buyer'] = item.buyer
			data['data'].append(item_data)
			print(item_data)


	# print(all_info)
	# data = json.dumps(data)
	return jsonify({'status':'success','data':data})

#修改挂单
@app.route('/api/changeMySellInfo',methods = ['PUT'])
@auth.login_required
def change_my_sell_info():
	id = request.json.get('sell_id')
	price = request.json.get('price')
	power_size = request.json.get('power_size')
	sell_info = Selling_info.query.filter_by(sell_id = id).first()
	sell_info.price = price
	sell_info.power_size = power_size
	db.session.add(sell_info)
	db.session.commit()
	data = {}
	data['price'] = price
	data['power_size'] = power_size
	return jsonify({"status":"success","data":data})
#删除挂单
@app.route('/api/deleteMySellInfo',methods = ['POST'])
# @auth.login_required

def delete_my_sell_info():
	id = request.json.get('sellId')
	sell_info = Selling_info.query.filter_by(sell_id = id).first()
	if sell_info.has_dealed_flag == 'selled':
		return jsonify({"status":"failed","msg":"the post is sold","flag":"selled"})
	if sell_info.has_dealed_flag == 'selling':
		return jsonify({"status":"failed","msg":"the post is selling","flag":"selling"})

	db.session.delete(sell_info)
	db.session.commit()
	return jsonify({"status":"success","msg":"delete success"})

# @app.route('/api/getallsellinfo')
# @auth.login_required
# def get_all_sell_info():


#充值的api
@app.route('/api/pushMoney',methods = ["POST"])
# @auth.login_required

def push_money():
	# username = request.json.get("userName")
	username = request.json.get("userName")
	money = float(request.json.get("addMoney"))
	# username = g.user.username
	user_info = User.query.filter_by(username = username).first()
	try:


		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect(('localhost', 1234))  # 链接服务器
	except ConnectionRefusedError:
		return jsonify({"status":"failed","msg":"sever ConnectionRefusedError"})

	while True:
		sock.send('{},{},{}'.format(username[-1],str(money),'charge').encode())  # 发送数据给服务器
		data_recv = sock.recv(1024).decode()  # 接收服务器发过来到数据
		break
	sock.close()


	if data_recv == "Success":

		my_money = user_info.money + float(money)
		user_info.money = my_money
		db.session.add(user_info)
		db.session.commit()
		money = user_info.money
		return jsonify({"status" : "success","money":money})
	else:
		return jsonify({"status":"failed","msg":"unknown error"})


# 购买的api

@app.route('/api/buy',methods = ["POST"])
# @auth.login_required

def buy():
	buyer = request.json.get('userName')
	user_info = User.query.filter_by(username = buyer).first()
	# user_info = g.user
	# buyer = user_info.username

	sell_id = request.json.get("sellId")
	sell_info = Selling_info.query.filter_by(sell_id = sell_id).first()
	seller_info = User.query.filter_by(username = sell_info.username).first()
	if sell_info.has_dealed_flag == 'selled':
		abort(404)
	if buyer == sell_info.username:
		abort(404)
	price = sell_info.price
	power_size = sell_info.power_size
	total = round(price*power_size,2)
	print(total)
	if user_info.money < total:
		return jsonify({"status":"failed","msg":"money is not enough"})
	sell_info.has_dealed_flag = 'selling'
	sell_info.buyer = buyer
	db.session.add(sell_info)
	db.session.commit()


	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect(('192.168.43.212', 1234))  # 链接服务器
	except ConnectionRefusedError:
		return jsonify({"status":"failed","msg":"server ConnectionRefusedError"})
	while True:
		sock.send('{},{},{},{},{},{}'.format(seller_info.username[-1],buyer[-1],total,power_size,price,'move').encode())  # 发送数据给服务器
		data_recv = sock.recv(1024).decode()  # 接收服务器发过来到数据
		break
	sock.close()


	if data_recv == 'Success':
		user_info.money = user_info.money - total
		seller_info.money = seller_info.money + total
		db.session.add(user_info)
		db.session.add(seller_info)
		db.session.commit()
		sell_info.buyer = buyer
		sell_info.has_dealed_flag = 'selled'
		db.session.add(sell_info)
		db.session.commit()

		return jsonify({"status":"success","money":user_info.money})
	else:
		sell_info.has_dealed_flag = 'on'
		sell_info.buyer = ''
		db.session.add(sell_info)
		db.session.commit()
		return  jsonify({"status":"failed","msg":"unkown error"})


#获取用户购买的挂单信息
@app.route('/api/getMyBought',methods = ['POST'])
# @auth.login_required


def get_my_bought():
	user_name = request.json.get('userName')
	user_info = User.query.filter_by(username = user_name)
	# user_info = g.user
	# user_name = user_info.username
	buy_info = Selling_info.query.filter_by(buyer = user_name).all()

	data = []
	# data.setdefault('data',[])
	for item in buy_info:
		if item.has_dealed_flag == 'selled':
			item_data = {}
			item_data['sell_id'] = item.sell_id
			item_data['price'] = item.price
			item_data['power_size'] = item.power_size
			item_data['seller'] = item.username
		data.append(item_data)
	return jsonify({"status":"success","data":data})





#获取用户参与的挂单信息，包括卖出的和买进的



@app.route('/api/getTransRecord',methods = ['POST'])
# @auth.login_required


def get_my_record():
	user_name = request.json.get('userName')
	trans_info =Selling_info.query.all()
	# user_info = g.user
	# user_name = user_info.username
	#trans_info = Selling_info.query.filter(Selling_info.buyer == user_name or Selling_info.username == user_name).all()

	data = []
	# data.setdefault('data',[])
	for item in trans_info:
		if item.buyer == user_name or item.username == user_name:

			item_data = {}
			item_data['buyer'] = item.buyer
			item_data['id'] = item.sell_id
			item_data['price'] = item.price
			item_data['size'] = item.power_size
			item_data['seller'] = item.username
			item_data['status'] = item.has_dealed_flag
		# if item.has_dealed_flag == 'on' and user_name == item.buyer:
		# 	item_data['has_dealed_flag'] = '等待卖出'
		# if item.has_dealed_flag == 'selling' and user_name == item.buyer:
		# 	item_data['has_dealed_flag'] = '正在购买'
		# if item.has_dealed_flag == 'selling' and user_name == item.username:
		# 	item_data['has_dealed_flag'] = '正在卖出'
		# if item.has_dealed_flag == 'selled' and user_name == item.buyer:
		# 	item_data['has_dealed_flag'] = '已经购买'
		# if item.has_dealed_flag == 'selled' and user_name == item.username:
		# 	item_data['has_dealed_flag'] = '已经卖出'

			data.append(item_data)
	return jsonify({"status":"success","data":data})





# @app.route('/api/login',methods = ['POST'])
# @db.session

# def sign_in():
# 	user_name = request.json.get('username')
# 	pass_word = request.json.get('password')
# 	remember_me = request.json.get('remember_me')
# 	if user_name is None or pass_word is None:
# 		return jsonify({'status':{'code':'failed','msg':'please input username or password'}})
# 	user = User.query.filter_by(username = user_name).first()
# 	if user is None or not user.verify_password(pass_word):
# 		return jsonify({'status':{'code':'failed','msg':'user not exits or wrongpassword'}})
# 	if user is not None and user.verify_password(pass_word):
# 		# login_user(user,remember_me)
# 		return jsonify({'status':{'code':'success','msg':'yes'}})

# @app.route('/api/logout')
# @login_required
#
# def logout():
# 	logout_user()
# 	return jsonify({'status':{'code':'success','msg':'log out success'}})





if __name__ == "__main__":
	if not os.path.exists('db.sqlite'):
		# db.drop_all()
		db.create_all()
	# app.run(debug = True,host='192.168.1.114',port=8079)
	app.run(debug = True,host='0.0.0.0',port= 8080)