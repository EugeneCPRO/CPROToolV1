import asyncio
from clean_term import wipe
from crypto_data_updater import CryptoDataUpdater
from crypto_apis_call import WalletDataProcessor

import pymongo


wipe()

# test inputs - will be part of menus
what = str("bal") # tx = transactions, bal = balances
name = str(input("Enter your name: "))
address = str(input("Enter your address: "))
wipe()

# Replace with your MongoDB connection details
mongo_uri = "mongodb+srv://eugened:jO5F7L1PU1VL1fh1@walletdb.yzkhawm.mongodb.net/?retryWrites=true&w=majority"
database_name = "user_wallet_balances"  # Replace with the name of the database you want to check
collection_name = name

def checkData(database_name,collection_name):
    try:
        # Connect to the MongoDB server
        client = pymongo.MongoClient(mongo_uri)

        # Access the specified database
        database = client[database_name]

        # Check if the collection exists within the database
        if collection_name in database.list_collection_names():
            print(f"The collection '{collection_name}' exists in the database '{database_name}'.")
        else:
            print(f"The collection '{collection_name}' does not exist in the database '{database_name}'.")

        # Close the MongoDB connection
        client.close()

    except Exception as e:
        print(f"An error occurred: {str(e)}")

# launch app
if __name__ == '__main__':
    # check if user data exists
    checkData(database_name,collection_name)
    # format and store wallet data
    processor = WalletDataProcessor(address,what,name)
    processor.fetch_and_store_data()

    # run price updates
    updater = CryptoDataUpdater(
        'wss://ws.coincap.io/prices?assets=ALL',
        'priceData.json',
        'coin_data.json',
        'thirdFile.json'
    )
    asyncio.run(updater.main())


#callAPI.cAPIBal(chain,address,what,name)
# portfolio = finGet.getAssets(chain,address,what,name)
# print(portfolio)
# portValue = finGet.balValue(portfolio, name)
# print(portValue)
# testUI.update_values(portfolio,portValue,name,chain)


