from google import genai
import numpy as np

client = genai.Client(api_key="AIzaSyDHplAkV-apzuKHJJWblc6uZtTSxApA2GI")

arr = ['wer', 'sdf']

result = client.models.embed_content(
        model="models/text-embedding-004",
        contents=arr,
)

print(result.embeddings[0].values)
