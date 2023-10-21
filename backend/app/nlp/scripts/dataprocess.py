import re
from typing import Optional

from app.data.database import get_collection
from rich import print

# ----------------------------- Get product names ---------------------------- #

sports = get_collection(database="adidas", collection="sports")
docs = sports.find()


def get_product_names(data):
    display_names = []
    for x in data:
        name = x["displayName"]
        display_names.append(name)
    return display_names


names = get_product_names(docs)
names

# ------------------------- Questions to train model ------------------------- #

questions = [
    "I want to know what the most relevant reviews said about the Terrex Trailmaker GORE-TEX Hiking Shoes",
    "what have been the most helpful reviews for the Terrex Trailmaker GORE-TEX Hiking Shoes",
    "Can you provide insights from the newest reviews for the [Product Name]",
    "What are the highest-rated reviews for the [Product Name] saying",
    "I'm interested in the lowest-rated reviews for the [Product Name]; can you share their feedback?",
    "Please tell me what customers think about the [Product Name] in their most relevant reviews.",
    "What have people been saying about the [Product Name] in the highest-rated reviews?",
    "Share insights from the newest reviews for the [Product Name].",
    "I want to know what the most relevant reviews said about the [Product Name].",
    "Can you provide insights from the lowest-rated reviews for the [Product Name]?",
    "Show me the newest reviews for the [Product Name].",
    "What are the highest-rated reviews for the [Product Name] saying?",
    "Tell me what customers think about the [Product Name] in the lowest-rated reviews.",
    "Share insights from the most helpful reviews for the [Product Name].",
    "I'm interested in the lowest-rated reviews for the [Product Name]; can you share their feedback in detail?",
    "What have been the most relevant reviews for the [Product Name]?",
    "Provide insights from the highest-rated reviews for the [Product Name].",
    "Can you show me the newest reviews for the [Product Name]?",
    "What are the most relevant reviews saying about the [Product Name]?",
    "Tell me what customers think about the [Product Name] in the most helpful reviews.",
]

replace = "[Product Name]"
name_label = ("displayName",)
reviews = ["relevant", "newest", "helpful", "highest-rated", "lowest-rated"]
review_label = ("SORT",)


def label_data() -> list[tuple[str, list[tuple, Optional[tuple]]]]:
    new_questions = []
    compiled_names = [re.compile(name) for name in names]
    compiled_reviews = [re.compile(review) for review in reviews]
    new_questions = []

    for name in compiled_names:
        for q in questions:
            new_q = q.replace(replace, name.pattern)  # Use the compiled pattern
            match_name = name.search(new_q)

            if not match_name:
                continue  # Skip to the next iteration if no match

            for review in compiled_reviews:
                match_review = review.search(new_q)

                if match_review:
                    name_span = match_name.span()
                    review_span = match_review.span()
                    name_labelled = name_span + name_label
                    review_labelled = review_span + review_label
                    anno_q = (new_q, [name_labelled, review_labelled])
                    new_questions.append(anno_q)

    return new_questions


def main() -> None:
    labelled = label_data()
    print(labelled)
    print(len(labelled))


if __name__ == "__main__":
    main()
