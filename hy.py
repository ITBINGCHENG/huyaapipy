#encoding=utf-8
from websocket import create_connection
import hashlib
import time, threading
import json
import secret
import sys

room = sys.argv[1]  #接受命令行参数
t = time.strftime("%Y%m%d-%H%M%S", time.localtime())
data='{"roomId":%s}'%(room)
appId=secret.appId
key=secret.key

# Tips
# 此处必须声明encode
# 若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing

def sock():
	hl = hashlib.md5()
	times = str(int(time.time()))  # 秒级时间戳
	strmd5 = 'data='+data+'&key='+key+'&timestamp='+times
	hl.update(strmd5.encode(encoding='utf-8'))
	sign = hl.hexdigest()
	socket =create_connection("ws://openapi.huya.com/index.html?do=getMessageNotice&data="+data+"&appId="+appId+"&timestamp="+times+"&sign="+sign)
	return socket

def send1():
	global socket
	while True:
		try:
			time.sleep(15)
			socket.send("ping")##发送消息
		except:
			#socket= sock()
			continue
	
def recv1():
	global socket
	while True:
		try:
			dic = socket.recv().encode('utf-8')#接收消息转变编码为utf-8
			with open("./%sdanmu.json"%(t), "ab+") as f:#存储弹幕原始数据
				f.write(dic)
			js = json.loads(dic)#字符串转字典
			#print(js)
			print("["+js["data"]['sendNick']+"]:"+js['data']["content"])
		except Exception as e:
			print(e)
			socket = sock()
			continue
	f.close()
	

socket=sock()
t1 = threading.Thread(target=send1)
t2 = threading.Thread(target=recv1)
t1.start()
t2.start()
t1.join()
t2.join()
print("end")
