def get_headers_for_req(token):
    headers = {
        "authority": "api.arkhamintelligence.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7",
        "cache-control": "no-cache",
        "authorization": token,
        "origin": "https://platform.arkhamintelligence.com",
        "pragma": "no-cache",
        "referer": "https://platform.arkhamintelligence.com/",
        "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    }

    return headers
