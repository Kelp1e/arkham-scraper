import json
from time import sleep

from cloudscraper import create_scraper
from requests import HTTPError

from auth_token import get_token
from db.models import Address
from db.setup import create_session
from request_data import get_headers_for_req

CHAINS = ["bitcoin", "ethereum", "tron", "arbitrum_one"]

scraper = create_scraper()

token = get_token()
headers = get_headers_for_req(token)


def refresh_token():
    headers["authorization"] = get_token()


def get(url, s=30):
    try:
        response = scraper.get(url, headers=headers)
        response.raise_for_status()
        return response
    except HTTPError as err:
        if err.response.status_code == 429:
            print(err, f"Sleeping for {s} seconds...")
            sleep(s)
            return get(url)
        if err.response.status_code == 401:
            refresh_token()
            return get(url)


def get_value(d, value):
    if isinstance(d, dict):
        return d.get(value)

    return d


def remove_fields_from_dict(data, fields):
    for field in fields:
        if field in data:
            del data[field]


def load_query_keys(data):
    with open("query_keys.json", "w") as file:
        json.dump(data, file)


def get_query_keys():
    with open("query_keys.json", "r") as data:
        query_keys = json.load(data)
        print(query_keys)
        return query_keys


def get_entities():
    url = "https://api.arkhamintelligence.com/important_entities"
    response = get(url)

    return response.json()


def get_more_entities(entities):
    result = []

    for entity in entities:
        response = get(
            f"https://api.arkhamintelligence.com/intelligence/search?query={entity}",
        ).json()
        arkham_entities_data = get_value(response, "arkhamEntities")
        sub_entities = [
            get_value(new_entity, "id") for new_entity in arkham_entities_data
        ]
        result.extend(sub_entities)

    return list(set(result))


def to_correct_string_format(string):
    if string == "ethereum":
        return "evm"

    if string == "optimism":
        return "evm"

    if string == "nft-marketplace":
        return "marketplace"

    if string == "blur-io":
        return "blur"

    return string


def get_name(obj):
    arkham_entity = get_value(obj, "arkhamEntity")

    if arkham_entity:
        if "id" in arkham_entity:
            return get_value(arkham_entity, "id")
        else:
            return get_value(arkham_entity, "name")


def get_intelligence_address(address):
    for chain in CHAINS:
        url = f"https://api.arkhamintelligence.com/intelligence/address/{address}?chain={chain}"
        response = get(url)

        if response and response.status_code == 200:
            return response.json()

        continue


def get_type(data):
    arkham_entity = get_value(data, "arkhamEntity")
    type = get_value(arkham_entity, "type")

    return to_correct_string_format(type)


def get_socials(data):
    arkham_entity = get_value(data, "arkhamEntity")

    social_fields = ["id", "website", "twitter", "crunchbase", "linkedin"]
    if arkham_entity:
        socials = {
            key: get_value(arkham_entity, key)
            for key in social_fields
            if key in arkham_entity
        }

        return socials


def get_address_type(obj):
    arkham_label = get_value(obj, "arkhamLabel")
    if arkham_label:
        if "chainType" in arkham_label:
            chain_type = get_value(arkham_label, "chainType")

            return to_correct_string_format(chain_type)

    chain_type = get_value(obj, "chain")

    return to_correct_string_format(chain_type)


def load_socials(socials):
    path = "socials.json"
    name = get_value(socials, "id")


def load_token_from_search(query_keys, s):
    for key in query_keys:
        search_field = get(
            f"https://api.arkhamintelligence.com/intelligence/search?query={key}"
        )
        arkham_addresses = get_value(search_field.json(), "arkhamAddresses")

        for obj in arkham_addresses:
            address = get_value(obj, "address").lower()

            intelligence_address = get_intelligence_address(address)
            socials = get_socials(intelligence_address)
            load_socials(socials)

            name = get_name(obj)
            tag = get_name(obj)
            type = get_type(intelligence_address)
            address_type = get_address_type(obj)

            if None in (name, tag, type):
                continue

            db_address = s.query(Address).filter_by(address=address).first()
            if db_address:
                db_address.address = address
                db_address.name = name
                db_address.tag = tag
                db_address.type = type
                db_address.address_type = address_type
            else:
                db_address = Address(
                    address=address,
                    name=name,
                    tag=tag,
                    type=type,
                    address_type=address_type,
                )
                s.add(db_address)
            s.commit()


def main():
    session = create_session()
    s = session()

    query_keys = get_query_keys()

    load_token_from_search(query_keys, s)


if __name__ == "__main__":
    main()
