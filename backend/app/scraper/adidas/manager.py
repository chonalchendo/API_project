from .upload import upload_detailed_prod, upload_model_reviews, upload_review_stats


def product_model(prod_id: str, model_id: str) -> dict[str, str]:
    return dict(prod_id=prod_id, model_id=model_id)


prod_1 = product_model("IF2375", "MBU20")
prod_2 = product_model("GX9127", "LWY12")
small_prod = product_model("HZ2181", "DLQ15")


def product() -> None:
    upload_detailed_prod(product=prod_2["prod_id"])


def review_stats() -> None:
    upload_review_stats(model=prod_2["model_id"])


def reviews() -> None:
    upload_model_reviews(model=prod_2["model_id"])


if __name__ == "__main__":
    reviews()
