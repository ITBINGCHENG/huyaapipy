# -*- coding: UTF-8 -*-
from websocket import create_connection #模块名为websocket_client
import hashlib
import time, threading
import json
import secret   #不宜公开信息

data = '{"roomId":11342412}'
appId=secret.appId
key=secret.key


# Tips
# 此处必须声明encode
# 若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing

def sock():
	hl = hashlib.md5()
	times = str(int(time.time()))  # 秒级时间戳
	strmd5 = 'data=' + data + '&key=' + key + '&timestamp=' + times
	hl.update(strmd5.encode(encoding='utf-8'))
	sign = hl.hexdigest()
	socket = create_connection(
		"ws://openapi.huya.com/index.html?do=getMessageNotice&data=" + data + "&appId=" + appId + "&timestamp=" + times + "&sign=" + sign)
	return socket


def send1():
	global socket
	while True:
		try:
			time.sleep(15)
			socket.send("ping")  ##发送消息
		except:
			# socket= sock()
			continue


def recv1():
	global socket
	while True:
		try:
			dic = socket.recv()
			print(type(dic))
			print(dic)
		except Exception as e:
			print(e)
			socket = sock()
			continue
	f.close()


socket = sock()
t1 = threading.Thread(target=send1)
t2 = threading.Thread(target=recv1)
t1.start()
t2.start()
t1.join()
t2.join()
print("end")
