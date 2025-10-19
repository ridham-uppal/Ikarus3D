# **AI-Powered Furniture Recommendation Web App**

This project is a full-stack web application that uses a multi-modal AI model to provide furniture recommendations based on natural language queries. It combines machine learning, NLP, and computer vision with a modern web stack to deliver an interactive user experience. The application also features a data analytics dashboard to visualize insights from the product catalog.

## **Project Overview**

The core of this application is a recommendation engine that understands both the text descriptions and the images of furniture items. When a user enters a query like "a modern wooden desk for a small office," the system finds the most relevant products by comparing the query's meaning to the combined text and image data of each item in the database.

The project is composed of four main parts:

1. **React Frontend:** A clean, responsive user interface with two main pages for product recommendations and data analytics.  
2. **FastAPI Backend:** A high-performance API server that handles user requests, communicates with the machine learning models, and serves data to the frontend.  
3. **ML/AI Pipeline:** A set of Python notebooks for data analysis, model training, and embedding generation using Hugging Face Transformers (CLIP & TinyLlama).  
4. **Vector Database (Pinecone):** A specialized database used to store and efficiently search through high-dimensional vector embeddings of the furniture products.

## **Tech Stack**

| Category | Technology / Library |
| :---- | :---- |
| **Frontend** | React, Tailwind CSS, Recharts, Lucide Icons |
| **Backend** | FastAPI, Python 3.12+, Uvicorn |
| **ML/AI** | PyTorch, Transformers (Hugging Face), LangChain, Sentence-Transformers, Pinecone |
| **Notebooks** | Jupyter Notebook, Pandas, Matplotlib, Seaborn |
| **Database** | Pinecone (Vector Database) |

## **Project Structure**

ikarus-project/  
│  
├── backend/  
│   ├── app/  
│   │   ├── \_\_init\_\_.py  
│   │   ├── api.py              \# API endpoint definitions  
│   │   ├── config.py           \# Configuration and path management  
│   │   ├── main.py             \# FastAPI app entry point  
│   │   ├── schemas.py          \# Pydantic data models  
│   │   └── services.py         \# Core ML/AI and data logic  
│   ├── requirements.txt      \# Backend Python dependencies  
│   └── .env.example          \# Example environment variables  
│  
├── data/  
│   └── intern\_data\_ikarus.csv  \# The raw dataset  
│  
├── frontend/  
│   ├── public/  
│   └── src/  
│       ├── components/         \# Reusable React components  
│       ├── pages/              \# Page-level components (Analytics, Recommendations)  
│       ├── App.jsx             \# Main React app component  
│       └── index.js  
│  
├── notebooks/  
│   ├── analytics.ipynb         \# Exploratory Data Analysis (EDA)  
│   └── model\_training.ipynb    \# Model training and Pinecone population  
│  
└── README.md                   \# This file

## **Setup and Installation**

Follow these steps to set up and run the project locally.

### **Prerequisites**

* Python 3.10+  
* Node.js v18+ and npm  
* A Pinecone account (the free tier is sufficient)

### **1\. Clone the Repository**

git clone \<your-repository-url\>  
cd ikarus-project

### **2\. Set Up the Backend**

1. **Create a Virtual Environment:**  
   python \-m venv venv  
   source venv/bin/activate  \# On Windows: venv\\Scripts\\activate

2. **Install Dependencies:**  
   pip install \-r backend/requirements.txt

3. **Set Up Environment Variables:**  
   * Create a .env file inside the backend/ directory.  
   * Add your Pinecone API key to this file:  
     PINECONE\_API\_KEY="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

### **3\. Set Up the Frontend**

1. **Navigate to the Frontend Directory:**  
   cd frontend

2. **Install Dependencies:**  
   npm install

## **Running the Application**

The application requires three main steps to run: populating the database, starting the backend, and starting the frontend.

### **Step 1: Run the ML Notebook**

You must first run the model\_training.ipynb notebook to process the dataset and populate your Pinecone vector database.

1. Open the notebooks/ directory.  
2. Run all cells in model\_training.ipynb. This will:  
   * Load the dataset from data/.  
   * Download the required AI models.  
   * Generate embeddings for all products.  
   * Connect to your Pinecone account and upload the embeddings.  
   * **Note:** This process can take a significant amount of time, depending on your hardware.

### **Step 2: Start the Backend Server**

1. Navigate to the backend/ directory.  
2. Make sure your Python virtual environment is activated.  
3. Start the FastAPI server using Uvicorn:  
   uvicorn app.main:app \--reload

   The backend API will now be running at http://1227.0.0.1:8000.

### **Step 3: Start the Frontend Application**

1. Open a **new terminal** and navigate to the frontend/ directory.  
2. Start the React development server:  
   npm start

   The application will automatically open in your browser at http://localhost:3000.

You can now interact with the web app, search for products, and view the analytics dashboard\!
