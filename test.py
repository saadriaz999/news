from google import genai
# from Articles.models import Embedding
# from pgvector.django import CosineDistance

client = genai.Client(api_key="AIzaSyDHplAkV-apzuKHJJWblc6uZtTSxApA2GI")

def get_embedding(text: str):
    result = client.models.embed_content(
        model="models/text-embedding-004",
        contents=[text, text],
    )
    return result.embeddings[0].values

def get_summary(article: str):
    prompt = f"""
    Generate a summary of the following article containing content of the following news article:
    
    News Article: {article}
    
    ONLY output the summary.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    print(response.text)


article ="people ate food that was tasty"
get_summary(article)

# text = "hehe"
# embedding = get_embedding(text)
# print(embedding)
# doc = Embedding.objects.create(article_id=5, embedding=embedding)
# print(doc)
#
# results = Embedding.objects.annotate(
#     similarity=CosineDistance("embedding", embedding)
# ).order_by("similarity")[:5]
#
# for result in results:
#     print(f"{result.id} (similarity={result.similarity:.4f})")
