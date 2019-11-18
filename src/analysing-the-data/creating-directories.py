from pathlib import *
p = Path("../../images/folk_thm")
if p.exists() == False:
    p.mkdir(parents=True)
    print("Path ../../images/folk_thm was created.")
else:
    print("Path ../../images/folk_thm already exists.")

