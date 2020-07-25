import requests


def list_for_sale(city, state_code, limit=50):
    url = "https://realtor.p.rapidapi.com/properties/v2/list-for-sale"

    querystring = {"sort": "relevance", "city": city, "limit": limit,
                   "offset": "0", "state_code": state_code}

    headers = {
        'x-rapidapi-host': "realtor.p.rapidapi.com",
        # 'x-rapidapi-key': INSERT REALTOR API KEY HERE!
    }

    response = requests.request("GET", url,
                                headers=headers, params=querystring)

    results = response.json()

    return results["properties"]


def detail(property_id):
    url = "https://realtor.p.rapidapi.com/properties/v2/detail"

    querystring = {"property_id": property_id}

    headers = {
        'x-rapidapi-host': "realtor.p.rapidapi.com",
        'x-rapidapi-key': "6a4ed64e38mshee54b26379b40d7p107093jsn36e25acd943f"
    }

    response = requests.request("GET", url,
                                headers=headers, params=querystring)

    result = response.json()["properties"][0]

    return result


def type_filter(input):
    if input == "multi_family":
        return "Multi-Family"
    elif input == "single_family":
        return "Single-Family"
    elif input == "condo":
        return "Condo"
    else:
        return "Unknown Type"


def usd(input):
    return "$" + "{:,}".format(input)


def status_filter(input):
    if input == "for_sale":
        return "For Sale"
    else:
        return "Not For Sale"
