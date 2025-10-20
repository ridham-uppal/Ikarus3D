# **AI-Powered Furniture Recommendation Web App**

This project is a full-stack web application that uses a multi-modal AI model to provide furniture recommendations based on natural language queries. It combines machine learning, NLP, and computer vision with a modern web stack to deliver an interactive user experience. The application also features a data analytics dashboard to visualize insights from the product catalog.

---

## 🌐 **Live Demo**

The frontend of this project is deployed and available here:  
👉 [**ikarus-nu.vercel.app**](https://ikarus-nu.vercel.app/)

> **Note:** The backend, ML model pipeline, and vector database are **not hosted** due to time constraints and infrastructure limitations.  
> The backend requires a **paid deployment solution** because of large model dependencies and database size.  
> However, the **entire backend and ML pipeline can be run locally** by following the setup instructions below.

---

## **Project Overview**

The core of this application is a recommendation engine that understands both the text descriptions and the images of furniture items. When a user enters a query like "a modern wooden desk for a small office," the system finds the most relevant products by comparing the query's meaning to the combined text and image data of each item in the database.

The project is composed of four main parts:

1. **React Frontend:** A clean, responsive user interface with two main pages for product recommendations and data analytics.  
2. **FastAPI Backend:** A high-performance API server that handles user requests, communicates with the machine learning models, and serves data to the frontend.  
3. **ML/AI Pipeline:** A set of Python notebooks for data analysis, model training, and embedding generation using Hugging Face Transformers (CLIP & TinyLlama).  
4. **Vector Database (Pinecone):** A specialized database used to store and efficiently search through high-dimensional vector embeddings of the furniture products.

---

## **Tech Stack**

| Category | Technology / Library |
| :---- | :---- |
| **Frontend** | React, Tailwind CSS, Recharts, Lucide Icons |
| **Backend** | FastAPI, Python 3.12+, Uvicorn |
| **ML/AI** | PyTorch, Transformers (Hugging Face), LangChain, Sentence-Transformers, Pinecone |
| **Notebooks** | Jupyter Notebook, Pandas, Matplotlib, Seaborn |
| **Database** | Pinecone (Vector Database) |

---

## **Project Structure**

ikarus-project/  
│  
├── backend/  
│   ├── app/  
│   │   ├── __init__.py  
│   │   ├── api.py              # API endpoint definitions  
│   │   ├── config.py           # Configuration and path management  
│   │   ├── main.py             # FastAPI app entry point  
│   │   ├── schemas.py          # Pydantic data models  
│   │   └── services.py         # Core ML/AI and data logic  
│   ├── requirements.txt        # Backend Python dependencies  
│   └── .env.example            # Example environment variables  
│  
├── data/  
│   └── intern_data_ikarus.csv  # The raw dataset  
│  
├── frontend/  
│   ├── public/  
│   └── src/  
│       ├── components/         # Reusable React components  
│       ├── pages/              # Page-level components (Analytics, Recommendations)  
│       ├── App.jsx             # Main React app component  
│       └── index.js  
│  
├── notebooks/  
│   ├── analytics.ipynb         # Exploratory Data Analysis (EDA)  
│   └── model_training.ipynb    # Model training and Pinecone population  
│  
└── README.md                   # This file

---

## **Setup and Installation**

Follow these steps to set up and run the project locally.

### **Prerequisites**

* Python 3.10+  
* Node.js v18+ and npm  
* A Pinecone account (the free tier is sufficient)

---

### **1. Clone the Repository**

```bash
git clone <your-repository-url>
cd ikarus-project
