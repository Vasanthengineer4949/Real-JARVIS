# voice_assistant/config.py

import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables from the .env file

class Config:
    """
    Configuration class to hold the model selection and API keys.
    
    Attributes:
    TRANSCRIPTION_MODEL (str): The model to use for transcription ('groq', 'deepgram').
    RESPONSE_MODEL (str): The model to use for response generation ('groq').
    TTS_MODEL (str): The model to use for text-to-speech ('deepgram').
    GROQ_API_KEY (str): API key for Groq services.
    DEEPGRAM_API_KEY (str): API key for Deepgram services.
    """
    # Model selection
    TRANSCRIPTION_MODEL = 'local'  # possible values: openai, groq
    RESPONSE_MODEL = 'groq'       # possible values: openai, groq
    TTS_MODEL = 'deepgram'        # possible values: openai, deepgram

    # API keys and paes
    GROQ_API_KEY =""
    DEEPGRAM_API_KEY = ""
    @staticmethod
    def validate_config():
        """
        Validate the configuration to ensure all necessary environment variables are set.
        
        Raises:
        ValueError: If a required environment variable is not set.
        """
        if Config.TRANSCRIPTION_MODEL not in ['groq', 'deepgram', 'local']:
            raise ValueError("Invalid TRANSCRIPTION_MODEL. Must be one of ['groq', 'deepgram']")
        if Config.RESPONSE_MODEL not in ['groq']:
            raise ValueError("Invalid RESPONSE_MODEL. Must be one of ['groq']")
        if Config.TTS_MODEL not in ['deepgram']:
            raise ValueError("Invalid TTS_MODEL. Must be one of ['deepgram']")
        
        if Config.TRANSCRIPTION_MODEL == 'groq' and not Config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is required for Groq models")
        
        if Config.TRANSCRIPTION_MODEL == 'deepgram' and not Config.DEEPGRAM_API_KEY:
            raise ValueError("DEEPGRAM_API_KEY is required for Deepgram models")

        if Config.RESPONSE_MODEL == 'groq' and not Config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is required for Groq models")

        if Config.TTS_MODEL == 'deepgram' and not Config.DEEPGRAM_API_KEY:
            raise ValueError("DEEPGRAM_API_KEY is required for Deepgram models")
