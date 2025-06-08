"""Browser interaction tool."""

import asyncio
import os
import subprocess
import webbrowser
from concurrent.futures import ThreadPoolExecutor

from pydantic import BaseModel, Field
from utils.ai_models import get_llm
from utils.common import logger


class WebUrl(BaseModel):
    """Web URL response."""

    url: str = Field(
        ...,
        description="The URL to open in the browser",
    )


open_browser_def = {
    "name": "open_browser",
    "description": "Opens a browser tab with the best-fitting URL based on the user's prompt.",
    "parameters": {
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "description": "The user's prompt to determine which URL to open.",
            },
        },
        "required": ["prompt"],
    },
}


def open_chrome(url: str) -> bool:
    """Try to open Chrome using different methods."""
    # Common Chrome installation paths on Windows
    chrome_paths = [
        os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
    ]
    
    # Try each Chrome path
    for chrome_path in chrome_paths:
        if os.path.exists(chrome_path):
            try:
                subprocess.Popen([chrome_path, url])
                return True
            except Exception as e:
                logger.warning(f"Failed to open Chrome at {chrome_path}: {str(e)}")
    
    return False


async def open_browser_handler(prompt: str):
    """Open a browser tab with the best-fitting URL based on the user's prompt."""
    try:
        logger.info(f"📖 open_browser() Prompt: {prompt}")

        browser_urls = [
            "https://www.chatgpt.com",
            "https://www.tesla.com",
            "https://www.spacex.com",
            "https://www.goodreads.com",
        ]
        browser_urls_str = "\n".join(browser_urls)

        prompt_structure = f"""
        Select a browser URL from the list of browser URLs based on the user's prompt.

        # Steps:
        1. Infer the browser URL that the user wants to open from the user-prompt and the list of browser URLs.
        2. If the user-prompt is not related to the browser URLs, return an empty string.

        # Browser URLs:
        {browser_urls_str}

        # Prompt:
        {prompt}
        """

        llm = get_llm()
        structured_llm = llm.with_structured_output(WebUrl)
        response = structured_llm.invoke(prompt_structure)

        logger.info(f"📖 open_browser() Response: {response}")

        # Open the URL if it's not empty
        if response.url:
            logger.info(f"📖 open_browser() Opening URL: {response.url}")
            loop = asyncio.get_running_loop()
            with ThreadPoolExecutor() as pool:
                # Try to open with Chrome first using our custom function
                try:
                    chrome_opened = await loop.run_in_executor(pool, open_chrome, response.url)
                    if not chrome_opened:
                        # If Chrome opening failed, try default browser
                        await loop.run_in_executor(pool, webbrowser.open, response.url)
                except Exception as e:
                    logger.warning(f"Failed to open with Chrome: {str(e)}")
                    # Last resort: try generic browser
                    await loop.run_in_executor(pool, webbrowser.get().open, response.url)
            return f"URL opened successfully in the browser: {response.url}"
        else:
            error_message = f"Error retrieving URL from the prompt: {prompt}"
            logger.error(f"❌ {error_message}")
            return error_message

    except Exception as e:
        error_message = f"Error opening browser: {str(e)}"
        logger.error(f"❌ {error_message}")
        return {"status": "Error", "message": error_message}


open_browser = (open_browser_def, open_browser_handler)
