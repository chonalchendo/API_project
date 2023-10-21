import json
from rich import print

# Define the path to the JSON file
json_file_path = "/Users/conal/Projects/API_project/data/nike.json"

# Open the JSON file for reading
try:
    with open(json_file_path, "r") as json_file:
        # Load the JSON data from the file
        data = json.load(json_file)

        # Now you can work with the JSON data as a Python dictionary
        print("JSON data loaded successfully:")
        index = 0
        links = []
        results = True
        while results:
            try:
                # link = data["data"]["filteredProductsWithContext"]["navlinks"][
                #     "categories"
                # ][index]["navigation"]["path"]
                link = data["data"]["filteredProductsWithContext"]["navlinks"][
                    "filters"
                ][index]['options'][index]["navigation"]["path"]
                links.append(link)
                index += 1
            except:
                results = False

        print(links)
except FileNotFoundError:
    print(f"The file '{json_file_path}' does not exist.")
except json.JSONDecodeError as e:
    print(f"JSON decoding error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

# paths = {
#     "all_shoes": "mens-shoes-nik1zy7ok",
#     "lifestyle": "mens-lifestyle-shoes-13jrmznik1zy7ok",
#     "jordan": "mens-jordan-shoes-37eefznik1zy7ok",
# }


# f"https://api.nike.com/cic/browse/v2?queryid=filteredProductsWithContext&anonymousId=990731FC3A4646EAC61EE5235F81DEBD&uuids=0f64ecc7-d624-4e91-b171-b83a03dd8550,16633190-45e5-4830-a068-232ac7aea82c,193af413-39b0-4d7e-ae34-558821381d3f&language=en-GB&country=GB&channel=NIKE&localizedRangeStr=%7BlowestPrice%7D%E2%80%94%7BhighestPrice%7D&path=/gb/w/{path}"


# "https://api.nike.com/cic/browse/v2?queryid=products&anonymousId=990731FC3A4646EAC61EE5235F81DEBD&country=gb&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(GB)%26filter%3Dlanguage(en-GB)%26filter%3DemployeePrice(true)%26filter%3DattributeIds(0f64ecc7-d624-4e91-b171-b83a03dd8550%2C16633190-45e5-4830-a068-232ac7aea82c%2C193af413-39b0-4d7e-ae34-558821381d3f)%26anchor%3D24%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D24&language=en-GB&localizedRangeStr=%7BlowestPrice%7D%E2%80%94%7BhighestPrice%7D"
