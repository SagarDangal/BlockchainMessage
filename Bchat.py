import requests
import json
import base64
import sys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding



arg=sys.argv
host='http://167.71.235.236:5000/'

with open('private_key.pem', "rb") as file:
        	# read all file data
    		file_data = file.read()
    		decrypt_key = serialization.load_pem_private_key(
            file_data,
            password=None,
            backend=default_backend()
            )
with open('public_key.pem', "rb") as file:
        	# read all file data
    		public = file.read()


if sys.argv[1]== '-h':
	print("Uses[+] python3 Bchat.py --send 'message' --p 'path to receiver public addr'") 
	print("Usee[+] python3 Bchat --recv")   		

if len(sys.argv)>=4:
	if sys.argv[3]=='--p':
		with open(sys.argv[4], "rb") as file:
        	# read all file data
    			file_data = file.read()
    			key = serialization.load_pem_public_key(
            	file_data,
            	backend=default_backend()
        )
	sender_addr=file_data
	

def Encryption(message,key):
	encrypted = key.encrypt(
	    message,
	    padding.OAEP(
	        mgf=padding.MGF1(algorithm=hashes.SHA256()),
	        algorithm=hashes.SHA256(),
	        label=None
	    )

	)
	return encrypted




def Decrypting(message,key):
	original_message = key.decrypt(
	    message,
	    padding.OAEP(
	        mgf=padding.MGF1(algorithm=hashes.SHA256()),
	        algorithm=hashes.SHA256(),
	        label=None
	    )

	)
	return original_message


if sys.argv[1]=='--send':
	if len(sys.argv[2])>>190:
		print("your message is too long")
		exit()
		
	encripted = Encryption(bytes(sys.argv[2],encoding='utf8'),key)

	#print(type(encripted.decode("utf-8")))
	url = host+'mine_block'
	myobj = {
            "from": str(public),
            "to": str(sender_addr),
            "msg": base64.b64encode(encripted),
        }

	#myobj=base64.b64encode(encripted)

	x = requests.post(url, json = myobj)
elif sys.argv[1]=='--recv':
	x = requests.get(host+'get_chain')
	data='no message'
	for i in range(x.json()["length"]-1):
		if x.json()["chain"][i+1]["data"]["to"] == str(public):
			decrypt_message=Decrypting(base64.b64decode(x.json()["chain"][i+1]["data"]["msg"]),decrypt_key)
			data = {
            	"from": str(x.json()["chain"][i+1]["data"]["from"]),
            	"to": str(x.json()["chain"][i+1]["data"]["to"]),
            	"decrypt_msg": decrypt_message
        	}

			print(data)
