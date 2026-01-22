import os
import json
import subprocess
from openai import OpenAI
from typing import Optional

# Configuration for OpenRouter (compatible with OpenAI SDK)
# Assumes OPENROUTER_API_KEY is set in the environment
OPENROUTER_API_BASE = "https://openrouter.ai/api/v1"
# Based on search results, Qwen3-VL-32B-Instruct is a good candidate model
QWEN_VL_MODEL = "qwen/qwen3-vl-32b-instruct" 

def upload_file_to_url(file_path: str) -> Optional[str]:
    """
    Uploads a local file using manus-upload-file and returns the public URL.
    
    Args:
        file_path: Local path to the file.
        
    Returns:
        The public URL of the uploaded file, or None if upload fails.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None
        
    try:
        # Use subprocess to call the utility
        command = ["manus-upload-file", file_path]
        # Setting a timeout for the upload process
        result = subprocess.run(command, capture_output=True, text=True, check=True, timeout=60)
        
        # The utility returns the URL on stdout
        public_url = result.stdout.strip()
        if not public_url.startswith("http"):
            print(f"Upload utility returned invalid URL: {public_url}")
            return None
        
        return public_url
    except subprocess.CalledProcessError as e:
        print(f"Error during file upload (CalledProcessError): {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return None
    except subprocess.TimeoutExpired:
        print("Error: File upload timed out.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during file upload: {e}")
        return None

def analyze_image_with_qwen_vl(image_path: str, prompt: str) -> Optional[str]:
    """
    Analyzes an image using the Qwen3-VL model via OpenRouter API.
    
    Args:
        image_path: Local path to the image file.
        prompt: The text prompt for the VLM.
        
    Returns:
        The model's text response, or None if the API call fails.
    """
    # 1. Upload the image to get a public URL
    print(f"Attempting to upload image: {image_path}")
    image_url = upload_file_to_url(image_path)
    
    if not image_url:
        return "Error: Could not upload image for VLM analysis."

    print(f"Image uploaded successfully. URL: {image_url}")

    # 2. Prepare the multi-modal message payload
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": image_url}}
            ]
        }
    ]

    # 3. Call the OpenRouter API
    try:
        client = OpenAI(
            base_url=OPENROUTER_API_BASE,
            api_key=os.environ.get("OPENROUTER_API_KEY"),
        )
        
        print(f"Calling Qwen3-VL model: {QWEN_VL_MODEL}...")
        
        response = client.chat.completions.create(
            model=QWEN_VL_MODEL,
            messages=messages,
            temperature=0.2,
            max_tokens=2048
        )
        
        # 4. Extract and return the response
        if response.choices and response.choices[0].message:
            return response.choices[0].message.content
        else:
            return "Error: Qwen3-VL API returned an empty response."

    except Exception as e:
        print(f"Error during Qwen3-VL API call: {e}")
        return f"Error: Failed to communicate with Qwen3-VL API. Details: {e}"

if __name__ == '__main__':
    # Placeholder for testing
    print("Qwen3-VL API module initialized.")
    pass
