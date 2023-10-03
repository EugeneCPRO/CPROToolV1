
# storing wallet data

import pymongo
import urllib3
import json
import time

# initialisation
mongo_uri = "mongodb+srv://eugened:jO5F7L1PU1VL1fh1@walletdb.yzkhawm.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(mongo_uri)
db = client["user_wallet_balances"]
url = str("https://rest.cryptoapis.io/v2/blockchain-data/")
mUrl = str("https://rest.cryptoapis.io/market-data/exchange-rates/by-symbols/")
network = "mainnet"
http = urllib3.PoolManager()


# Sample JSON data
def default(obj):
    return list(obj)


# CryptoAPIs Headers
def getHeaders():

    headers = {
    'Content-Type': "application/json",
    'X-API-Key': "02c685e06072bc14c5b75e6ea3e59dd7ffd21b87" # change API key to company 
    }

    return headers

# automated blockchain selection based on wallet format
def identify_blockchain(address):

    address_lower = address.lower()

    if address_lower.startswith("1") or address_lower.startswith("bc1"):
        print("Network identified as: Bitcoin")
        return "bitcoin"
    elif address_lower.startswith("0x"):
        print("Network identified as: Ethereum")
        return "ethereum"
    elif address_lower.startswith("bnb"):
        print("Network identified as: Binance Smart Chain")
        return "binance-smart-chain"
    # Add more checks for other blockchains here

    return "unknown"  # Blockchain couldn't be identified

def reqcAPI(chain,address,what,name): # constructors for balance/transaction request URL

    if what == "bal": # for grabbing portfolio
        cBal = str(f'/balance?context={name}') # const balance
        if chain == "ethereum": # clause for ethereum
            cTok = str(f'/tokens?context={name}&limit=50&offset=0') # const ERC-20 balance
            reqBal = url+chain+"/"+network+"/addresses/"+address+cBal
            reqTok = url+chain+"/"+network+"/addresses/"+address+cTok
            return reqBal, reqTok # return request URLs: L1 bal (e.g. ETH), token bal
        
        reqBal = url+chain+"/"+network+"/addresses/"+address+cBal # construct balance url

        return reqBal
    
    if what == "tx": # for grabbing transactions

        what = str("transactions")
        limit = "&limit=50&offset=0" # transaction limit defaulted to 100
        address = f'/addresses/{address}'
        reqTx = str(f'{url}{chain}/{network}{address}/{what}?context={name}{limit}')
        return reqTx
        
# Function to process wallet data and save it to a file, for local output testing
def cAPIBal(chain, address, what, name):
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

        return data_dict

    else:
        reqs = reqcAPI(chain,address,what,name)
        reqs = http.request("GET", reqs, headers=headers)  
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
                        "type": data_dict["data"]["item"]["confirmedBalance"]["unit"],
                        "confirmedBalance": data_dict["data"]["item"]["confirmedBalance"]["amount"],
                        "name": data_dict["data"]["item"]["confirmedBalance"]["unit"],
                        "symbol": data_dict["data"]["item"]["confirmedBalance"]["unit"]
                    }
                ]
            }
        }

        return reformat_data

class WalletDataProcessor:
    def __init__(self, address, what, name):
        # Replace with your MongoDB connection details
        self.mongo_uri = "mongodb+srv://eugened:jO5F7L1PU1VL1fh1@walletdb.yzkhawm.mongodb.net/?retryWrites=true&w=majority"  # Replace with your MongoDB URI
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client["user_wallet_balances"]
        self.url = "https://rest.cryptoapis.io/v2/blockchain-data/"
        self.mUrl = "https://rest.cryptoapis.io/market-data/exchange-rates/by-symbols/"
        self.network = "mainnet"
        self.http = urllib3.PoolManager()

        self.chain = identify_blockchain(address)
        self.address = address
        self.what = what
        self.name = name

    # Function to fetch data from the CryptoAPIs and store it in MongoDB
    def fetch_and_store_data(self):
        # Define the API URL with the provided wallet address
        # Replace with your API key
        wallet_data = cAPIBal(self.chain, self.address, self.what, self.name)
        # wallet_data = json.dumps(wallet_data)
        # Fetch data from the API
        wallet_collection = self.db[self.name]  # Use the name as the database name

        # Insert or update wallet address data
        result = wallet_collection.update_one(
            {"_id": self.address},
            {"$set": {"data": wallet_data}},
            upsert=True
        )

        print(f'Data for address {self.address} stored successfully.')
        return result
    
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



