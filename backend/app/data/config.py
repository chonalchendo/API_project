from urllib.parse import quote


class Urls:
    NIKE = "https://api.nike.com/cic/browse/v2?queryid=products&anonymousId=990731FC3A4646EAC61EE5235F81DEBD&country=gb&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(GB)%26filter%3Dlanguage(en-GB)%26filter%3DemployeePrice(true)%26filter%3DattributeIds(16633190-45e5-4830-a068-232ac7aea82c%2Cce478c9c-2649-4b02-b19c-6e2b865e1ede)%26anchor%3D48%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D24&language=en-GB&localizedRangeStr=%7BlowestPrice%7D%E2%80%94%7BhighestPrice%7D"
    URL = "https://www.adidas.co.uk/terrex"
    ADIDAS = "https://www.adidas.co.uk/api/plp/content-engine?query=originals&start=48"
    AD2 = "https://www.adidas.co.uk/api/plp/content-engine?experiment=CORP_BEN%2CPDE-9700-1&query=terrex"


links = ["originals", "terrex", "sportswear"]


PROXY = f"http://{quote('qC96RNAuJuLnWjOo')}:{quote('EuXkdltqFZvutzXQ')}@geo.iproyal.com:12321"

