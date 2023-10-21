import sys

from app.data.database import get_collection
from rich import print

print(sys.path)

sports = get_collection(database="adidas", collection="sports")


docs = sports.find()


display_names = []

for x in docs:
    name = x["displayName"]
    display_names.append(name)


print(display_names)
print(len(display_names))
