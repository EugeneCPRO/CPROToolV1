import asyncio
import json
import websockets

class CryptoDataUpdater:
    def __init__(self, websocket_url, json_file, second_file, third_file, save_interval=5):
        self.websocket_url = websocket_url
        self.json_file = json_file
        self.second_file = second_file
        self.third_file = third_file
        self.crypto_data = {}
        self.symbol_to_id_mapping = {}  # To store "symbol" to "id" mapping from the second file
        self.save_interval = save_interval  # Set the interval for saving data (in seconds)

    async def on_message(self, websocket, path):
        async for message in websocket:
            try:
                data = json.loads(message)

                for asset, price in data.items():
                    
                    # Check if the price has changed
                    if self.crypto_data.get(asset) is None:
                        # Create a new entry if it doesn't exist
                        self.crypto_data[asset] = {'price': float(price)}
                    else:
                        # Update the price if the entry exists
                        self.crypto_data[asset]['price'] = float(price)

            except Exception as e:
                print(f"Error: {str(e)}")

    async def load_second_file_data(self):
        try:
            with open(self.second_file, 'r') as file:
                second_file_data = json.load(file)
                # Create a mapping from "symbol" to "id" (swapping "ticker" and "name")
                self.symbol_to_id_mapping = {entry["symbol"]: entry["id"] for entry in second_file_data}
        except FileNotFoundError:
            pass  # File doesn't exist, start with an empty mapping

    async def save_data_periodically(self):
        while True:
            await asyncio.sleep(self.save_interval)
            # Combine data from the WebSocket and the second file, and save it to the third file
            combined_data = []

            for asset, data in self.crypto_data.items():
                id = self.symbol_to_id_mapping.get(asset)
                if id:
                    combined_entry = {
                        "ticker": asset,  # Swapping "ticker" and "name" here
                        "name": id,  # Swapping "ticker" and "name" here
                        "id": id,
                        "price": data["price"]
                    }
                    combined_data.append(combined_entry)

            with open(self.third_file, 'w') as file:
                json.dump(combined_data, file, indent=4)

    async def run_websocket(self):
        while True:
            try:
                async with websockets.connect(self.websocket_url) as websocket:
                    await websocket.send('{"method":"subscribe","topic":"market-all","market":"ALL"}')
                    await self.on_message(websocket, None)
            except websockets.exceptions.ConnectionClosedError:
                print("Connection closed unexpectedly. Reconnecting...")
                await asyncio.sleep(5)  # Sleep for a while before attempting to reconnect
            except Exception as e:
                print(f"Error during WebSocket connection: {str(e)}")

    async def main(self):
        # Load the data from the second file
        await self.load_second_file_data()

        # Start the WebSocket connection and data saving tasks
        asyncio.create_task(self.run_websocket())
        asyncio.create_task(self.save_data_periodically())

        # Your program can continue executing other tasks here
        while True:
            await asyncio.sleep(1)  # Perform other tasks and sleep to avoid busy-waiting

# Usage:
if __name__ == "__main__":
    updater = CryptoDataUpdater(
        'wss://ws.coincap.io/prices?assets=ALL',
        'priceData.json',
        'coin_data.json',
        'new_test_File.json'
    )
    asyncio.run(updater.main())
