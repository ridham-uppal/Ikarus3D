# # ---
# # File: backend/app/services.py
# # ---
# # Description: This file contains the core business logic.
# # It handles loading models, processing data, and interacting with Pinecone.
# # ---

# import os
# import pandas as pd
# import torch
# from transformers import CLIPProcessor, CLIPModel
# from pinecone import Pinecone
# from langchain_huggingface import HuggingFacePipeline
# from langchain_core.prompts import PromptTemplate
# from . import config

# # --- Global Variables & Model Loading ---
# # This section should execute only once when the application starts.

# # Initialize Pinecone
# try:
#     pc = Pinecone(api_key=config.PINECONE_API_KEY)
#     index_name = "furniture-recommendations"
#     index = pc.Index(index_name)
#     print("Pinecone index loaded successfully.")
# except Exception as e:
#     index = None
#     print(f"Error initializing Pinecone: {e}")

# # Load the dataset for lookups
# try:
#     df = pd.read_csv(config.DATA_FILE_PATH)
#     df.dropna(subset=['uniq_id'], inplace=True)
#     df.drop_duplicates(subset=['uniq_id'], keep='first', inplace=True)
#     df_lookup = df.set_index('uniq_id').to_dict('index')
#     print(f"Data file loaded. Total unique products: {len(df_lookup)}")
# except FileNotFoundError:
#     df = pd.DataFrame() # Ensure df is an empty DataFrame if file not found
#     df_lookup = {}
#     print(f"Error: Data file not found at {config.DATA_FILE_PATH}")
# except ValueError as e:
#     df = pd.DataFrame()
#     df_lookup = {}
#     print(f"Error creating data lookup: {e}")


# # Set device for PyTorch
# device = "cuda" if torch.cuda.is_available() else "cpu"
# print(f"Device set to use {device}")

# # Load CLIP model for embeddings
# try:
#     clip_model_name = "openai/clip-vit-base-patch32"
#     clip_processor = CLIPProcessor.from_pretrained(clip_model_name)
#     clip_model = CLIPModel.from_pretrained(clip_model_name, use_safetensors=True).to(device)
#     print("CLIP model loaded successfully.")
# except Exception as e:
#     clip_model = None
#     clip_processor = None
#     print(f"Error loading CLIP model: {e}")

# # Load LLM for text generation
# try:
#     llm_model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
#     llm = HuggingFacePipeline.from_model_id(
#         model_id=llm_model_name,
#         task="text-generation",
#         device=0 if device == "cuda" else -1,
#         model_kwargs={"torch_dtype": torch.bfloat16, "use_safetensors": True},
#         pipeline_kwargs={"max_new_tokens": 100}
#     )
#     print("Language model loaded successfully.")
# except Exception as e:
#     llm = None
#     print(f"Error loading LLM: {e}")


# # --- Service Functions ---

# def get_analytics_data() -> dict:
#     """Processes the dataframe to extract key analytics."""
#     if df.empty:
#         return {"error": "Dataset not loaded."}
    
#     df_analytics = df.copy()
#     df_analytics['price'] = pd.to_numeric(df_analytics['price'].replace({'\$': ''}, regex=True), errors='coerce')
#     df_analytics.dropna(subset=['price'], inplace=True)

#     # Structure the output to match the AnalyticsData schema
#     return {
#         "total_products": int(df_analytics.shape[0]),
#         "price_statistics": {
#             "average": round(df_analytics['price'].mean(), 2)
#         },
#         "top_brands": df_analytics['brand'].value_counts().nlargest(10).to_dict(),
#         "top_materials": df_analytics['material'].value_counts().nlargest(10).to_dict(),
#         "top_countries": df_analytics['country_of_origin'].value_counts().nlargest(10).to_dict(),
#     }


# def find_similar_products(query_text: str, top_k: int = 5) -> list:
#     """Finds similar products using Pinecone."""
#     if not index or not clip_model or not clip_processor:
#         raise ConnectionError("A required service (Pinecone or CLIP) is not initialized.")
        
#     with torch.no_grad():
#         text_inputs = clip_processor(text=[query_text], return_tensors="pt", padding=True, truncation=True).to(device)
#         query_text_embedding = clip_model.get_text_features(**text_inputs)
        
#     query_image_embedding = torch.zeros(1, clip_model.config.projection_dim).to(device)
    
