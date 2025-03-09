import json
class Symptom:
    def __init__(self, symptoms):
        self.symptoms = symptoms

    def info(self):
        with open('backend/symptoms.json', 'r') as f:
            data = json.load(f)
        
        response = []
        for symptom in self.symptoms:
            for item in data['symptoms']:
                if item['name'].lower() == symptom.lower():
                    response.append(item['recommendation'])
                    break
        return json.dumps(response)