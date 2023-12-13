from app.core.config import log

from .upload import upload_detailed_prod, upload_model_reviews, upload_review_stats


def product_model(prod_id: str, model_id: str) -> dict[str, str]:
    return dict(prod_id=prod_id, model_id=model_id)


prod_1 = product_model("IF2375", "MBU20")
prod_2 = product_model("GX9127", "LWY12")
prod_3 = product_model("HQ1345", "LIZ85")
prod_4 = product_model("HQ3688", "LKP28")

# restart scrape from here

prod_5 = product_model("IF4853", "LKO64")
prod_6 = product_model("IG5018", "MBU12")
prod_7 = product_model("IF4857", "LKO63")
prod_8 = product_model("ID0263", "MDF79")
prod_9 = product_model("GX9859", "LVM94")
prod_10 = product_model("HP6701", "LRE99")

small_prod = product_model("HZ2181", "DLQ15")

new_products = [prod_9, prod_10]


def main() -> None:
    for product in new_products:
        log.info(f"--- Scraping product data for product: {product['prod_id']} ---")
        upload_detailed_prod(product=product["prod_id"])

        log.info(f"--- Scraping review stats for model: {product['model_id']} ---")
        upload_review_stats(model=product["model_id"])

        log.info(f"--- Scraping all reviews for model: {product['model_id']} ---")
        upload_model_reviews(model=product["model_id"])

    log.info("--- Finished scraping ---")


if __name__ == "__main__":
    main()
