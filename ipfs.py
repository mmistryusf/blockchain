import requests
import json


def pin_to_ipfs(data):
	assert isinstance(data,dict), f"Error pin_to_ipfs expects a dictionary"
	#YOUR CODE HERE
	headers = {
		'pinata_api_key':  '4b2fee85e6025caf6666',
		'pinata_secret_api_key' : '23286651dc8d0b157b790fb864b9fd8c16684bb16e412f665bf12d9861c4d4c7'
	}
	
	url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
	#payload = json.dumps(data)
	response = requests.request("POST", url, json=data, headers = headers)
	#print(response)
	if response.status_code == 200:
		ipfs_hash = response.json()['IpfsHash']
		
		return str(ipfs_hash)
	else:
		Exception(f"Failed to pin Json data:{response.text}")

def get_from_ipfs(cid,content_type="json"):
	assert isinstance(cid,str), f"get_from_ipfs accepts a cid in the form of a string"
	#YOUR CODE HERE	
	url = f"https://ipfs.io/ipfs/{cid}"
	response = requests.get(url)
	# if response.status_code == 200:
	data = response.json()
	assert isinstance(data,dict), f"get_from_ipfs should return a dict"
	return data
