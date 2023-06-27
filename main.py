import argparse
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
            print(err)
            sleep(s)
            return get(url)
        if err.response.status_code == 401:
            refresh_token()
            return get(url)


def get_value(d, value):
    if isinstance(d, dict):
        return d.get(value)

    return d


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
        if arkham_entities_data:
            sub_entities = [
                get_value(new_entity, "id") for new_entity in arkham_entities_data
            ]
            result.extend(sub_entities)

    return list(set(result))


def load_query_keys(data, path="query_keys.json"):
    with open(path, "w") as file:
        json.dump(data, file)


def get_query_keys(path="query_keys.json"):
    parser = argparse.ArgumentParser()
    parser.add_argument("--more", action="store_true")
    args = parser.parse_args()

    with open(path, "r") as data:
        query_keys = json.load(data)

    if args.more:
        more_keys = get_more_entities(query_keys)
        load_query_keys(more_keys, "query_keys.json")
        return more_keys

    return query_keys


def to_correct_string(string):
    replacements = {
        "trader-joe": "traderJoe",
        "rari-capital": "rariCapital",
        "polychain-capital": "polychainCapital",
        "immutable-x": "immutableX",
        "defiance-capital": "deFianceCapital",
        "plutusdao": "plutusDao",
        "infinity-stones": "InfStones",
        "lucky-block": "luckyblock",
        "vesta-finance": "vestaFinance",
        "nexus-mutual": "nexusMutual",
        "beethoven-x": "beethovenX",
        "hundred-finance": "hundredFinance",
        "mintdice": "mintDice",
        "olympusdao": "olympusDao",
        "figment-capital": "figmentCapital",
        "crypto-com": "crypto.com",
        "pantera-capital": "panteraCapital",
        "alpaca-finance": "alpacaFinance",
        "ftx-us": "fts us",
        "layerzero": "layerZero",
        "hop-protocol": "hopProtocol",
        "xt-com": "xt.com exchange",
        "rhinofi": "rhino.fi",
        "harvest-finance": "harvestFinance",
        "bittrex*": "bittrex*",
        "axie-infinity": "axieInfinity",
        "anchor-protocol": "anchorProtocol",
        "openleverage": "openleverage",
        "rocket-pool": "rocketPool",
        "abyss-finance": "abyssFinance",
        "convex-finance": "convexFinance",
        "cake-defi": "cakeDefi",
        "tornado-cash": "tornadoCash",
        "clipper-dex": "clipperDex",
        "parafi-capital": "parafiCapital",
        "overnight": "overnight.fi",
        "across-protocol": "acrossProtocol",
        "cake-monster": "cakeMonster",
        "akuna-capital": "akunaCapital",
        "reaper-farm": "reaperFarm",
        "falconx": "falconX",
        "celsius-network": "celsiusNetwork",
        "starry-night-capital": "starryNightCapital",
        "trade-io": "trade.io",
        "flata-exchange": "flataexchange",
        "gate-io": "gate.io",
        "li-fi": "li.fi",
        "ethereum": "evm",
        "optimism": "evm",
        "polygon": "evm",
        "arbitrum_one": "evm",
        "avalanche": "evm",
        "bsc": "evm",
        "bitcoin": "btc",
        "nft-marketplace": "marketplace",
        "blur-io": "blur",
        "cex": "exchange",
        "cdp": "dex",
        "crosschain-interoperability": "bridge",
        "smart-contract-platform": "bridge"
    }

    if string in replacements:
        return replacements[string]

    return string


def get_tag(obj):
    arkham_entity = get_value(obj, "arkhamEntity")

    if arkham_entity:
        if "id" in arkham_entity:
            return to_correct_string(get_value(arkham_entity, "id"))
        else:
            return to_correct_string(get_value(arkham_entity, "name"))


def get_name(obj):
    arkham_entity = get_value(obj, "arkhamEntity")

    if arkham_entity:
        if "name" in arkham_entity:
            return to_correct_string(get_value(arkham_entity, "name"))
        else:
            return to_correct_string(get_value(arkham_entity, "id"))


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

    return to_correct_string(type)


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

            return to_correct_string(chain_type)

    chain_type = get_value(obj, "chain")

    return to_correct_string(chain_type)


def remove_duplicate_objects(lst):
    unique_objects = {}

    for obj in lst:
        if obj:
            obj_id = obj.get('id')
            if obj_id and len(obj.keys()) > 1:
                unique_objects[obj_id] = obj

    return list(unique_objects.values())


def load_token_from_search(query_keys, s):
    count = 0
    unnecessary_count = 0
    social_networks = []
    for key in query_keys[5010:]:
        print(f"{count}: {key}")
        search_field = get(
            f"https://api.arkhamintelligence.com/intelligence/search?query={key}"
        )
        arkham_addresses = get_value(search_field.json(), "arkhamAddresses")
        count += 1
        if arkham_addresses:
            for obj in arkham_addresses:
                address = get_value(obj, "address").lower()

                intelligence_address = get_intelligence_address(address)
                socials = get_socials(intelligence_address)
                social_networks.append(socials)

                name = get_name(obj)
                tag = get_tag(obj)
                type = get_type(intelligence_address)
                address_type = get_address_type(obj)

                if None in (name, tag, type):
                    print(f"unnecessary: {unnecessary_count}")
                    print(obj)
                    unnecessary_count += 1
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

    with open("socials.json", "w") as file:
        clear_socials = remove_duplicate_objects(social_networks)
        json.dump(clear_socials, file, indent=4)


def main():
    session = create_session()
    s = session()

    query_keys = get_query_keys()

    load_token_from_search(query_keys, s)


if __name__ == "__main__":
    main()
