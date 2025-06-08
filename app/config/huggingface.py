"""Hugging Face API configuration."""

import os
from typing import Optional
from pydantic import BaseModel, Field

class HuggingFaceConfig(BaseModel):
    """Hugging Face API configuration."""
    
    api_token: str = Field(
        default=os.getenv("HUGGINGFACE_API_TOKEN", ""),
        description="Hugging Face API token"
    )
    
    api_base: str = Field(
        default="https://api-inference.huggingface.co",
        description="Hugging Face API base URL"
    )
    
    default_model: str = Field(
        default="stabilityai/stable-diffusion-xl-base-1.0",
        description="Default model to use for inference"
    )
    
    max_retries: int = Field(
        default=3,
        description="Maximum number of retries for API calls"
    )
    
    timeout: int = Field(
        default=30,
        description="Timeout in seconds for API calls"
    )

# Initialize configuration
hf_config = HuggingFaceConfig()

# Available models
AVAILABLE_MODELS = {
    "text-to-image": [
        "stabilityai/stable-diffusion-xl-base-1.0",
        "runwayml/stable-diffusion-v1-5",
        "CompVis/stable-diffusion-v1-4"
    ],
    "text-generation": [
        "meta-llama/Llama-2-7b-chat-hf",
        "tiiuae/falcon-7b-instruct",
        "google/flan-t5-xxl"
    ],
    "text-classification": [
        "distilbert-base-uncased-finetuned-sst-2-english",
        "facebook/bart-large-mnli"
    ]
} 