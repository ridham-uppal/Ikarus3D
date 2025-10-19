# # ---
# # File: backend/app/schemas.py
# # ---
# # Description: This file contains the Pydantic models (schemas) used for
# # data validation and serialization in the API.
# # ---

# from pydantic import BaseModel
# from typing import Optional, Dict

# # --- Analytics Schemas ---

# class PriceStatistics(BaseModel):
#     """Nested model for price-related analytics."""
#     average: float

# class AnalyticsData(BaseModel):
#     """Schema for the main analytics endpoint response."""
#     total_products: int
#     price_statistics: PriceStatistics
#     top_brands: Dict[str, int]
#     top_materials: Dict[str, int]
#     top_countries: Dict[str, int]

# # --- Recommendation Schemas ---

# class Query(BaseModel):
#     """Schema for the incoming recommendation query."""
#     text: str

# class ProductDetails(BaseModel):
#     """Schema for the detailed product information."""
#     uniq_id: str
#     title: str
#     description: str
#     brand: Optional[str] = None
#     price: Optional[str] = None
#     images: Optional[str] = None
#     material: Optional[str] = None
#     color: Optional[str] = None

# class Recommendation(BaseModel):
#     """Schema for a single recommendation item in the response."""
#     uniq_id: str
#     score: float
#     details: ProductDetails
#     creative_description: str

# ---
# File: backend/app/schemas.py
# ---
# Description: Defines the Pydantic models for data validation and serialization.
# These models act as the data contracts for the API.
# ---

from pydantic import BaseModel
from typing import Dict, Any

# --- Analytics Schemas ---
class PriceStatistics(BaseModel):
    average: float

class AnalyticsData(BaseModel):
    total_products: int
    price_statistics: PriceStatistics
    top_brands: Dict[str, int]
    top_materials: Dict[str, int]
    top_countries: Dict[str, int]

# --- Recommendation Schemas ---
class Query(BaseModel):
    text: str

class ProductDetails(BaseModel):
    uniq_id: str
    title: str | None = None
    description: str | None = None
    brand: str | None = None
    price: Any | None = None
    images: str | None = None
    material: str | None = None
    color: str | None = None
    
class Recommendation(BaseModel):
    uniq_id: str
    score: float
    details: ProductDetails

class CreativeDescription(BaseModel):
    creative_description: str

