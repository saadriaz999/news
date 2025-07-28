import requests
import streamlit as st

st.set_page_config(page_title="MyNews", page_icon="🗞️")

st.title("📰 MyNews – News Answer Assistant")

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear Chat Button
if st.button("Clear Chat"):
    st.session_state.messages = []

# Display Past Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Dropdown for day selection
date_range = st.selectbox("Select time range", options=["1 day", "7 days"])
date_range_days = 1 if date_range == "1 day" else 7

# User query input
if user_input := st.chat_input("Ask a question based on recent news"):
    # Show user input
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call the Django backend
    try:
        response = requests.post(
            "http://localhost:8000/articles/query/",
            json={"date_range": date_range_days, "query": user_input},
            timeout=30
        )
        if response.status_code == 200:
            answer = response.json().get("answer", "No response.")
        else:
            answer = f"❌ Error from API: {response.json().get('error', 'Unknown error')}"

    except Exception as e:
        answer = f"❌ Failed to connect to backend: {e}"

    # Show assistant response
    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
