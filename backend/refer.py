from transformers import pipeline
import torch
from transformers import pipeline


class Refer:
    def __init__(self, name, symptoms):
        self.name = name
        self.symptoms = symptoms
        self.generator = pipeline("text-generation", model="meta-llama/Llama-3.2-1B")
        model_id = "meta-llama/Llama-3.2-1B-Instruct"
        self.pipe = pipeline("text-generation",model=model_id,torch_dtype=torch.bfloat16,device_map="auto",)
        self.messages = [{"role": "system", "content": "You are a healthcare assistant thate based on the symptoms provided, you will determine if the patient should visit the emergency room and respond with only a'yes' or 'no'."},{"role": "user", "content": self.symptoms},]
    def gen(self):
        # Generate text based on the prompt
        prompt = f"Please respond to {self.name} using the words 'yes' or 'no'. Answer yes if this person should visit the emergency room based on the symptoms: {self.symptoms}, otherwise answer no."
        result = self.generator(prompt)
        self.outputs = self.pipe(self.messages, max_new_tokens=20,)
        return self.outputs[0]["generated_text"][-1]
