import json
import pymongo
from wallet_data_manipulation.cmc_api import priceCall

# Connect to MongoDB
mongo_uri = "mongodb+srv://eugened:jO5F7L1PU1VL1fh1@walletdb.yzkhawm.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(mongo_uri)

def calculate_value_for_tickers(tickers, portfolio_data):
    # Split the tickers by comma and create a list
    tickers_list = tickers.split(',')

    # Call the function to retrieve prices for the tickers
    price_data = priceCall(','.join(tickers_list))

    # Create an empty list to store the updated portfolio data
    updated_portfolio_data = []

    for asset_ticker in tickers_list:
        if asset_ticker in price_data:
            asset_info = portfolio_data[asset_ticker]

            # Calculate the value based on the confirmed balance and price
            confirmed_balance = float(asset_info["confirmedBalance"])

            # Retrieve the asset's price from the price data
            price = price_data[asset_ticker]["price"]

            value = confirmed_balance * price

            # Create an updated asset entry with the "value" field
            updated_asset_info = {
                "contractAddress": asset_info["contractAddress"],
                "type": asset_info["type"],
                "confirmedBalance": asset_info["confirmedBalance"],
                "name": asset_info["name"],
                "symbol": asset_info["symbol"],
                "value": value  # Add the calculated value
            }

            # Add the updated asset entry to the list
            updated_portfolio_data.append((asset_ticker, updated_asset_info))

    # Create a dictionary from the list of updated assets
    updated_portfolio_dict = dict(updated_portfolio_data)

    return updated_portfolio_dict

def updatePortVal(name):

    # Connect to MongoDB
    mongo_uri = "mongodb+srv://eugened:jO5F7L1PU1VL1fh1@walletdb.yzkhawm.mongodb.net/?retryWrites=true&w=majority"
    client = pymongo.MongoClient(mongo_uri)
    db = client["user_wallet_balances"]
    collection = db[name]

    # Retrieve portfolio data from MongoDB
    portfolio_data = {}
    cursor = collection.find_one({"_id": "TotalBalance"})
    if cursor and "data" in cursor:
        portfolio_data = cursor["data"]

    # Extract a list of tickers from MongoDB
    ticker_list_from_mongodb = list(portfolio_data.keys())

    # Example usage: Pass the extracted list of tickers
    updated_data = calculate_value_for_tickers(','.join(ticker_list_from_mongodb), portfolio_data)
    fp = "test.json"
    with open(fp, "w") as outfile:
        json.dump(updated_data,outfile,indent=4)

    # Save the updated portfolio data to MongoDB
    collection.update_one(
        {"_id": "TotalBalance"},
        {"$set": {"data": updated_data}},
        upsert=True
    )
    print("\nPrices Updated")

    # Close the MongoDB client connection
    client.close()
