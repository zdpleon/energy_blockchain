# -*- coding: utf-8 -*-

'''
	Edit by Leon zdp
'''

import os
import subprocess
import socket
import sys
from time import sleep
import _thread
import couchdb
import json


data_a = ''
data_b = ''
data_c = ''
data_d = ''
data_e = ''
data_p = ''
name_list = ['a','b','c','d','f','g']
lock = _thread.allocate_lock()

couch = couchdb.Server('http://localhost:5984')
db =  couch['transaction_info']
  
HOST = '0.0.0.0'  # Symbolic name meaning all available interfaces
PORT = 1234 # Arbitrary non-privileged port
  
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Socket created')
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
#Bind socket to local host and port
try:
	s.bind((HOST, PORT))# -*- coding: utf-8 -*-
except socket.error:
	print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
	sys.exit()
    
print ('Socket bind complete')
  
#Start listening on socket
s.listen(10)
print ('Socket now listening')
# For KeyboardInterrupt
def reset():
	s.close()
	sys.exit(1) 

#Function for handling connections. This will be used to create threads
def clientthread(conn):
	#Sending message to connected client
	#conn.send('Connect Success! Transaction Ready!\n'.encode()) #send only takes string
	print ('Connect Success! Transaction Ready!\n')
	#infinite loop so that function do not terminate and thread do not end.
	while True:
		#Receiving from client
		data = conn.recv(512).decode()
		data_recv = data.split(',')
		length = len(data_recv)
		data_a = 0
		data_b = 0 
		data_c = 0
		data_d = 0
		data_e = 0
		data_f = 0
		data_g = 0
		data_p = 0
		data_z = 0
		#split
		if  length == 6 and data_recv[-1] == 'move':
			data_list = ['0','0','0','0','0','0','0','0','0']
			data_list[name_list.index(data_recv[0])] = data_recv[2]
			data_list[name_list.index(data_recv[1])] = '-'+data_recv[2]
			data_list[6] = data_recv[3]
			data_list[7] = data_recv[4]
			data_list[8] = data_recv[5]
			data_a = data_list[0]
			data_b = data_list[1] 
			data_c = data_list[2]
			data_d = data_list[3]
			data_f = data_list[4]
			data_g = data_list[5]
			data_e = data_list[6]
			data_p = data_list[7]
			data_z = data_list[8]
			#print(data_list)
			move_info = 0			
			for mm in [data_list[0],data_list[1],data_list[2],data_list[3],data_list[4],data_list[5]]:
				if mm == '0':
					move_info = move_info + 1
				else:
					continue
			if float(data_list[0]) + float(data_list[1]) + float(data_list[2]) + float(data_list[3]) + float(data_list[4]) + float(data_list[5]) == 0 and move_info == 4 :
				reply1 = '  ####Receive Transation Info,Transacting...Please wait.....####  \n'
				#conn.sendall(reply1.encode())
				lock.acquire() 
				#config change
				old_file ='$GOPATH/src/github.com/hyperledger/fabric/fabric-sdk-node/test/integration/e2e/config.json'
				f =open(old_file,'r+')
				flist=f.readlines()
				flist[53]='	         "{}",\n'.format(data_a)
				flist[54]='	         "{}",\n'.format(data_b)
				flist[55]='	         "{}",\n'.format(data_c)
				flist[56]='	         "{}",\n'.format(data_d)
				flist[57]='	         "{}",\n'.format(data_f)
				flist[58]='	         "{}",\n'.format(data_g)
				flist[59]='	         "{}",\n'.format(data_e)
				flist[60]='	         "{}",\n'.format(data_p)
				flist[61]='	         "{}"\n'.format(data_z)
				f=open(old_file,'w+')
				f.writelines(flist)
				f.close()
				#change done 
				for i in range(1,4):
					trans_info = subprocess.Popen('$GOPATH/src/github.com/hyperledger/fabric/fabric-sdk-node/test/integration/e2e/script.sh',stdout = subprocess.PIPE,shell =True).stdout.read()
					if  trans_info.decode().find('# pass  12') <0:
						retry_info = '  ####Have tried Transaction For {} Times!!!!!!!!####\n  '.format(i)
						print (retry_info)
						sleep(1)				
						if i == 3:
							failed_info = '   ###Transaction failed!!!!!!####\n  '
							print (failed_info)
							conn.sendall('Falied'.encode())
						continue
					else:
						trans_result_a =list()
						trans_result_b =list()
						trans_result_c =list()
						trans_result_d =list()
						trans_result_f =list()
						trans_result_g =list()
						trans_result_e =list()
						trans_result_p =list()
						trans_time = list()
						result_all = list()
						befoe_list = [0,0,0,0]
						next_list = [0,0,0,0]
						result_list = list()
						result_dict = {}
						buy_user = ''
						sell_user = ''
						buy_val = ''
						sell_val = ''
						input_couchDB_json = ''
						input_couchDB = {}				
						docker_info = subprocess.Popen('$GOPATH/src/github.com/hyperledger/fabric/fabric-sdk-node/test/integration/e2e/query1.sh',stdout = subprocess.PIPE,shell =True).stdout.readlines()
						for line in docker_info:
							line = line.strip().decode()
							if '###########' in line or 'Query' in line:
								continue
							result_all.append(line)
						for line in result_all:
							line_list = line.split(',')
							trans_result_a.append(float(line_list[0][38:]))
							trans_result_b.append(float(line_list[1][8:]))
							trans_result_c.append(float(line_list[2][8:]))
							trans_result_d.append(float(line_list[3][8:]))
							trans_result_f.append(float(line_list[4][8:]))
							trans_result_g.append(float(line_list[5][8:]))
							trans_result_e.append(float(line_list[6][15:]))
							trans_result_p.append(float(line_list[7][9:]))
							trans_time.append(line_list[0][:30])
						del trans_time[0]
						trans_time.reverse()
						val_electric = trans_result_e[-1]
						val_price =  trans_result_p[-1]
						next_list = [trans_result_a[-1],trans_result_b[-1],trans_result_c[-1],trans_result_d[-1],trans_result_f[-1],trans_result_g[-1]]
						if len(result_all) > 1:
							befoe_list = [trans_result_a[-2],trans_result_b[-2],trans_result_c[-2],trans_result_d[-2],trans_result_f[-2],trans_result_g[-2]]
						for (l,m) in zip(befoe_list,next_list):
							result_list.append(m-l)
						result_dict = dict(zip(name_list,result_list))
						print('#########3',result_dict)
						result_list = list()							
						for i in result_dict:
							if result_dict[i] < 0:
								buy_user = i
								buy_val = abs(result_dict[i])
							elif result_dict[i] > 0:
								sell_user = i
								sell_val = abs(result_dict[i])
							else:
								continue	
						input_couchDB['Date'] = trans_time[0][:10]
						input_couchDB['Time'] = trans_time[0][11:19]
						#input_couchDB['Meta'] = trans_time[0][20:30]
						input_couchDB['Total_Price'] = round(buy_val,2)
						input_couchDB['KW/h']	 = val_electric
						input_couchDB['Unit_Price'] = val_price
						conn.sendall('Success'.encode())
						#conn.sendall(input_couchDB_json.encode())
						#conn.sendall('  ####Transaction Complete! Buyer:{},Seller:{},Electricity:{},Price:{}#####\n  '.format(buy_user,sell_user,val_electric,input_couchDB['Unit_Price']).encode())	
						print ('Transaction Done!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

						lock.release()
						 #连接调度中心
						sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
						sock.connect(('192.168.1.100', 7000))
						print(sell_user)
						if sell_user == 'g':
							diaodu = '#1;plant_{};load_{};{};{} {};{}*'.format(sell_user,buy_user,trans_time[0][20:30],trans_time[0][:10],trans_time[0][11:19],val_electric)
							input_couchDB['Buyer'] = 'load_{}'.format(buy_user)
							input_couchDB['Seller'] = 'plant_{}'.format(sell_user)		
						elif sell_user == 'f':
							diaodu = '#1;plant_{};load_{};{};{} {};{}*'.format(sell_user,buy_user,trans_time[0][20:30],trans_time[0][:10],trans_time[0][11:19],val_electric)
							input_couchDB['Buyer'] = 'load_{}'.format(buy_user)
							input_couchDB['Seller'] = 'plant_{}'.format(sell_user)							
						else:
							diaodu = '#1;load_{};load_{};{};{} {};{}*'.format(sell_user,buy_user,trans_time[0][20:30],trans_time[0][:10],trans_time[0][11:19],val_electric)
							input_couchDB['Buyer'] = 'load_{}'.format(buy_user)
							input_couchDB['Seller'] = 'load_{}'.format(sell_user)
						input_couchDB_json = json.dumps(input_couchDB)
						list_couch = []
						list_couch.append(input_couchDB)
						print(input_couchDB_json)		
						print ('  ####Transaction Complete! Buyer:{},Seller:{},Electricity:{},Price:{}#####\n  '.format(buy_user,sell_user,val_electric,input_couchDB['Unit_Price']))				
						#print(diaodu)
						sock.send(diaodu.encode())   
						#data_recv_diaodu = sock.recv(1024)  
						#print ('调度中心:',data_recv_diaodu.decode())
						sock.close()			
					break
				db.update(list_couch)	
				#lock.release()	
			else:
				print ('###Error Input!!!###')
				break
		elif  length == 3 and data_recv[0] != 'f' and data_recv[0] != 'g' and data_recv[-1]== 'charge':
			data_list = ['0','0','0','0','0','0','0','0','0']
			data_list[name_list.index(data_recv[0])] = data_recv[1]
			data_list[8] = data_recv[2]
			data_a = data_list[0]
			data_b = data_list[1] 
			data_c = data_list[2]
			data_d = data_list[3]
			data_f = data_list[4]
			data_g = data_list[5]
			data_e = data_list[6]
			data_p = data_list[7]
			data_z = data_list[8]
			#print(data_list)
			charge_info = 0			
			for cc in data_list:
				if cc == '0':
					charge_info = charge_info + 1
				else:
					continue
			if  charge_info == 7 :
				reply1 = '  ####Receive Transation Info,Transacting...Please wait.....####  \n'
				#conn.sendall(reply1.encode())
				lock.acquire() 
				#config change
				old_file ='$GOPATH/src/github.com/hyperledger/fabric/fabric-sdk-node/test/integration/e2e/config.json'
				f =open(old_file,'r+')
				flist=f.readlines()
				flist[53]='	         "{}",\n'.format(data_a)
				flist[54]='	         "{}",\n'.format(data_b)
				flist[55]='	         "{}",\n'.format(data_c)
				flist[56]='	         "{}",\n'.format(data_d)
				flist[57]='	         "{}",\n'.format(data_f)
				flist[58]='	         "{}",\n'.format(data_g)
				flist[59]='	         "{}",\n'.format(data_e)
				flist[60]='	         "{}",\n'.format(data_p)
				flist[61]='	         "{}"\n'.format(data_z)
				f=open(old_file,'w+')
				f.writelines(flist)
				f.close()
				#change done 
				for i in range(1,4):
					trans_info = subprocess.Popen('$GOPATH/src/github.com/hyperledger/fabric/fabric-sdk-node/test/integration/e2e/script.sh',stdout = subprocess.PIPE,shell =True).stdout.read()
					if  trans_info.decode().find('# pass  12') <0:
						retry_info = '  ####Have tried Transaction For {} Times!!!!!!!!####\n  '.format(i)
						print (retry_info)
						sleep(1)				
						if i == 3:
							failed_info = '   ###Transaction failed!!!!!!####\n  '
							print (failed_info)
							conn.sendall('Falied'.encode())
						continue
					else:
						trans_result_a =list()
						trans_result_b =list()
						trans_result_c =list()
						trans_result_d =list()
						trans_result_f =list()
						trans_result_g =list()
						trans_result_e =list()
						trans_result_p =list()
						trans_time = list()
						result_all = list()
						befoe_list = [0,0,0,0]
						next_list = [0,0,0,0]
						result_list = list()
						result_dict = {}
						buy_user = ''
						sell_user = ''
						buy_val = ''
						sell_val = ''
						input_couchDB_json = ''
						input_couchDB = {}				
						docker_info = subprocess.Popen('$GOPATH/src/github.com/hyperledger/fabric/fabric-sdk-node/test/integration/e2e/query1.sh',stdout = subprocess.PIPE,shell =True).stdout.readlines()
						for line in docker_info:
							line = line.strip().decode()
							if '###########' in line or 'Query' in line:
								continue
							result_all.append(line)
						for line in result_all:
							line_list = line.split(',')
							trans_result_a.append(float(line_list[0][38:]))
							trans_result_b.append(float(line_list[1][8:]))
							trans_result_c.append(float(line_list[2][8:]))
							trans_result_d.append(float(line_list[3][8:]))
							trans_result_f.append(float(line_list[4][8:]))
							trans_result_g.append(float(line_list[5][8:]))
							trans_result_e.append(float(line_list[6][15:]))
							trans_result_p.append(float(line_list[7][9:]))
							trans_time.append(line_list[0][:30])
						del trans_time[0]
						trans_time.reverse()
						val_electric = trans_result_e[-1]
						val_price =  trans_result_p[-1]
						next_list = [trans_result_a[-1],trans_result_b[-1],trans_result_c[-1],trans_result_d[-1],trans_result_f[-1],trans_result_g[-1]]
						if len(result_all) > 1:
							befoe_list = [trans_result_a[-2],trans_result_b[-2],trans_result_c[-2],trans_result_d[-2],trans_result_f[-2],trans_result_g[-2]]
						for (l,m) in zip(befoe_list,next_list):
							result_list.append(m-l)
						result_dict = dict(zip(name_list,result_list))
						result_list = list()							
						for i in result_dict:
							if result_dict[i] > 0:
								charge_user = i
								charge_val = result_dict[i]
							else:
								continue
						input_couchDB['Charger'] = 'load_{}'.format(charge_user)		#TO DO
						input_couchDB['Date'] = trans_time[0][:10]
						input_couchDB['Time'] = trans_time[0][11:19]
						#input_couchDB['Meta'] = trans_time[0][20:30]
						input_couchDB['Charge value'] = round(charge_val,2)
						input_couchDB_json = json.dumps(input_couchDB)
						#conn.sendall(input_couchDB_json.encode())
						conn.sendall('Success'.encode())
						print ('  ####Charge Complete! Charger:{},Charge Value:{}#####\n  '.format(charge_user,charge_val))
						print ('  ####Charge Done####!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
						list_couch = []
						list_couch.append(input_couchDB)
						print(input_couchDB_json)
					break
				db.update(list_couch)	
				lock.release()	
			else:
				print ('###Error Input!!!###')
				break
		elif  length == 3 and data_recv[0] == 'f':
			print('error input plant can not charge')
			break
		elif  length == 3 and data_recv[0] == 'g':
			print('error input plant can not charge')
			break
		elif  data_recv[0] == 'query' and length == 2:   # query should be fixed, use coudb view()
			result_all = list()
			trans_result_a =list()
			trans_result_b =list()
			trans_result_c =list()
			trans_result_d =list()
			trans_result_e =list()
			trans_result_p =list()
			trans_time = list()
			result_list = list()		
			befoe_list = [0,0,0,0]
			next_list = [0,0,0,0]
			result_dict = {}
			buy_user = ''
			sell_user = ''
			buy_val = ''
			sell_val = ''
			input_couchDB_query_json = ''
			input_couchDB_query = {}
			trans_form = 'Charge'					
			docker_info = subprocess.Popen('$GOPATH/src/github.com/hyperledger/fabric/fabric-sdk-node/test/integration/e2e/query1.sh',stdout = subprocess.PIPE,shell =True).stdout.readlines()
			for line in docker_info:
				line = line.strip().decode()
				if '###########' in line or 'Query' in line:    ##need to fix  it is for4 ,now for 6, maybe delete
					continue
				result_all.append(line)
			for line in result_all:
				line_list = line.split(',')
				trans_result_a.append(float(line_list[0][38:]))
				trans_result_b.append(float(line_list[1][8:]))
				trans_result_c.append(float(line_list[2][8:]))
				trans_result_d.append(float(line_list[3][8:]))
				trans_result_e.append(float(line_list[4][14:]))
				trans_result_p.append(float(line_list[5][9:]))
				trans_time.append(line_list[0][:30])
			del trans_time[0]
			trans_time.reverse()			
			for j in range(min(len(trans_time),float(data_recv[1]))):				
				val_electric = trans_result_e[-j-1]
				val_price =  trans_result_p[-j-1]
				next_list = [trans_result_a[-j-1],trans_result_b[-j-1],trans_result_c[-j-1],trans_result_d[-j-1]]
				if len(result_all) > 1:
					befoe_list = [trans_result_a[-j-2],trans_result_b[-j-2],trans_result_c[-j-2],trans_result_d[-j-2]]
				for (l,m) in zip(befoe_list,next_list):
					result_list.append(m-l)
				result_dict = dict(zip(name_list,result_list))
				result_list = list()
				for i in result_dict:
					if result_dict[i] < 0:
						buy_user = i
						buy_val = abs(result_dict[i])
						trans_form = 'Deal'
					elif result_dict[i] > 0:
						sell_user = i
						sell_val = abs(result_dict[i])
					else:
						continue
				if trans_form == 'Deal':	
					input_couchDB_query['Buyer'] = buy_user
					input_couchDB_query['Seller'] = sell_user
					input_couchDB_query['Date'] = trans_time[j][:10]
					input_couchDB_query['Time'] = trans_time[j][11:19]
					#input_couchDB_query['Meta'] = trans_time[j][20:30]
					input_couchDB_query['Total_Price'] = round(buy_val,2)
					input_couchDB_query['KW/h']	 = 	val_electric
					input_couchDB_query['Unit_Price'] = val_price
					input_couchDB_query_json = json.dumps(input_couchDB_query)
				else:
					input_couchDB_query['Charger'] = sell_user		
					input_couchDB_query['Date'] = trans_time[0][:10]
					input_couchDB_query['Time'] = trans_time[0][11:19]
					#input_couchDB_query['Meta'] = trans_time[0][20:30]
					input_couchDB_query['Charge value'] = round(sell_val,2)
					input_couchDB_query_json = json.dumps(input_couchDB_query)
				print (input_couchDB_query_json)
				conn.sendall(input_couchDB_query_json.encode())
			print ('############Query Done!!!!!!!!##############')
			conn.sendall ('############Query Done!!!!!!!!##############'.encode())			
		else:
			break		
	error_input = 'Error'
	conn.sendall(error_input.encode())
	conn.close()

#now keep talking with the client
while True:
	try:
		#wait to accept a connection - blocking call
		conn, addr = s.accept()
		print ('Connected with ' + addr[0] + ':' + str(addr[1]))
		    
		#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
		_thread.start_new_thread(clientthread ,(conn,))
	except KeyboardInterrupt:
		reset() 
s.close()