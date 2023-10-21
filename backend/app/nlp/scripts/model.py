import spacy
from rich import print
from pathlib import Path


abs_path = Path(__file__).parent.parent


class NLPModel:
    general: str = f"{abs_path}/old_output/model-best"
    sport: str = f"{abs_path}/output/model-best"

    @staticmethod
    def model(query: str) -> dict:
        nlp_ner = spacy.load(NLPModel.sport)
        doc = nlp_ner(query)
        return_dict = {}
        for ent in doc.ents:
            if "display" not in ent.label_:
                label = ent.label_.lower()
            else:
                label = ent.label_
            return_dict[label] = ent.text
        return return_dict


if __name__ == "__main__":
    query = "I want to know what the most relevant reviews said about the Terrex Trailmaker GORE-TEX Hiking Shoes"

    response = NLPModel.model(query=query)
    print(response)
