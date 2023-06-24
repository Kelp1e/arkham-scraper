import json

# https://securetoken.googleapis.com/v1/token?key=AIzaSyA9EERCXQ0gQstZRwcQ_Ws8XAELd2FUaXM
# AIzaSyA9EERCXQ0gQstZRwcQ_Ws8XAELd2FUaXM
# APZUo0TScmv9ltCZVH28QEN46-JoPyWSZGC_9KerLiDautnZJEFWLb1eHzQsceY9ZXUNve-6w7NoXI29g3-7R--LHHzTW9H8j5LmNp1iIAaWVbF6HJRzLyeqH-JUsgZ5nTgzy7QmAE20sZHIr4TpGQtt-kXv59NVZueDZYemw8RjBN909IgjHZYZ91E0NamdVkUzq-F3-WFTKmVUFdUh
from cloudscraper import create_scraper

from request_data import headers

scraper = create_scraper()


def get_entities():
    url = "https://api.arkhamintelligence.com/important_entities"
    response = scraper.get(url, headers=headers)
    print(response)

    return response.json()


def get_more_entities(entities):
    result = []

    for entity in entities:
        response = scraper.get(
            f"https://api.arkhamintelligence.com/intelligence/search?query={entity}",
            headers=headers,
        ).json()
        arkham_entities_data = response.get("arkhamEntities", [])
        sub_entities = [new_entity["id"] for new_entity in arkham_entities_data]
        result.extend(sub_entities)

    return list(set(result))


def load_query_keys(data):
    with open("query_keys.json", "w") as file:
        json.dump(data, file)


def get_query_keys():
    with open("query_keys.json", "r") as data:
        return json.load(data)


