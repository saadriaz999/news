import streamlit as st
# import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity
# import cohere
# import ast
import pandas as pd


# Load in the dataframe from S3 containing the csv file that contains our current news data
# this is neccessary primarily for performance reasons

# df_news = pd.read_csv('news_data.csv)')



# co = cohere.Client('tHOKvUc9kU3iiZ3CDuMuPdJQn9Wwj1qwZKbG256D')

# def generate_embedding(content):
#     if content:
#         response = co.embed(texts=[content], model='embed-english-v2.0')
#         return response.embeddings[0]
#     return None
#
# def convert_embedding(embed):
#     embedding_list = ast.literal_eval(embed)
#     return np.array(embedding_list, dtype=float)

# df_news['Embedding'] = df_news['Embedding'].apply(convert_embedding)


def get_top_k_similar_articles(query, df, k=3):
    # query_embedding = np.array(generate_embedding(query)).reshape((1, -1))
    # df_filtered = df[df['Embedding'].notnull()].copy()
    # embeddings = np.stack(df_filtered['Embedding'].values)
    # similarities = cosine_similarity(query_embedding, embeddings).flatten()
    # df_filtered['Similarity'] = similarities
    # top_k = df_filtered.sort_values('Similarity', ascending=False).head(k)
    # return top_k
    return ['a1', 'a2', 'a3']


def cohere_prompt(prompt, model='command', max_tokens=300):
    # response = co.generate(
    #     model=model,
    #     prompt=prompt,
    #     max_tokens=max_tokens
    # )
    # return response.generations[0].text.strip()
    return 'cohere_response'

def generate_summaries(query, df, k=5):
    return 'extractive_summary', 'abstractive_summary'
    # # Get top-k articles
    # top_k_articles = get_top_k_similar_articles(query, df, k)
    #
    # # Extractive summaries
    # extractive_summaries = "ARTICLE: " + "\n\nARTICLE: ".join(top_k_articles['Extractive Summary'].values)
    # extractive_prompt = f"Summarize the following articles into a cohesive extractive summary in under 200 words with proper flow. It should have something from each article:\n{extractive_summaries}"
    #
    # # Abstractive summaries
    # abstractive_summaries = "ARTICLE: " + "\n\nARTICLE: ".join(top_k_articles['Abstractive Summary'].values)
    # abstractive_prompt = f"Summarize the following articles into a cohesive abstractive summary in under 200 words with proper flow. It should have something from each article:\n{abstractive_summaries}"
    #
    # print("EXTRACTIVE PROMPT:\n", extractive_prompt)
    # extractive_summary = cohere_prompt(extractive_prompt)
    #
    # print("\n\nABSTRACTIVE PROMPT:\n", abstractive_prompt)
    # abstractive_summary = cohere_prompt(abstractive_prompt)
    #
    # return extractive_summary, abstractive_summary


st.title("News Summarizer")

# Button to clear chat history
if st.button("Clear Chat"):
    st.session_state.messages = []

# Initialize chat history if not already initialized
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Please Enter a News Topic"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    sum1, sum2 = "a", "b"
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown('Extractive Summary\n')
        st.markdown(sum1)
        st.markdown('Abstractive Summary\n')
        st.markdown(sum2)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": sum1})