#     query_embedding = torch.cat((query_text_embedding, query_image_embedding), dim=1)
#     query_embedding = query_embedding / query_embedding.norm(dim=1, keepdim=True)
    
#     print(f"DEBUG: Query vector shape: {query_embedding.shape}")

#     results = index.query(
#         vector=query_embedding.cpu().tolist(),
#         top_k=top_k,
#         include_metadata=True
#     )
    
#     print(f"DEBUG: Raw Pinecone query results: {results}")

#     return results.get('matches', [])


# def get_product_details(product_id: str) -> dict | None:
#     """Retrieves product details from the lookup dictionary."""
#     return df_lookup.get(product_id)


# def generate_creative_description(product_details: dict) -> str:
#     """Generates a creative product description using the LLM."""
#     if not llm:
#         return "Creative description service is currently unavailable."

#     prompt_template = """
#     You are a creative copywriter for a high-end furniture store.
#     Write a short, engaging, and creative product description based on the following details.
    
#     Product Name: {title}
#     Brand: {brand}
#     Category: {category}
#     Material: {material}
#     Color: {color}
    
#     Creative Description:
#     """
    
#     prompt = PromptTemplate.from_template(prompt_template)
    
#     chain = prompt | llm
    
#     try:
#         category = eval(product_details.get('categories', "[]"))[0] if product_details.get('categories') else "Furniture"
#     except (SyntaxError, IndexError):
#         category = "Furniture"

#     creative_desc = chain.invoke({
#         "title": product_details.get('title', 'N/A'),
#         "brand": product_details.get('brand', 'N/A'),
#         "category": category,
#         "material": product_details.get('material', 'N/A'),
#         "color": product_details.get('color', 'N/A'),
#     })
    
#     # Clean up the output from the LLM
#     if "Creative Description:" in creative_desc:
#         creative_desc = creative_desc.split("Creative Description:")[1].strip()
    
#     # Additional cleanup if the model repeats the prompt
#     prompt_elements = [
#         product_details.get('title', ''),
#         product_details.get('brand', ''),
#         category
#     ]
#     for element in prompt_elements:
#         if element and element in creative_desc:
#             creative_desc = creative_desc.replace(element, "").strip()

#     return creative_desc

# ---
# File: backend/app/services.py
# ---
# Description: Contains the core business logic for ML models and data processing.
# This keeps the API endpoints clean and focused on request/response handling.
# ---
# ---
# File: backend/app/services.py
# ---
# Description: Contains the core business logic for ML models and data processing.
# This keeps the API endpoints clean and focused on request/response handling.
# ---


#preb----version

# import pandas as pd
# import torch
# from transformers import CLIPProcessor, CLIPModel
# from pinecone import Pinecone
# from langchain_huggingface import HuggingFacePipeline
# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# import numpy as np

# from . import config

# # --- Globals ---
# pinecone_index = None
# clip_model = None
# clip_processor = None
# llm = None
# df_lookup = {}

# # --- Initialization Functions ---
# def load_pinecone():
#     """Initializes and returns the Pinecone index."""
#     global pinecone_index
#     if pinecone_index is None:
#         pc = Pinecone(api_key=config.PINECONE_API_KEY)
#         pinecone_index = pc.Index(config.PINECONE_INDEX_NAME)
#         print("Pinecone index loaded successfully.")
#     return pinecone_index

# def load_data():
#     """Loads the product data from CSV and creates a lookup dictionary."""
#     global df_lookup
#     if not df_lookup:
#         df = pd.read_csv(config.DATA_FILE_PATH)
#         # Handle duplicate uniq_id values before creating the lookup
#         df.drop_duplicates(subset='uniq_id', keep='first', inplace=True)
#         df_lookup = df.set_index('uniq_id').to_dict('index')
#         print(f"Data file loaded. Total unique products: {len(df_lookup)}")

# def load_clip_model():
#     """Loads the CLIP model and processor."""
#     global clip_model, clip_processor
#     if clip_model is None:
#         device = "cuda" if torch.cuda.is_available() else "cpu"
#         print(f"Device set to use {device}")
#         model_name = "openai/clip-vit-base-patch32"
#         clip_processor = CLIPProcessor.from_pretrained(model_name)
#         clip_model = CLIPModel.from_pretrained(model_name, use_safetensors=True).to(device)
#         print("CLIP model loaded successfully.")

