import openai
from abstract_security.envy_it import get_env_value
class ApiManager:
    def __init__(self,content_type=None,header=None,api_env:str=None,api_key:str=None):
        self.content_type=content_type or 'application/json'
        self.api_env=api_env or 'OPENAI_API_KEY'
        self.api_key=api_key or self.get_openai_key()
        self.header=header or self.get_header()
        self.load_openai_key()
    def get_openai_key(self):
        """
        Retrieves the OpenAI API key from the environment variables.

        Args:
            key (str): The name of the environment variable containing the API key. 
                Defaults to 'OPENAI_API_KEY'.

        Returns:
            str: The OpenAI API key.
        """
        return get_env_value(key=self.api_env)
    def load_openai_key(self):
        """
        Loads the OpenAI API key for authentication.
        """
        openai.api_key = self.api_key
    def get_header(self):
        """
        Generates request headers for API call.
        
        Args:
            content_type (str): Type of the content being sent in the request. Default is 'application/json'.
            api_key (str): The API key for authorization. By default, it retrieves the OpenAI API key.
            
        Returns:
            dict: Dictionary containing the 'Content-Type' and 'Authorization' headers.
        """
        return {'Content-Type': self.content_type, 'Authorization': f'Bearer {self.api_key}'}
    
