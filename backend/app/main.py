# # # ---
# # # File: backend/app/main.py
# # # ---
# # # Description: This is the main entry point for the FastAPI application.
# # # It sets up the FastAPI app instance, includes the API routers, and configures CORS.
# # # ---

# # from fastapi import FastAPI
# # from fastapi.middleware.cors import CORSMiddleware
# # from .api import api_router

# # # Create the FastAPI app instance
# # app = FastAPI(
# #     title="Product Recommendation API",
# #     description="API for furniture product recommendations, creative descriptions, and analytics.",
# #     version="1.0.0"
# # )

# # # --- Configure CORS (Cross-Origin Resource Sharing) ---
# # # This is crucial to allow your React frontend (running on a different domain/port)
# # # to communicate with this backend.
# # origins = [
# #     "http://localhost:3000",  # Default React development server
# #     "http://localhost:5173",  # Default Vite React development server
# #     # Add any other origins you might use for development or deployment
# # ]

# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=origins,
# #     allow_credentials=True,
# #     allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
# #     allow_headers=["*"],  # Allows all headers
# # )

# # # --- Include API Routers ---
# # # This line includes all the endpoint definitions from the api.py file.
# # app.include_router(api_router, prefix="/api/v1")

# # # --- Root Endpoint ---
# # # A simple endpoint to confirm that the API is running.
# # @app.get("/", tags=["Root"])
# # async def read_root():
# #     """
# #     Root endpoint to check API status.
# #     """
# #     return {"message": "Welcome to the Product Recommendation API!"}

# # ---
# # File: backend/app/main.py
# # ---
# # Description: The main entry point for the FastAPI application.
# # It initializes the FastAPI app, sets up CORS, and includes the API router.
# # ---

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.openapi.docs import get_swagger_ui_html
# from starlette.responses import HTMLResponse

# from .api import api_router

# # Initialize the FastAPI application
# app = FastAPI(
#     title="Product Recommendation API",
#     description="API for furniture product recommendations and analytics.",
#     version="1.0.0",
#     # Disable the default docs to use a custom one
#     docs_url=None, 
#     redoc_url=None
# )

# # Set up CORS (Cross-Origin Resource Sharing)
# # This allows the frontend (running on a different port) to communicate with the backend.
# origins = [
#     "http://localhost:5173",
#     "http://localhost:3000", # Default port for React apps
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # --- FIX: Custom Swagger UI Endpoint ---
# # This custom endpoint serves the Swagger UI documentation using assets from a more
# # reliable CDN (unpkg), which can resolve issues where the default docs page gets
# # stuck in a loading state due to network or CDN problems.
# @app.get("/docs", include_in_schema=False)
# async def custom_swagger_ui_html() -> HTMLResponse:
#     """
#     Serve the Swagger UI documentation from an alternative CDN.
#     """
#     return get_swagger_ui_html(
#         openapi_url=app.openapi_url,
#         title=app.title + " - Swagger UI",
#         swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
#         swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
#     )
# # --- END FIX ---


# # Include the API router
# # This adds all the endpoints defined in `api.py` to the application.
# app.include_router(api_router)

# @app.get("/", summary="Root endpoint to check API status")
# def read_root():
#     """A simple endpoint to confirm that the API is running."""
#     return {"status": "API is running"}


# ---
# File: backend/app/main.py
# ---
# Description: The main entry point for the FastAPI application.
# It initializes the FastAPI app, sets up CORS, and includes the API router.
# ---

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.responses import HTMLResponse

from .api import api_router

# Initialize the FastAPI application
app = FastAPI(
    title="Product Recommendation API",
    description="API for furniture product recommendations and analytics.",
    version="1.0.0",
    # Disable the default docs to use a custom one
    docs_url=None, 
    redoc_url=None
)

# Set up CORS (Cross-Origin Resource Sharing)
# This allows the frontend (running on a different port) to communicate with the backend.
origins = [
    "http://localhost:5173",
    "http://localhost:8080", # Default port for React apps
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- FIX: Custom Swagger UI Endpoint ---
# This custom endpoint serves the Swagger UI documentation using assets from a more
# reliable CDN (unpkg), which can resolve issues where the default docs page gets
# stuck in a loading state due to network or CDN problems.
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html() -> HTMLResponse:
    """
    Serve the Swagger UI documentation from an alternative CDN.
    """
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )
# --- END FIX ---


# Include the API router
# This adds all the endpoints defined in `api.py` to the application.
app.include_router(api_router)

@app.get("/", summary="Root endpoint to check API status")
def read_root():
    """A simple endpoint to confirm that the API is running."""
    return {"status": "API is running"}

