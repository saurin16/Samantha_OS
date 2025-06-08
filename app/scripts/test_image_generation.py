"""Test script for Hugging Face image generation."""

import os
import base64
from PIL import Image
import io
import sys
from pathlib import Path

# Add both app and utils directories to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.extend([
    str(project_root),  # For app imports
    str(project_root / "app"),  # For app submodules
    str(project_root / "utils"),  # For utils imports
])

# Import after setting up the path
from app.tools.image import generate_image
from utils.common import logger

def test_image_generation():
    """Test the image generation functionality."""
    try:
        # Check if API token is set
        if not os.getenv("HUGGINGFACE_API_TOKEN"):
            logger.error("❌ HUGGINGFACE_API_TOKEN environment variable not set")
            return

        # Test prompt
        prompt = "A serene landscape with mountains and a lake at sunset, photorealistic style"
        
        logger.info(f"🎨 Testing image generation with prompt: {prompt}")
        
        # Generate image
        result = generate_image(prompt)
        
        if result["status"] == "success":
            # Save the image
            image_data = base64.b64decode(result["data"]["image"])
            image = Image.open(io.BytesIO(image_data))
            
            # Create output directory if it doesn't exist
            os.makedirs("output", exist_ok=True)
            
            # Save the image
            output_path = "output/generated_image.png"
            image.save(output_path)
            
            logger.info(f"✅ Image generated successfully and saved to {output_path}")
            logger.info(f"📝 Used model: {result['data']['model']}")
        else:
            logger.error(f"❌ Image generation failed: {result['message']}")

    except Exception as e:
        logger.error(f"❌ Test failed: {str(e)}")

if __name__ == "__main__":
    test_image_generation() 