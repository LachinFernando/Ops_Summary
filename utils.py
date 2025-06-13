import streamlit as st
import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import googleapiclient.discovery


YOUTUBE_SECRETS = "youtube_secrets.json"


def get_google_creds(credential_file_path: str) -> Credentials:
    creds = None

    creds = Credentials.from_authorized_user_file(credential_file_path)
    if not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

    return creds


def convert_time_to_ms(time_str: str) -> int:
    h, m, s, ms = time_str.replace(".", ":").split(":")
    
    ms_time = (int(h) * 3600 + int(m) * 60 + int(s)) * 1000 + int(ms)
    
    return ms_time


def parse_transcript_text(caption_data: str) -> list:
    list_transcript = []
    
    for block in caption_data.strip().split("\n\n"):
        lines = block.split("\n")
        if len(lines) >= 2:
            # Extract text
            text = lines[1]
            if text == "e":
                continue
            
            # Extract timing
            timing = lines[0]
            start_time, end_time = timing.split(",")
            start_time = convert_time_to_ms(start_time)
            end_time = convert_time_to_ms(end_time)
            
            list_transcript.append({"text": text, "start": start_time, "end": end_time})
    
    return list_transcript


def get_youtube_transcript(video_id: str) -> list:
    # fetch youtube secrets
    youtube_secrets = dict(st.secrets["youtube"])

    # write a json
    with open(YOUTUBE_SECRETS, "w") as f:
        f.write(json.dumps(youtube_secrets))

    api_service_name = "youtube"
    api_version = "v3"
    auth_location = YOUTUBE_SECRETS

    credentials = get_google_creds(auth_location)

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials
    )

    response = youtube.captions().list(part="id,snippet", videoId=video_id).execute()

    caption_id = None
    for item in response.get("items", []):
        if item["snippet"]["language"] == "en":
            caption_id = item["id"]
            break

    if not caption_id:
        raise Exception("Transcript is not available")

    caption_response = youtube.captions().download(id=caption_id).execute()

    caption_data = caption_response.decode("utf-8")

    list_transcript = parse_transcript_text(caption_data)
    
    return list_transcript