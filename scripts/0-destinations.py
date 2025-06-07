import pandas as pd
import os

list_of_destinations = ["Mont Saint Michel", "St Malo", "Bayeux", "Le Havre", "Rouen", "Paris", "Amiens", "Lille", "Strasbourg", "Chateau du Haut Koenigsbourg",
    "Colmar", "Eguisheim", "Besancon", "Dijon", "Annecy", "Grenoble", "Lyon", "Gorges du Verdon", "Bormes les Mimosas", "Cassis", "Marseille",
    "Aix en Provence", "Avignon", "Uzes", "Nimes", "Aigues Mortes", "Saintes Maries de la mer", "Collioure", "Carcassonne", "Ariege", "Toulouse",
    "Montauban", "Biarritz", "Bayonne", "La Rochelle"]

destinations = pd.DataFrame(list_of_destinations, columns=['destination'])

results_dir = os.path.join('results')
print("Saving destinations into a csv file ...")
filepath= os.path.join(results_dir, "destination_names.csv")
destinations.to_csv(filepath, index=False)
print("...Done")
print(f"All destinations are stored into : {filepath}")