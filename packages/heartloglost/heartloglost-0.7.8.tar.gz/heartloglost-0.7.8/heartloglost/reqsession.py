import requests

def reqsession(url, params=None):
    session = requests.Session()
    session.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.1.2222.33 Safari/537.36",
        "Accept-Encoding": "*",
        "Connection": "keep-alive"
    }
    response = session.get(url, params=params)
    session.close()
    return response

# Example usage
# url = "https://example.com"
# response_text = get_response(url)
# print(response_text)