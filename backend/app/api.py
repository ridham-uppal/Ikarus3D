# # ---
# # File: backend/app/api.py
# # ---
# # Description: Defines the API routes for the application using FastAPI's APIRouter.
# # This keeps the main application file clean.
# # ---

# from fastapi import APIRouter, HTTPException
# import pandas as pd
# from . import services, schemas

# api_router = APIRouter(prefix="/api/v1")

# @api_router.get("/analytics", response_model=schemas.AnalyticsData)
# async def get_analytics():
#     """
#     Endpoint to get analytics data about the product catalog.
#     """
#     data = services.get_analytics_data()
#     if "error" in data:
#          raise HTTPException(status_code=500, detail=data["error"])
#     return data

# @api_router.post("/recommend", response_model=list[schemas.Recommendation])
# async def get_recommendations(query: schemas.Query):
#     """
#     Endpoint to get product recommendations.

#     Receives a text query, finds similar products using the ML model,
#     generates a creative description for each, and returns the results.
#     """
#     try:
#         matches = services.find_similar_products(query.text)
#         print(f"DEBUG: Matches received from service: {matches}")

#         recommendations = []
#         for match in matches:
#             product_id = match['id']
#             print(f"DEBUG: Processing product ID: {product_id}")

#             product_details = services.get_product_details(product_id)

#             if not product_details:
#                 print(f"DEBUG: No details found for ID: {product_id}. Skipping.")
#                 continue

#             creative_desc = services.generate_creative_description(product_details)

#             # Clean data to prevent Pydantic validation errors
#             cleaned_details = {
#                 "uniq_id": product_id,
#                 "title": product_details.get('title') or "No Title",
#                 "description": "" if pd.isna(product_details.get('description')) else str(product_details.get('description')),
#                 "brand": "" if pd.isna(product_details.get('brand')) else str(product_details.get('brand')),
#                 "price": "" if pd.isna(product_details.get('price')) else str(product_details.get('price')),
#                 "images": "[]" if pd.isna(product_details.get('images')) else str(product_details.get('images')),
#                 "material": "" if pd.isna(product_details.get('material')) else str(product_details.get('material')),
#                 "color": "" if pd.isna(product_details.get('color')) else str(product_details.get('color')),
#             }
            
#             # Construct the final response object according to the schema
#             recommendation = schemas.Recommendation(
#                 uniq_id=product_id,
#                 score=match['score'],
#                 details=cleaned_details,
#                 creative_description=creative_desc
#             )
#             recommendations.append(recommendation)
        
#         return recommendations

#     except Exception as e:
#         print(f"Error in /recommend endpoint: {e}")
#         raise HTTPException(status_code=500, detail="An internal error occurred while generating recommendations.")


# ---
# File: backend/app/api.py
# ---
# Description: Defines the API routes for the application using FastAPI's APIRouter.
# This keeps the main application file clean.
# ---

# from fastapi import APIRouter, HTTPException
# import pandas as pd
# from . import services, schemas

# api_router = APIRouter(prefix="/api/v1")

# # --- In-memory cache for analytics data ---
# # This variable will store the analytics data after it's calculated once.
# _analytics_cache = None

# @api_router.get("/analytics", response_model=schemas.AnalyticsData)
# async def get_analytics():
#     """
#     Endpoint to get analytics data about the product catalog.
#     The data is cached in memory after the first request to improve performance.
#     """
#     global _analytics_cache
    
#     # If the cache is empty, calculate the data and store it.
#     if _analytics_cache is None:
#         print("DEBUG: Analytics data not in cache. Calculating and caching now.")
#         _analytics_cache = services.get_analytics_data()
#     else:
#         print("DEBUG: Returning cached analytics data.")
        
#     return _analytics_cache

# @api_router.post("/recommend", response_model=list[schemas.Recommendation])
# async def get_recommendations(query: schemas.Query):
#     """
#     Endpoint to get product recommendations without creative descriptions.
#     This provides a fast initial response to the user.
#     """
#     try:
#         matches = services.find_similar_products(query.text)
#         recommendations = []
#         for match in matches:
#             product_id = match['id']
#             product_details = services.get_product_details(product_id)

#             if not product_details:
#                 continue
            
#             # Add uniq_id to the details dictionary before cleaning
#             product_details['uniq_id'] = product_id

#             cleaned_details = {
#                 key: "" if pd.isna(value) else value
#                 for key, value in product_details.items()
#             }
            
#             recommendation = schemas.Recommendation(
#                 uniq_id=product_id,
#                 score=match['score'],
#                 details=cleaned_details
#             )
#             recommendations.append(recommendation)
        
#         return recommendations

#     except Exception as e:
#         print(f"Error in /recommend endpoint: {e}")
#         raise HTTPException(status_code=500, detail="An error occurred while finding recommendations.")

# @api_router.post("/generate-description", response_model=schemas.CreativeDescription)
# async def generate_description_endpoint(details: schemas.ProductDetails):
#     """
#     Endpoint to generate a creative description for a single product.
#     """
#     try:
#         # Pydantic models can be converted to dicts for the service function
#         details_dict = details.dict()
#         creative_desc = services.generate_creative_description(details_dict)
#         return schemas.CreativeDescription(creative_description=creative_desc)
#     except Exception as e:
#         print(f"Error in /generate-description endpoint: {e}")
#         raise HTTPException(status_code=500, detail="Failed to generate creative description.")


#only 2 apis
# ---
# File: backend/app/api.py
# ---
# Description: Defines the API routes for the application using FastAPI's APIRouter.
# This keeps the main application file clean.
# ---

from fastapi import APIRouter, HTTPException
import pandas as pd
from . import services, schemas

api_router = APIRouter(prefix="/api/v1")

# --- In-memory cache for analytics data ---
_analytics_cache = None

@api_router.get("/analytics", response_model=schemas.AnalyticsData)
async def get_analytics():
    """
    Endpoint to get analytics data about the product catalog.
    The data is cached in memory after the first request to improve performance.
    """
    global _analytics_cache
    
    if _analytics_cache is None:
        print("DEBUG: Analytics data not in cache. Calculating and caching now.")
        _analytics_cache = services.get_analytics_data()
    else:
        print("DEBUG: Returning cached analytics data.")
        
    return _analytics_cache

@api_router.post("/recommend", response_model=list[schemas.Recommendation])
async def get_recommendations(query: schemas.Query):
    """
    Endpoint to get product recommendations.

    This single endpoint now handles finding similar products AND generating
    their creative descriptions before sending the complete response.
    """
    try:
        matches = services.find_similar_products(query.text)
        recommendations = []
        for match in matches:
            product_id = match['id']
            product_details = services.get_product_details(product_id)

            if not product_details:
                continue
            
            product_details['uniq_id'] = product_id

            # Generate the creative description here in the backend
            creative_desc = services.generate_creative_description(product_details)

            cleaned_details = {
                key: "" if pd.isna(value) else value
                for key, value in product_details.items()
            }
            
            recommendation = schemas.Recommendation(
                uniq_id=product_id,
                score=match['score'],
                details=cleaned_details,
                creative_description=creative_desc # Add it to the response model
            )
            recommendations.append(recommendation)
        
        return recommendations

    except Exception as e:
        print(f"Error in /recommend endpoint: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while finding recommendations.")

