# 🚀 Endava Training Projects – Data Engineer/Software Developer 🧠

👋 Welcome to my **training portfolio** as a **Data Engineer/Developer** at **Endava**!  
This repository contains all the bite-sized, hands-on projects I've built during my **3-month training journey** 🛠️

## 📁 One Repo to Rule Them All 🗃️

Because each project is small but powerful 💥, I've kept everything neatly organized in a **single repository**.  
---

## 📅 Timeline Highlights
 
### Month1 - 🧱 Generic RDBMS & PLSQL & ETL
- ✅ Worked with SQL (Microsoft SQL Server & Oracle)gi
- ✅ Created a logging framework
- ✅ Created a Timesheet database where each employee's time worked can be tracked
- ✅ Took some Prompt Engineering trainings


### Month2 - 🐍 Python & Data Science & AI Fundamentals & Pydantic
- ✅ Worked on an ETL project where integrated 3 sources of data (Confluence leaves, Timesheets, Meeting Attendances) using Python scripts and Pandas 🐼
- ✅ Python from Basic Algorithms -> Advanced topics such as concurrency, async functions, event loops, Global Interpretor Lock (GIL), Garbage Collector,
- ✅ Python Authentication using HTTPBasicAuth / HTTPDigestAuth / Bearer Auth using JWT tokens
- ✅ Python pydantic Basemodels
- ✅ Flask + React app that exposes 3 APIs for computing(power to the 2, n-th Fibonacci, factorial). For persistance used SQLModel (pydantic) that could easily validate and store in SQL lite.


### Month 3 LLM Integration & OpenAI API & DevOps
- ✅ Agent🕵 for currency convertor that could answer prompts like this: "How many Euros were 2400 RONS in 2022-11-28?". Used OpenAI function calling, pydantic and integrated
    ExchangeRata.host API for historical conversion rates
- ✅ # RAG workflow for book recommendations based on user preferences (mostly topic).

## Hosting the Qdrant Client locally: Docker
## Vector store + Semantic Search: Qdrant
## LLM Tool calling + generation + Embeddings: OpenAI
## Frontend: React + Typescript
## Backend: Python + Flask
## Toxic Language Detection: Guardrails
Workflow: User asks the chatbot to recommend books based on a topic or genre. The chatbot uses the RAG workflow to retrieve relevant book information from Qdrant vector store and generates a response using gpt-5
- 🐳 Docker for containerization a Flask + React app that also uses a SqlLite. Managed Dockerfiles, used gunicorn for runing flask app, nginx for runing the react app
- 🐳 Docker Compose for orchestrating multi-container setup.
- 🐳 Deploy Qdrant on Kubernetes with a NodePort service for hosting the DB locally