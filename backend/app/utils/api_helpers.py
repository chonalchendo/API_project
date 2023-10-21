def convert_mongodb_doc_to_json(doc):
    # Convert ObjectId to its hexadecimal representation if present
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    # Add other custom conversions as needed
    # For example, convert other non-serializable types to serializable types
    return doc


def convert_dict_to_string(product: dict) -> str:
    big_string = ""
    for key, value in product.items():
        if not isinstance(value, str):
            value = str(value)
        big_string += f"{key}: {value}, "
    return big_string
