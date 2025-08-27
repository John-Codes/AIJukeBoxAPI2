import json
import re

class JSONResponseParser:
    def __init__(self, llm_client):
        """
        Initialize the JSONResponseParser with an LLM client.
        
        Args:
            llm_client: An instance of the LLM client used for cleaning responses
        """
        self.llm_client = llm_client
    
    def parse_json_response(self, response_text, clean_prompt=None):
        """
        Parse JSON response with optional cleaning.
        
        Args:
            response_text (str): The response text to parse
            clean_prompt (str, optional): Prompt to clean the response if needed
            
        Returns:
            dict: Parsed JSON result or None if parsing fails
        """
        try:
            # Remove Markdown formatting
            cleaned_response = re.sub(r"```json|```", "", response_text).strip()
            
            # Try to parse the response as JSON
            result = json.loads(cleaned_response)
            
            # Ensure all required keys are present
            if all(key in result for key in ["relevant", "type", "confidence"]):
                return result
        except:
            pass  # Continue to cleaning attempt if provided
        
        # If parsing failed and we have a clean prompt, try cleaning
        if clean_prompt:
            try:
                clean_response = self.llm_client.call_llm(clean_prompt + response_text)
                print("\033[93mCleaned JSON response:\033[0m", clean_response)
                
                result = json.loads(clean_response)
                if all(key in result for key in ["relevant", "type", "confidence"]):
                    return result
            except:
                pass  # Will return None to indicate failure
        
        return None  # Indicates parsing failed
    
    def parse_song_picker_json(self, response_text, clean_prompt=None):
        """
        Parse and validate JSON response for song picker with required keys.
        
        Required keys:
        - "acceptable" (boolean): Whether the song is acceptable
        - "roast" (string): Roast message about the song choice
        
        Args:
            response_text (str): The response text to parse
            clean_prompt (str, optional): Prompt to clean the response if needed
            
        Returns:
            dict: Parsed JSON result with all required keys or None if parsing fails
        """
        # Define required keys for song picker
        required_keys = ["acceptable", "roast"]
        
        try:
            # Remove Markdown formatting
            cleaned_response = re.sub(r"```json|```", "", response_text).strip()
            
            # Try to parse the response as JSON
            result = json.loads(cleaned_response)
            
            # Validate required keys and their types
            if (all(key in result for key in required_keys) and
                isinstance(result["acceptable"], bool) and
                isinstance(result["roast"], str)):
                return result
        except:
            pass  # Continue to cleaning attempt if provided
        
        # If parsing failed and we have a clean prompt, try cleaning
        if clean_prompt:
            try:
                clean_response = self.llm_client.call_llm(clean_prompt + response_text)
                print("\033[93mCleaned JSON response:\033[0m", clean_response)
                
                result = json.loads(clean_response)
                if (all(key in result for key in required_keys) and
                    isinstance(result["acceptable"], bool) and
                    isinstance(result["roast"], str)):
                    return result
            except:
                pass  # Will return None to indicate failure
        
        return None  # Indicates parsing failed
    
    def parse_custom_song_picker_json(self, response_text, clean_prompt=None):
        """
        Parse and validate JSON response for custom song picker with required keys.
        
        Required keys:
        - "acceptable" (boolean): Whether the song is acceptable
        - "roast" (string): Roast message about the song choice
        
        Args:
            response_text (str): The response text to parse
            clean_prompt (str, optional): Prompt to clean the response if needed
            
        Returns:
            dict: Parsed JSON result with all required keys or None if parsing fails
        """
        # Define required keys for custom song picker (same as regular song picker)
        required_keys = ["acceptable", "roast"]
        
        try:
            # Remove Markdown formatting
            cleaned_response = re.sub(r"```json|```", "", response_text).strip()
            
            # Try to parse the response as JSON
            result = json.loads(cleaned_response)
            
            # Validate required keys and their types
            if (all(key in result for key in required_keys) and
                isinstance(result["acceptable"], bool) and
                isinstance(result["roast"], str)):
                return result
        except:
            pass  # Continue to cleaning attempt if provided
        
        # If parsing failed and we have a clean prompt, try cleaning
        if clean_prompt:
            try:
                clean_response = self.llm_client.call_llm(clean_prompt + response_text)
                print("\033[93mCleaned JSON response:\033[0m", clean_response)
                
                result = json.loads(clean_response)
                if (all(key in result for key in required_keys) and
                    isinstance(result["acceptable"], bool) and
                    isinstance(result["roast"], str)):
                    return result
            except:
                pass  # Will return None to indicate failure
        
        return None  # Indicates parsing failed
