import json
from logpy import facts, fact
import rel
import family

with open("relationships.json") as f:
    d = json.loads(f.read())

for item in d["father"]:
    facts(rel.father, (list(item.keys())[0], list(item.values())[0]))

for item in d["mother"]:
    facts(rel.mother, (list(item.keys())[0], list(item.values())[0]))

for item in d["males"]:
    fact(rel.male, item)

for item in d["females"]:
    fact(rel.female, item)

# print(family.spouse("Albert"))

for item in family.nieces("Mark"):
    print(item)
  