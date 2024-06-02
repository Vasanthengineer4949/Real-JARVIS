import logging
import time
from colorama import Fore, init
from modules.audio import record_audio, play_audio
from modules.transcription import transcribe_audio
from modules.response_generation import generate_response
from modules.text_to_speech import text_to_speech
from modules.utils import delete_file, find_function
from modules.config import Config
from modules.api_key_manager import get_transcription_api_key, get_response_api_key, get_tts_api_key
from modules.calendar_events import get_events, create_event
from modules.vision import explain_webcam, explain_screen
from modules.clipboard import clipboard_prompt

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

init(autoreset=True)

class JARVIS:

    def __init__(self):

        self.chat_history = [
        {"role": "system", "content": "You are JARVIS close similar to same JARVIS in Iron Man movie but created by me your boss Vasanth in Neural Hacks with Vasanth labs. You are a helpful Assistant. Keep your answers short and concise. I am Vasanth your boss who is an AI engineer. Address me only as Sir."}
        ]
        self.transcription_api_key = get_transcription_api_key()
        self.response_api_key = get_response_api_key()
        self.tts_api_key = get_tts_api_key()

    def response_generation(self, function_to_perform, user_input):

        if function_to_perform == "get_events":
            events_i_have = get_events()
            user_input ="My Upcoming Meeting Information: " + events_i_have + "\n" + user_input
            self.chat_history.append(
                                        {
                                            "role": "user", 
                                            "content": user_input
                                        }
                                    )
            response_text = generate_response(
                                                Config.RESPONSE_MODEL, 
                                                self.response_api_key, 
                                                self.chat_history
                                            )
            
            self.chat_history.append(
                                        {
                                            "role": "assistant", 
                                            "content": response_text  
                                        }
                                    )
            return response_text

        
        elif function_to_perform == "create_event":
            date = input("Enter Date of Meeting Format: YYYY-MM-DD")
            start_time = input("Enter meeting starting time Format: 12:00pm/am")
            end_time = input("Enter meeting ending time Format: 12:00pm/am")
            summary = input("Enter a title for the meeting/event")
            create_event(date, start_time, end_time, summary)
            response_text = "Event Created and Added to Your Calendar Successfully Sir"
            self.chat_history.append(
                                        {
                                            "role": "user", 
                                            "content": user_input  
                                        }
                                    )
            self.chat_history.append(
                                        {
                                            "role": "assistant", 
                                            "content": response_text  
                                        }
                                    )
            return response_text
        
        elif function_to_perform == "explain_webcam":
            webcam_explanation = explain_webcam(user_input)

            user_input ="Here is an explanation of what is there in webcam: " + webcam_explanation + "\n" + user_input + "\nBased on the explanation provide your simple explanation"

            self.chat_history.append(
                                        {
                                            "role": "user", 
                                            "content": user_input
                                        }
                                    )
            response_text = generate_response(
                                                Config.RESPONSE_MODEL, 
                                                self.response_api_key, 
                                                self.chat_history
                                            )
            self.chat_history.append(
                                        {
                                            "role": "assistant", 
                                            "content": response_text  
                                        }
                                    )
            return response_text


        elif function_to_perform == "explain_screen":
            screen_explanation = explain_screen(user_input)

            user_input ="Here is an explanation of what is there in computer screen: " + screen_explanation + "\n" + user_input + "\nBased on the explanation provide your simple explanation"

            self.chat_history.append(
                                        {
                                            "role": "user", 
                                            "content": user_input
                                        }
                                    )
            response_text = generate_response(
                                                Config.RESPONSE_MODEL, 
                                                self.response_api_key, 
                                                self.chat_history
                                            )
            self.chat_history.append(
                                        {
                                            "role": "assistant", 
                                            "content": response_text  
                                        }
                                    )
            return response_text

        elif function_to_perform == "clipboard_prompt":
            user_input = clipboard_prompt(user_input)

            self.chat_history.append(
                                        {
                                            "role": "user", 
                                            "content": user_input
                                        }
                                    )
            response_text = generate_response(
                                                Config.RESPONSE_MODEL, 
                                                self.response_api_key, 
                                                self.chat_history
                                            )
            self.chat_history.append({"role": "assistant", "content": response_text})
            return response_text

        elif function_to_perform == "general":
            self.chat_history.append(
                                        {
                                            "role": "user", 
                                            "content": user_input
                                        }
                                    )
            response_text = generate_response(
                                                Config.RESPONSE_MODEL, 
                                                self.response_api_key, 
                                                self.chat_history
                                            )
            self.chat_history.append({"role": "assistant", "content": response_text})
            return response_text

        else:
            return "Sorry Sir! Unable to do the task provided"

    def run_jarvis(self):

        try:
            
            # Audio input
            record_audio("input.wav")

            # Transcribe user audio input
            user_input = transcribe_audio(
                                            Config.TRANSCRIPTION_MODEL,
                                            self.transcription_api_key, 
                                            "input.wav"
                                        )
            logging.info(Fore.GREEN + "You said: " + user_input) 
            
            # Find the appropriate function to complete the task
            function_to_perform = find_function(user_input)["function"]
            print(function_to_perform)

            # Response Generation for the given task
            response_text = self.response_generation(
                                                    function_to_perform,    
                                                    user_input
                                                )
            logging.info(Fore.CYAN + "Response: " + response_text)

            # Convert the response text to speech and save it to the appropriate file
            text_to_speech(
                            Config.TTS_MODEL, 
                            self.tts_api_key, 
                            response_text, 
                            "output.wav"
                        )
            
            # Play the generated speech audio
            play_audio("output.wav")
            
        except Exception as e:
            logging.error(Fore.RED + f"An error occurred: {e}")
            delete_file('input.wav')
            if 'output_file' in locals():
                delete_file("output.wav")
            time.sleep(1)

if __name__ == "__main__":
    jarvis = JARVIS()
    while True:
        jarvis.run_jarvis()
            


