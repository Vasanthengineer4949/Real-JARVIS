# voice_assistant/utils.py

import os
import logging
from groq import Groq
import ast

os.environ["GROQ_API_KEY"] = ""

groq = Groq()

def delete_file(file_path):
    try:
        os.remove(file_path)
        logging.info(f"Deleted file: {file_path}")
    except FileNotFoundError:
        logging.warning(f"File not found: {file_path}")
    except PermissionError:
        logging.error(f"Permission denied when trying to delete file: {file_path}")
    except OSError as e:
        logging.error(f"Error deleting file {file_path}: {e}")

def find_function(task):

    fcs = """
        You have access to lots of Python functions which provides you the capabilities to do various tasks. Here are the functions:

        Functions - Purpose

        get_events() - To know the list of events and meetings 
        create_event(start_time, end_time, summary) - Create/Schedule new meetings or events
        explain_webcam(question) - Captures webcam and answers the question based on the captured image
        explain_screen(question) - Captures the screen and answers the question based on the captured image
        clipboard_prompt(question) - Formats an input prompt to give to LLM to explain what is stored in the clipboard
        general(question) - Answer any given question which doesnt fall under any of the other functions

        Now based on the function and description provided return the function name that suits to do a given task as JSON as follows:

        'function': 'function_name'

        Task:
        {task}
    """

    chat_completion = groq.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are great in accessing tools.\n"
            },
            {
                "role": "user",
                "content": fcs.format(task=task),
            },
        ],
        model="mixtral-8x7b-32768",
        temperature=0,
        # Streaming is not supported in JSON mode
        stream=False,
        # Enable JSON mode by setting the response format
        response_format={"type": "json_object"},
    )
    function = ast.literal_eval(chat_completion.choices[0].message.content)
    return function