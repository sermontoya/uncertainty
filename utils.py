import csv

def load_data(filename):
    data = dict()
    file = csv.DictReader(open(filename))
    for row in file:
        name = row["name"]
        mother = row["mother"] or None
        father = row["father"] or None
        trait = (True if row["trait"] == "1" else
                 False if row["trait"] == "0" else None)
        data[name] = {
            "name": name,
            "mother": mother,
            "father": father,
            "trait": trait
        }
    return data