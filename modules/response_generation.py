from groq import Groq
import logging

def generate_response(model, api_key, chat_history):
    """
    Generate a response using the specified model.
    
    Args:
    model (str): The model to use for response generation.
    api_key (str): The API key for the response generation service.
    chat_history (list): The chat history as a list of messages.
    Returns:
    str: The generated response text.
    """
    try:

        if model == 'groq':
            client = Groq(api_key=api_key)
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=chat_history
            )
            return response.choices[0].message.content
        else:
            raise ValueError("Unsupported response generation model")
    except Exception as e:
        logging.error(f"Failed to generate response: {e}")
        return "Error in generating response"
