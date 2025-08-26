import os
from dotenv import load_dotenv
from openai import OpenAI
import logging

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self):
        """
        Initialize the LLM client with OpenRouter API configuration.
        """
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
        
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )
        
        # Optional headers for rankings on openrouter.ai
        self.headers = {
            "HTTP-Referer": os.getenv("SITE_URL", ""),  # Optional
            "X-Title": os.getenv("SITE_NAME", ""),      # Optional
        }

    def call_llm(self, prompt, model="mistralai/mistral-small-3.2-24b-instruct:free", **kwargs):
        """
        One-liner method to call the LLM with a prompt.
        
        Args:
            prompt (str): The input prompt for the LLM
            model (str): The model to use (default: qwen/qwen3-coder)
            **kwargs: Additional arguments to pass to the API
            
        Returns:
            str: The response from the LLM
        """
        try:
            completion = self.client.chat.completions.create(
                extra_headers=self.headers,
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                **kwargs
            )
            return completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Error calling LLM: {e}")
            raise

    def ask_question(self, question, model="qwen/qwen3-coder:free"):
        """
        Convenience method to ask a question.
        
        Args:
            question (str): The question to ask
            model (str): The model to use
            
        Returns:
            str: The response from the LLM
        """
        return self.call_llm(question, model)

# Example usage
if __name__ == "__main__":
    # Initialize the client
    llm_client = LLMClient()
    
    # Example: Ask a question
    try:
        response = llm_client.ask_question("What is the meaning of life?")
        print("Response:", response)
    except Exception as e:
        print(f"Error: {e}")
