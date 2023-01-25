import requests
from config import *
headers = {"authorization": TOKEN}


def read_file(file_path, chunk_size=5242880):
    with open(file_path, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data


def upload_file(file_path):
    response = requests.post(FILE_UPLOAD_ENDPOINT, headers=headers, data=read_file(file_path))
    return response.json()["upload_url"]


def transcribe(audio_url):
    json = {"audio_url": audio_url}
    response = requests.post(TRANSCRIPT_ENDPOINT, json=json, headers=headers)
    return response.json()["id"]


def poll_transcription_status(transcript_id):
    response = requests.get(TRANSCRIPT_ENDPOINT + '/' + transcript_id, headers=headers)
    return response.json()["status"]


def get_transcription(transcript_id):
    response = requests.get(TRANSCRIPT_ENDPOINT + '/' + transcript_id, headers=headers)
    return response.json()['text']
