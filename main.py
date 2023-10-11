
from clean_term import wipe
from price_data.crypto_data_updater import CryptoDataUpdater
from wallet_data_manipulation.crypto_apis_call import WalletDataProcessor
from wallet_data_manipulation.merge_wallet_balances import WalletDataMerger
from wallet_data_manipulation.user_prices import updatePortVal

wipe()

testdata = input("Use previous data?")
if testdata == "y":
    name = str("SITG")
else:
    # test inputs - will be part of menus
    what = str("bal") # tx = transactions, bal = balances
    name = str(input("Enter your name: "))
    address = str(input("Enter your address: "))

wipe()

# Replace with your MongoDB connection details
mongo_uri = "mongodb+srv://eugened:jO5F7L1PU1VL1fh1@walletdb.yzkhawm.mongodb.net/?retryWrites=true&w=majority"
database_name = "user_wallet_balances"  # Replace with the name of the database you want to check
collection_name = name



# launch app
if __name__ == '__main__':
    if testdata =="y":
        pass
    else:
        # format and store wallet data
        processor = WalletDataProcessor(address,what,name)
        processor.fetch_and_store_data()

    # merge any balances
    wallet_merger = WalletDataMerger(name)  # Replace with the desired name
    wallet_merger.merge_wallet_data()

    # calculate portfolio values
    portfolio = updatePortVal(name)

    # # run price updates
    # updater = CryptoDataUpdater(
    #     'wss://ws.coincap.io/prices?assets=ALL',
    #     'priceData.json',
    #     'coin_data.json',
    #     'ticker_price_list.json'
    # )
    # asyncio.run(updater.main())

