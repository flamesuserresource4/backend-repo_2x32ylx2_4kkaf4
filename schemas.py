"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Laptop-specific schema for the e-commerce app
class Laptop(BaseModel):
    """
    Laptops collection schema
    Collection name: "laptop"
    """
    name: str = Field(..., description="Laptop model name")
    brand: str = Field(..., description="Brand such as HP, Dell, Lenovo, Apple, Asus, Acer, etc.")
    price: float = Field(..., ge=0, description="Price in USD")
    cpu: Optional[str] = Field(None, description="Processor model")
    ram_gb: Optional[int] = Field(None, ge=1, description="RAM size in GB")
    storage: Optional[str] = Field(None, description="Storage description e.g., 512GB SSD")
    gpu: Optional[str] = Field(None, description="Graphics card")
    screen: Optional[str] = Field(None, description="Screen size/resolution e.g., 15.6\" FHD")
    os: Optional[str] = Field(None, description="Operating system")
    rating: Optional[float] = Field(4.5, ge=0, le=5, description="Average rating 0-5")
    stock: int = Field(10, ge=0, description="Units in stock")
    image_url: Optional[str] = Field(None, description="Product image URL")
    highlights: Optional[List[str]] = Field(default=None, description="Key selling points")

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
