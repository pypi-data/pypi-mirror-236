import requests
from bs4 import BeautifulSoup
import json
import os
import asyncio
import math

class STClient:
    def __init__(self, username, api_key):
        self.username = username
        self.api_key = api_key
    def auth(self):
        if not all((self.username, self.api_key)):
            raise ValueError("Username, password, and API key must be specified.")
        Api_info = f"https://api.streamtape.com/account/info?login={self.username}&key={self.api_key}"
        try:
            response = requests.get(Api_info)
            response.raise_for_status()  # Raise an exception if the request was not successful
            json_data = response.json()
            a_api = json_data["status"]
            if int(a_api) == 200:
                print("You are authorised")
            else:
                print("Unsuccessful ! Check credentials.")
        except Exception as e:
            print(e)

    def upload_video(self, file_path, folder_id):
        Main_API = f"https://api.streamtape.com/file/ul?login={self.username}&key={self.api_key}&folder={self.folder_id}"
        try:
            response = requests.get(Main_API)
            response.raise_for_status()  # Raise an exception if the request was not successful
            json_data = response.json()
            temp_api = json_data["result"]["url"]
            print("Temp URL:" + temp_api)
            files = {'file': open(file_path, 'rb')}
            response = requests.post(temp_api, files=files)
            response.raise_for_status()
            data_f = response.json()
            download_link = data_f["result"]["url"]
            print(download_link)
            return download_link
        except requests.exceptions.RequestException as e:
            print("Request Exception:", e)
            return f"Error {e}"

    def tapeimg_url(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            og_image_tag = soup.find('meta', {'name': 'og:image'})
            if og_image_tag:
                image_url = og_image_tag['content']
                return image_url
            else:
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def add_remote(self, url, folder_id=None, name=None):
        # Main_API = f"https://api.streamtape.com/file/ul?login={self.username}&key={self.api_key}&folder={self.folder_id}"
        if url:
            try:
                Main_API = f"https://api.streamtape.com/remotedl/add?login={self.username}&key={self.api_key}&url={url}"
                payload = {}
                if name:
                    payload["name"] = name
                if folder_id:
                    payload["folder"] = folder_id
                response = requests.get(Main_API, params=payload)
                response.raise_for_status()  # Raise an exception if the request was not successful
                json_data = response.json()
                remote_id = json_data["result"]["id"]
                print("UpID:" + remote_id)
                return remote_id
            except requests.exceptions.RequestException as e:
                print("Request Exception:", e)
                return f"Error {e}"
        else:
            return "Please Give Api Key/url/"

    # check out docs\streamtape_gud\remotestatus.md
    def remote_status(self, id):
        if id:
            try:
                Main_API = f"https://api.streamtape.com/remotedl/status?login={self.username}&key={self.api_key}&id={id}"
                payload = {}
                response = requests.get(Main_API, params=payload)
                response.raise_for_status()  # Raise an exception if the request was not successful
                json_data = response.json()
                # print("UpID:" + json_data)
                return json_data
            except requests.exceptions.RequestException as e:
                print("Request Exception:", e)
                return f"Error {e}"
        else:
            return "Please Give id and what to get"

# idd = "FVAaYwD_ULM"
# json_res = client.remote_status("FVAaYwD_ULM")
# a = client.remote_status("J4Cx7hXoT1s")
# print(a["status"])

def add_parm(dicti, name, value):
    dicti[f"{name}"] = value

# Example usage:
# client = STClient("your_username", "your_api_key")
# client.auth()
# client.upload_video("path_to_video.mp4", "folder_id"
