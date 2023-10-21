import spacy
from app.nlp.scripts.dataprocess import label_data
from spacy.tokens import DocBin
from tqdm import tqdm

nlp = spacy.blank("en")

questions = [
    "Show me products from the Originals division.",
    "What's available in the Five Ten division?",
    "I'm interested in Sportswear. Can you show me products?",
    "Find me TERREX division items.",
    "What does Y-3 division offer?",
    "Show me products from adidas by Stella McCartney.",
    "I need football gear. What do you have?",
    "Can you show me items for running?",
    "I'm into cycling. What's available?",
    "Find products for tennis players.",
    "What's in stock for gym and training?",
    "I'm looking for golf equipment.",
    "Show me clothing options.",
    "What accessories do you have?",
    "I need new shoes. What's available?",
    "Find me clothing for yoga.",
    "What products does the Five Ten division offer?",
    "Show me TERREX division items for hiking.",
    "I need football gear from the Performance division.",
    "Find me Y-3 division lifestyle products.",
    "What's available in the Originals division for lifestyle?",
    "I'm looking for climbing gear.",
    "Show me winter sports equipment.",
    "Can you recommend gym and training products?",
    "I need new yoga clothing.",
    "Find me accessories from the City Outdoor division.",
]
training_data = [
    (questions[0], [(26, 35, "DIVISION")]),  # "Originals" is the division
    (questions[1], [(24, 32, "DIVISION")]),  # "Five Ten" is the division
    (questions[2], [(18, 28, "DIVISION")]),  # "Sportswear" is the division
    (questions[3], [(8, 14, "DIVISION")]),  # "TERREX" is the division
    (questions[4], [(10, 13, "DIVISION")]),  # "Y-3" is the division
    (
        questions[5],
        [(22, 48, "DIVISION")],
    ),  # "adidas by Stella McCartney" is the division
    (questions[6], [(7, 15, "SPORT")]),  # "football" is the sport
    (questions[7], [(26, 33, "SPORT")]),  # "running" is the sport
    (questions[8], [(9, 16, "SPORT")]),  # "cycling" is the sport
    (questions[9], [(18, 24, "SPORT")]),  # "tennis" is the sport
    (questions[10], [(20, 36, "SPORT")]),  # "gym and training" is the sport
    (questions[11], [(16, 20, "SPORT")]),  # "golf" is the sport
    (questions[12], [(8, 16, "CATEGORY")]),  # "clothing" is the category
    (questions[13], [(5, 16, "CATEGORY")]),  # "accessories" is the category
    (questions[14], [(11, 16, "CATEGORY")]),  # "shoes" is the category
    (questions[15], [(8, 16, "CATEGORY")]),  # "clothing" is the category
    (questions[16], [(23, 31, "DIVISION")]),
    (questions[17], [(8, 14, "DIVISION"), (34, 40, "SPORT")]),
    (questions[18], [(7, 15, "SPORT"), (30, 41, "DIVISION")]),
    (questions[19], [(8, 11, "DIVISION"), (21, 30, "SPORT")]),
    (questions[20], [(24, 33, "DIVISION"), (47, 56, "SPORT")]),
    (questions[21], [(16, 24, "SPORT")]),
    (questions[22], [(8, 21, "SPORT")]),
    (questions[23], [(18, 34, "SPORT")]),
    (questions[24], [(11, 15, "SPORT")]),
    (questions[25], [(8, 19, "CATEGORY"), (29, 41, "SPORT")]),
]

# To train model use: python -m spacy train backend/app/nlp/configs/config.cfg --output ./output --paths.train backend/app/nlp/train.spacy --paths.dev backend/app/nlp/train.spacy


def main() -> None:
    TRAIN_DATA = label_data()
    print(TRAIN_DATA[:20])

    db = DocBin()

    for text, annotations in tqdm(TRAIN_DATA):
        doc = nlp(text)
        ents = []
        for start, end, label in annotations:
            span = doc.char_span(start, end, label=label)
            if span:
                ents.append(span)
        doc.ents = ents
        db.add(doc)

    db.to_disk("/Users/conal/Projects/API_project/backend/app/nlp/train.spacy")


if __name__ == "__main__":
    main()
