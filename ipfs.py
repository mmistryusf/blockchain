import requests
import json
import ipfshttpclient

def pin_to_ipfs(data):
	assert isinstance(data,dict), f"Error pin_to_ipfs expects a dictionary"
	#YOUR CODE HERE
	json_data = json.dumps(data)
	client = ipfshttpclient.connect()
	cid = client.add_str(json_data)
	return cid
	return cid

def get_from_ipfs(cid,content_type="json"):
	assert isinstance(cid,str), f"get_from_ipfs accepts a cid in the form of a string"
	#YOUR CODE HERE	

	assert isinstance(data,dict), f"get_from_ipfs should return a dict"
	return data