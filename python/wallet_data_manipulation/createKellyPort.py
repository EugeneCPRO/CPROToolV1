import json

# Load the contents of the two JSON files
with open('kelly_optimised_portfolio.json', 'r') as file1:
    data1 = json.load(file1)

with open('updated_portfolio_copy.json', 'r') as file2:
    data2 = json.load(file2)

# Update the "value" attribute in data2 with values from data1
for symbol, value in data1["Dollar Allocations"].items():
    if symbol in data2:
        data2[symbol]["value"] = value

# Save the updated data2 to a new JSON file (file3.json)
with open('kelly_optimal.json', 'w') as file3:
    json.dump(data2, file3, indent=4)

print("Updated data saved to 'kelly_optimal.json'")