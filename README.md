# 📰 MyNews – Personalized News Answering System

MyNews is an end-to-end data engineering and NLP project that ingests recent news articles, summarizes them, stores embeddings for semantic search, and enables users to ask natural language questions via a chatbot interface. Built with Apache Kafka, Spark, Airflow, Django, pgvector, and Streamlit.

---

## 🚀 Features

- ✅ **Automated News Ingestion** every 15 minutes using Airflow and Kafka
- ⚡ **Real-time Summarization & Embedding Generation** with Spark
- 🔍 **Semantic Search** powered by pgvector in PostgreSQL
- 📡 **Django REST API** to handle user queries and return context-aware answers
- 💬 **Streamlit Frontend** for an interactive chat interface

---

## 🏗️ Architecture

```
News API → Kafka → Spark → Postgres (pgvector)
                            ↳ Airflow (scheduling)
                            ↳ Django API → Streamlit UI
```

---

## 🧱 Tech Stack

| Layer      | Tools Used                                |
| ---------- | ----------------------------------------- |
| Ingestion  | Apache Kafka, Airflow                     |
| Processing | Apache Spark (Python API)                 |
| Storage    | PostgreSQL with pgvector extension        |
| Backend    | Django, Django REST Framework             |
| Embeddings | Sentence Transformers / Vertex AI / Gemini |
| Frontend   | Streamlit                                 |
| Deployment | Docker Compose                 |

---

## 🧺 How It Works

1. **Fetch Articles:** Airflow triggers a DAG every 15 minutes to call the News API.
2. **Stream with Kafka:** Articles are streamed to Kafka topics.
3. **Summarize + Embed:** Spark consumes from Kafka, creates summaries & vector embeddings.
4. **Store Data:** Summaries and embeddings are stored in PostgreSQL (with pgvector).
5. **Querying:** Users input queries via Streamlit → Django API → vector similarity search → summarized answers returned.

---

## 💾 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/mynews-pipeline.git
cd mynews-pipeline
```

### 2. Start the Entire System with Docker Compose

```bash
docker-compose up --build
```

> This will launch:
>
> - PostgreSQL with pgvector
> - Kafka + Zookeeper
> - Airflow (scheduler + webserver)
> - Spark job processor
> - Django backend (API for querying articles)
> - Streamlit frontend (chat interface)

---

## 📂 Project Structure

```
mynews/
├── data_pipeline/
│   ├── dags/               # Airflow DAGs
│   ├── kafka/              # Kafka producer/consumer
│   ├── spark_app/          # Spark summarization/embedding
│   └── requirements.txt
├── django_backend/
│   ├── articles/           # Django app for news query API
│   └── mynews_backend/     # Django project settings
├── streamlit_app/
│   └── app.py              # Streamlit chatbot frontend
├── docker-compose.yml
└── README.md
```

---

## 🧠 Example Use Case

> “What happened in international politics in the past 7 days?”

✅ MyNews will:

- Search the last 7 days of articles
- Retrieve top relevant summaries via cosine similarity
- Return a concise answer via the chatbot interface

---

## 📍 License

This project is open-source and available under the [MIT License](LICENSE).

