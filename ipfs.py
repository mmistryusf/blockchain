import requests
import json


def pin_to_ipfs(data):
	assert isinstance(data,dict), f"Error pin_to_ipfs expects a dictionary"
	#YOUR CODE HERE
	url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"	
	headers = {		
		"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiI0YTdjYjliYi0xNzUwLTQ2NjktOTg1Yi03MzU5YTY5OWIxM2EiLCJlbWFpbCI6Im1taXN0cnlAc2Vhcy51cGVubi5lZHUiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicGluX3BvbGljeSI6eyJyZWdpb25zIjpbeyJkZXNpcmVkUmVwbGljYXRpb25Db3VudCI6MSwiaWQiOiJGUkExIn0seyJkZXNpcmVkUmVwbGljYXRpb25Db3VudCI6MSwiaWQiOiJOWUMxIn1dLCJ2ZXJzaW9uIjoxfSwibWZhX2VuYWJsZWQiOmZhbHNlLCJzdGF0dXMiOiJBQ1RJVkUifSwiYXV0aGVudGljYXRpb25UeXBlIjoic2NvcGVkS2V5Iiwic2NvcGVkS2V5S2V5IjoiNGIyZmVlODVlNjAyNWNhZjY2NjYiLCJzY29wZWRLZXlTZWNyZXQiOiIyMzI4NjY1MWRjOGQwYjE1N2I3OTBmYjg2NGI5ZmQ4YzE2Njg0YmIxNmU0MTJmNjY1YmYxMmQ5ODYxYzRkNGM3IiwiZXhwIjoxNzUxNTg1OTU0fQ.BOWstVMMR7C6YhxkO975Ca-ZnaPz56WLZNKlrBF6FgQ",
		"Content-Type": "application/json"		
	}	
	response = requests.request("POST", url, json=data, headers = headers)
	
	if response.status_code == 200:
		ipfs_hash = response.json()['IpfsHash']		
		return ipfs_hash
	else:
		Exception(f"Failed to pin Json data:{response.text}")

def get_from_ipfs(cid,content_type="json"):
	assert isinstance(cid,str), f"get_from_ipfs accepts a cid in the form of a string"
	#YOUR CODE HERE	
	url = f"https://gateway.moralisipfs.com/ipfs/{cid}"
	response = requests.get(url)
	# if response.status_code == 200:
	data = response.json()
	assert isinstance(data,dict), f"get_from_ipfs should return a dict"
	return data
