import json

class Price:
    def __init__(self, job):
        self.job = job

    def info(self):
        data = None
        print("Loading data from JSON file...")
        with open('backend/price.json') as f:
            data = json.load(f)
        response = []
        for place in data['prices']:
            for item in place['operation']:
                if item['name'] == self.job:
                    response.append([place['name'], place['latitude'], place['longitude'], item['price']])
        print(response)
        return response