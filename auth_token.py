from cloudscraper import create_scraper

scraper = create_scraper()

headers = {
    "authority": "www.googleapis.com",
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "origin": "https://platform.arkhamintelligence.com",
    "pragma": "no-cache",
    "referer": "https://platform.arkhamintelligence.com/",
    "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "x-client-data": "CJK2yQEIo7bJAQipncoBCPL/ygEIk6HLAQiFoM0BCI2nzQE=",
    "x-client-version": "Chrome/JsCore/8.10.1/FirebaseCore-web",
}

params = {
    "key": "AIzaSyA9EERCXQ0gQstZRwcQ_Ws8XAELd2FUaXM",
}

json_data = {
    "email": "vladklp22@gmail.com",
    "password": "aa0316icman",
    "returnSecureToken": True,
}

response = scraper.post(
    "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword",
    params=params,
    headers=headers,
    json=json_data,
)


def get_token():
    access_token = response.json()["idToken"]
    print(access_token)

    return access_token
