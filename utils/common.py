"""Common utilities for the application."""

import logging
import os
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Create logger instance
logger = logging.getLogger(__name__)

# Define common paths
project_root = Path(__file__).parent.parent
scratch_pad_dir = project_root / "scratchpad"
output_dir = project_root / "output"

# Create necessary directories
scratch_pad_dir.mkdir(exist_ok=True)
output_dir.mkdir(exist_ok=True) 