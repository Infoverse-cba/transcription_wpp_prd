import json
import base64
import requests
from datetime import datetime
import whisper
import sys

sys.path.append('/path/to/ffmpeg')

class AudioTranscriptionBot:
    """
    This class handles the process of fetching audio files from an API, converting audio from MP3 to text using the Whisper model,
    and sending the transcribed text back to the API.
    """

    def __init__(self, config_file: str = 'conf.json'):
        """
        Initializes the bot by loading configuration settings.

        :param config_file: Path to the configuration file (default is 'conf.json').
        """
        self.config = self.load_config(config_file)
        self.model = whisper.load_model("base")  # Load Whisper transcription model

    def load_config(self, file_name: str) -> dict:
        """
        Loads the bot's configuration from a JSON file.

        :param file_name: The name of the JSON file containing the configuration.
        :return: A dictionary with the configuration.
        """
        with open(file_name, 'r') as file:
            config = json.load(file)
        return config

    def get_messages(self) -> str:
        """
        Retrieves audio messages from the API, decodes them from base64, and saves the audio to an MP3 file.

        :return: The ID of the message retrieved from the API.
        """
        headers = {
            "Content-Type": "application/json",
            "X-API-KEY": self.config['API'].get('token')
        }
        session = requests.Session()
        response = session.get('https://api.infoverse.com.br/v1/Bot_adm/file_transcription/1', headers=headers)

        if response.json()['status']:
            data = response.json()['data'][0]
            base64_string = data['base64']
            id_message = data['id_message']
            
            with open('audio.txt', 'w') as file:
                file.write(base64_string)

            sound_data = base64.b64decode(base64_string)
            with open('audio.mp3', 'wb') as file:
                file.write(sound_data)

            return id_message
        else:
            return None

    def mp3_to_text(self, mp3_file_path: str = 'audio.mp3') -> str:
        """
        Converts an MP3 file to text using the Whisper model.

        :param mp3_file_path: The path to the MP3 file (default is 'audio.mp3').
        :return: The transcribed text from the audio.
        """
        try:
            start_time = datetime.now()
            result = self.model.transcribe(mp3_file_path)
            text = result['text']
            processing_time = datetime.now() - start_time
            print(f"Processing time: {processing_time}")
            return text
        except Exception as e:
            print(f"Error during transcription: {e}")
            return 'Transcription error'

    def send_text(self, text: str, id_message: str):
        """
        Sends the transcribed text back to the API.

        :param text: The transcribed text to send.
        :param id_message: The ID of the message being processed.
        """
        headers = {
            "Content-Type": "application/json",
            "X-API-KEY": self.config['API'].get('token')
        }
        session = requests.Session()
        payload = {
            'transcrition_text': text,
            'id': id_message
        }

        response = session.post('https://api.infoverse.com.br/v1/Bot_adm/file_transcription', headers=headers, data=json.dumps(payload))
        print(f"Response status code: {response.status_code}")
        print(f"Response text: {response.text}")
        print(f"Transcribed text: {text}")

    def run(self):
        """
        Main loop to continuously fetch audio messages, transcribe them, and send the transcribed text back to the API.
        """
        while True:
            id_message = self.get_messages()
            if id_message is not None:
                transcribed_text = self.mp3_to_text('audio.mp3')
                self.send_text(transcribed_text, id_message)
            else:
                print('\rNo messages found', end='', flush=True)

if __name__ == '__main__':
    bot = AudioTranscriptionBot()
    bot.run()