import json
import numpy as np
import urllib3
import pandas
import cleanUp
import time

# unless testnet required, network is always mainnet
network = str("mainnet")
http = urllib3.PoolManager()
url = str("https://rest.cryptoapis.io/v2/blockchain-data/")
mUrl = str("https://rest.cryptoapis.io/market-data/exchange-rates/by-symbols/")

# test inputs - will be part of menus
chain = str("ethereum")
address = str("0x938A75511F44325b9a5EB75eBe445BBaeb29F305")
what = str("bal") # tx = transactions, bal = balances
name = str("SITG")
chains = "bitcoin","ethereum"


#CryptoAPIs keys
def getHeaders():

    headers = {
    'Content-Type': "application/json",
    'X-API-Key': "02c685e06072bc14c5b75e6ea3e59dd7ffd21b87" # change API key to company 
    }

    return headers

def reqcAPI(chain,address,what,name): # constructors for balance/transaction request URL

    if what == "bal": # for grabbing portfolio
        cBal = str(f'/balance?context={name}') # const balance
        if chain == "ethereum":
            cTok = str(f'/tokens?context={name}&limit=50&offset=0') # const ERC-20 balance

            reqBal = url+chain+"/"+network+"/addresses/"+address+cBal
            reqTok = url+chain+"/"+network+"/addresses/"+address+cTok
            return reqBal, reqTok # return request URLs: L1 bal (e.g. ETH), token bal
        
        reqBal = url+chain+"/"+network+"/addresses/"+address+cBal
        print(reqBal)
        return reqBal
    
    if what == "tx": # for grabbing transactions

        what = str("transactions")
        limit = "&limit=50&offset=0" # transaction limit defaulted to 100
        address = f'/addresses/{address}'
        reqTx = str(f'{url}{chain}/{network}{address}/{what}?context={name}{limit}')
        return reqTx

# Sample JSON data

def cAPIBal(chain,address,what,name): 

    headers = getHeaders()


    if chain == "ethereum" and what == "bal" :
        reqs = reqcAPI(chain,address,what,name)
        req1 = http.request("GET",reqs[0], headers=headers) # return L1 token balance
        req2 = http.request("GET",reqs[1], headers=headers) # returns other tokens balance
        json_data = req1.data.decode("utf-8"),req2.data.decode("utf-8") # decode response

        data_dict = [0,0]
        data_dict[0],data_dict[1] = json.loads(json_data[0]),json.loads(json_data[1])
        eth_data = data_dict[0]["data"]["item"]
        reformat_eth = {
                            "contractAddress": "No Contract!",
                            "type": "ERC-20",
                            "confirmedBalance": eth_data["confirmedBalance"]["amount"],
                            "name": "Ether",
                            "symbol": "ETH"
                        }
        
        data_dict[1]["data"]["items"].append(reformat_eth)
        data_dict = data_dict[1]
        return data_dict
    else:
        reqs = reqcAPI(chain,address,what,name)
        reqs = http.request("Get", reqs, headers=headers)
        json_data = reqs.data.decode("utf-8")
        data_dict = json.loads(json_data)
        return data_dict

# Parse the JSON data
json_data = cAPIBal(chain,address,what,name)



# Format the data
items = (json_data)

# Write the formatted data to a JSON file
with open("formatted_data.json", "w") as outfile:
    json.dump(items, outfile, indent=4)

print("Formatted data has been stored in 'formatted_data.json'.")

with open("formatted_data.json", "r") as infile:
    data = json.load(infile)
    try:
        for i in range(len(data["data"]["items"])):
            print(data["data"]["items"][i]["symbol"], data["data"]["items"][i]["confirmedBalance"])
    except TypeError:
        print(data["data"]["item"]["unit"], data["data"]["item"]["amount"])


    
