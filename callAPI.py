
import json
import urllib3
import time
import re
import requests

# unless testnet required, network is always mainnet
network = str("mainnet")
http = urllib3.PoolManager()
url = str("https://rest.cryptoapis.io/v2/blockchain-data/")
mUrl = str("https://rest.cryptoapis.io/market-data/exchange-rates/by-symbols/")





class callAPI(object):
    def __init__():
        return


def openFile(filename):
    try:
        with open(filename) as data:
            data = json.load(data)
        return data
    except FileNotFoundError:
        pass


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

        return reqBal
    
    if what == "tx": # for grabbing transactions

        what = str("transactions")
        limit = "&limit=50&offset=0" # transaction limit defaulted to 100
        address = f'/addresses/{address}'
        reqTx = str(f'{url}{chain}/{network}{address}/{what}?context={name}{limit}')
        return reqTx
    

# Sample JSON data
def default(obj):
    return list(obj)

def cAPIBal(chain,address,what,name): 
    directory = f'./{name}/'
    filename = f'{directory}{name}_{chain}_{what}.json'
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

        with open(filename, "w") as outfile:
            json.dump(data_dict, outfile, indent=4)

        return data_dict
    
    else:
        reqs = reqcAPI(chain,address,what,name)
        reqs = http.request("Get", reqs, headers=headers)
        json_data = reqs.data.decode("utf-8")
        data_dict = json.loads(json_data)
        
        reformat_data = {
                                "apiVersion": "2023-04-25",
                                "requestId": "65159804999496dd3cdcf9fb",
                                "context": "SITG",
                                "data": {
                                    "limit": 50,
                                    "offset": 0,
                                    "total": 1,
                                    "items": [
                                        {
                                                        "contractAddress": "No Contract!",
                                                        "type": {data_dict["data"]["item"]["confirmedBalance"]["unit"]},
                                                        "confirmedBalance": data_dict["data"]["item"]["confirmedBalance"]["amount"],
                                                        "name": {data_dict["data"]["item"]["confirmedBalance"]["unit"]},
                                                        "symbol": data_dict["data"]["item"]["confirmedBalance"]["unit"]
                                                    }
                                                                
                                                ]
                                            }
                                        }
  
        with open(filename, "w") as outfile:
            json.dump(reformat_data, outfile, indent=4, default=default)

        return data_dict
    
def cAPIPrice(ticker,base,name):
# time data
    headers = getHeaders()
    now = int(time.time())
    now = str(now)
    tstamp = "Timestamp="+str(now)
    context = f'context={name}&calculation'

    # create url
    reqUrl = f'{mUrl}{ticker}/{base}?{context}{tstamp}'
    pReq = http.request("GET", reqUrl, headers = headers)
    dec = pReq.data.decode("utf-8")
    dec = json.loads(dec)
    try:
        price = dec["data"]["item"]["rate"]
    except KeyError:
            return float(0)
    else:
        return round(float(price),2)