# def load_llm():
#     """Loads the language model for generating descriptions."""
#     global llm
#     if llm is None:
#         device = "cuda" if torch.cuda.is_available() else "cpu"
#         print(f"Device set to use {device}")
#         llm_model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
#         llm = HuggingFacePipeline.from_model_id(
#             model_id=llm_model_name,
#             task="text-generation",
#             device=0 if device == "cuda" else -1,
#             model_kwargs={"torch_dtype": torch.bfloat16, "use_safetensors": True},
#             pipeline_kwargs={"max_new_tokens": 100},
#         )
#         print("Language model loaded successfully.")


# # --- Service Functions ---
# def get_analytics_data():
#     """Calculates and returns analytics data."""
#     df = pd.read_csv(config.DATA_FILE_PATH)
#     df['price'] = pd.to_numeric(df['price'].replace({'\$': ''}, regex=True), errors='coerce')
#     df.dropna(subset=['price'], inplace=True)
    
#     avg_price = round(df['price'].mean(), 2)
#     price_stats = {"average": avg_price}
    
#     return {
#         "total_products": len(df),
#         "price_statistics": price_stats,
#         "top_brands": df['brand'].value_counts().nlargest(10).to_dict(),
#         "top_materials": df['material'].value_counts().nlargest(10).to_dict(),
#         "top_countries": df['country_of_origin'].value_counts().nlargest(5).to_dict()
#     }

# def find_similar_products(query_text: str, top_k=5):
#     """Finds similar products using CLIP and Pinecone."""
#     device = clip_model.device
    
#     # 1. Create text embedding for the query
#     inputs = clip_processor(text=[query_text], return_tensors="pt", padding=True).to(device)
#     with torch.no_grad():
#         text_features = clip_model.get_text_features(**inputs)
    
#     # 2. --- FIX: Create a placeholder image embedding with the correct projection dimension ---
#     # The final output dimension of both text and image features from CLIP is `projection_dim`.
#     # Using the wrong dimension (e.g., `vision_config.hidden_size`) causes a mismatch.
#     image_features = torch.zeros(1, clip_model.config.projection_dim).to(device)
#     # --- END FIX ---
    
#     # 3. Combine and normalize
#     query_embedding = torch.cat((text_features, image_features), dim=1)
#     query_embedding /= query_embedding.norm(dim=-1, keepdim=True)
    
#     # 4. Query Pinecone
#     results = pinecone_index.query(
#         vector=query_embedding.cpu().tolist(),
#         top_k=top_k,
#         include_metadata=False
#     )
#     return results['matches']

# def get_product_details(product_id: str):
#     """Retrieves product details from the lookup dictionary."""
#     return df_lookup.get(product_id)

# def generate_creative_description(product_details: dict):
#     """Generates a creative product description using the LLM."""
#     prompt_template = """
#     You are a creative copywriter. Write a short, engaging product description based on these details.
#     Do not repeat the title. Focus on the feeling and style.
    
#     Title: {title}
#     Brand: {brand}
#     Material: {material}
#     Color: {color}
    
#     Creative Description:
#     """
    
#     prompt = PromptTemplate.from_template(prompt_template)
#     chain = prompt | llm | StrOutputParser()
    
#     # Fill NaN with "not specified" for better LLM context
#     filled_details = {k: v if pd.notna(v) else "not specified" for k, v in product_details.items()}
    
#     return chain.invoke(filled_details)


# # --- Application Startup Logic ---
# load_pinecone()
# load_data()
# load_clip_model()
# load_llm()

# ---
# File: backend/app/services.py
# ---
# Description: Contains the core business logic for the application, including
# loading models, interacting with Pinecone, and generating content.
# ---
import os
import pandas as pd
import torch
from transformers import CLIPProcessor, CLIPModel
from langchain_huggingface import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from pinecone import Pinecone
from . import config

# --- Load Data ---
try:
    df = pd.read_csv(config.DATA_FILE_PATH)
    # FIX: Drop duplicates to prevent errors when creating the lookup dictionary
    df.drop_duplicates(subset='uniq_id', keep='first', inplace=True)
    df_lookup = df.set_index('uniq_id').to_dict('index')
    print("Data file loaded. Total unique products:", len(df_lookup))
except FileNotFoundError:
    print(f"Error: Data file not found at {config.DATA_FILE_PATH}")
    df_lookup = {}

# --- Initialize Pinecone ---
try:
    pc = Pinecone(api_key=config.PINECONE_API_KEY)
    index = pc.Index(config.PINECONE_INDEX_NAME)
    print("Pinecone index loaded successfully.")
