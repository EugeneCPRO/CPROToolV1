import pymongo
import re
class WalletDataMerger:
    def __init__(self, name):
        # Replace with your MongoDB connection details
        self.mongo_uri = "mongodb+srv://eugened:jO5F7L1PU1VL1fh1@walletdb.yzkhawm.mongodb.net/?retryWrites=true&w=majority"
        self.name = name
        self.database_name = "user_wallet_balances"
        self.collection_name = self.name  # Use the provided name as the collection name

    def clean_data(self, data):
        # Regular expression pattern to match alphanumeric keys
        alphanumeric_pattern = re.compile(r'^[a-zA-Z0-9_]+$')

        cleaned_data = {}
        for key, value in data.items():
            if (
                alphanumeric_pattern.match(key) and
                len(key) <= 7 and
                value.get("confirmedBalance", 0) != 0
            ):
                cleaned_data[key] = value
        return cleaned_data


    def merge_wallet_data(self):
        # Initialize the MongoClient
        client = pymongo.MongoClient(self.mongo_uri)

        # Access the database and collection
        db = client[self.database_name]
        collection = db[self.collection_name]

        # Create an empty dictionary to store merged data
        merged_data = {
            "_id": "TotalBalance",  # Set the "_id" field for the merged document
            "data": {}  # Initialize an empty dictionary for data
        }

        # Fetch all documents in the collection
        cursor = collection.find({})

        # Iterate through all documents and merge their data into the "TotalBalance" document
        for document in cursor:
            # Extract the data you want to merge (customize as needed)
            data_to_merge = document.get("data", {})

            # Clean the data before merging
            cleaned_data = self.clean_data(data_to_merge)

            # Iterate through the cleaned data and merge it into the "TotalBalance" document
            for key, value in cleaned_data.items():
                if key in merged_data["data"]:
                    # If the key already exists, update the value (e.g., add balances)
                    merged_data["data"][key].update(value)
                else:
                    # If the key doesn't exist, create it with the current value
                    merged_data["data"][key] = value

        # Insert or update the "TotalBalance" document in the collection
        result = collection.update_one(
            {"_id": "TotalBalance"},
            {"$set": merged_data},
            upsert=True
        )

        # Close the MongoDB client connection
        client.close()

        # Print a message indicating the merge is complete
        if result.upserted_id:
            print(f"{self.name} TotalBalance document created.")
        else:
            print(f"{self.name} TotalBalance document updated.")


