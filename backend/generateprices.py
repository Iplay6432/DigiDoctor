import json
import random

# Filepath to the JSON file
filepath = 'price.json'

# Function to adjust the price slightly higher or lower
def adjust_price(price):
    adjustment = random.uniform(-0.1, 0.1)  # Adjust by up to ±10%
    new_price = price * (1 + adjustment)
    return round(new_price, 2)  # Round to 2 decimal places

# Read the JSON file
with open(filepath, 'r') as file:
    data = json.load(file)

# Adjust the prices
for hospital in data['prices']:
    for operation in hospital['operation']:
        operation['price'] = adjust_price(operation['price'])

# Write the updated data back to the JSON file
with open(filepath, 'w') as file:
    json.dump(data, file, indent=4)

print("Prices have been adjusted.")