"""
This script converts the most frequent formula mapping JSON file to a more
usable format for robocrystallographer.

The original JSON file was generated by the matstract team and is not provided
here.
"""
import os

from monty.serialization import loadfn, dumpfn

from pymatgen import Composition

cwd = os.path.join(os.path.dirname(__file__))
formulas = loadfn(os.path.join(cwd, "relevant_formulae.json"))

new_formula_mapping = {}

skipped = 0
for formula, mappings in formulas.items():
    try:
        comp = Composition(formula)

        mappings = list(mappings.items())
        mappings = sorted(mappings, key=lambda x: x[1])

        most_seen_repr = mappings[-1][0]
        new_formula_mapping[comp.reduced_formula] = most_seen_repr
    except ValueError:
        skipped += 1
        pass

dumpfn(new_formula_mapping, "formula_db.json.gz")

print("total formulas processed: {}".format(len(new_formula_mapping.keys())))
print("total formulas skipped: {}".format(skipped))