except Exception as e:
    print(f"Error initializing Pinecone: {e}")
    index = None

# --- Load Models ---
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device set to use {device}")

# Load CLIP model for embeddings
try:
    clip_model_name = "openai/clip-vit-base-patch32"
    clip_processor = CLIPProcessor.from_pretrained(clip_model_name)
    clip_model = CLIPModel.from_pretrained(clip_model_name, use_safetensors=True).to(device)
    print("CLIP model loaded successfully.")
except Exception as e:
    print(f"Error loading CLIP model: {e}")
    clip_model = None

# Load Language Model for text generation
try:
    llm_model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    llm = HuggingFacePipeline.from_model_id(
        model_id=llm_model_name,
        task="text-generation",
        device=0 if device == "cuda" else -1,
        model_kwargs={"torch_dtype": torch.bfloat16, "use_safetensors": True},
        pipeline_kwargs={"max_new_tokens": 100},
    )
    print("Language model loaded successfully.")
except Exception as e:
    print(f"Error loading language model: {e}")
    llm = None

# --- Prompt Template ---
prompt_template_str = """
You are a creative copywriter for a high-end furniture store.
Write a short, engaging, and creative product description based on the following details.
Do not just repeat the details, but use them as inspiration.

Product Details:
- Title: {title}
- Brand: {brand}
- Color: {color}
- Material: {material}

Creative Description:
"""
prompt_template = PromptTemplate.from_template(prompt_template_str)


# --- Service Functions ---

def get_analytics_data() -> dict:
    """Calculates and returns analytics data from the dataframe."""
    total_products = len(df)
    
    # Ensure price is numeric before calculating mean
    df['price_numeric'] = pd.to_numeric(df['price'].str.replace('$', ''), errors='coerce')
    average_price = round(df['price_numeric'].mean(), 2)

    top_brands = df['brand'].value_counts().nlargest(10).to_dict()
    top_materials = df['material'].value_counts().nlargest(10).to_dict()
    top_countries = df['country_of_origin'].value_counts().nlargest(5).to_dict()

    return {
        "total_products": total_products,
        "price_statistics": {"average": average_price},
        "top_brands": top_brands,
        "top_materials": top_materials,
        "top_countries": top_countries,
    }

def find_similar_products(query_text: str, top_k: int = 5) -> list:
    """Finds similar products using CLIP and Pinecone."""
    if not clip_model or not index:
        return []
        
    with torch.no_grad():
        inputs = clip_processor(text=[query_text], return_tensors="pt", padding=True).to(device)
        text_embedding = clip_model.get_text_features(**inputs)
        
        # Create a zero vector for the image part to match the combined embedding dimension
        image_placeholder = torch.zeros(1, clip_model.config.vision_config.hidden_size).to(device)
        
        query_embedding = torch.cat([text_embedding, image_placeholder], dim=1)
        query_embedding /= query_embedding.norm(dim=-1, keepdim=True)

    results = index.query(
        vector=query_embedding.cpu().tolist(),
        top_k=top_k,
        include_metadata=False
    )
    return results.get('matches', [])


def generate_creative_description(product_details: dict) -> str:
    """
    Generates a creative product description using the language model.
    """
    if not llm:
        return "A finely crafted piece, perfect for any home."
        
    try:
        # FIX: Clean the input values first to handle potential NaN from pandas.
        # This prevents errors or empty responses from the language model.
        title = product_details.get("title", "")
        brand = product_details.get("brand", "")
        color = product_details.get("color", "")
        material = product_details.get("material", "")

        prompt_input = {
            "title": "" if pd.isna(title) else title,
            "brand": "" if pd.isna(brand) else brand,
            "color": "" if pd.isna(color) else color,
            "material": "" if pd.isna(material) else material,
        }
        
        chain = prompt_template | llm
        result = chain.invoke(prompt_input)
        
        if "Creative Description:" in result:
            result = result.split("Creative Description:")[1]
        
        if not result.strip():
            return "A versatile and stylish piece, designed to complement any modern living space."

        return result.strip()
    except Exception as e:
        print(f"Error generating description: {e}")
        return "A finely crafted piece, perfect for any home."


def get_product_details(product_id: str) -> dict:
    """Retrieves the full details for a product by its unique ID."""
    return df_lookup.get(product_id)

