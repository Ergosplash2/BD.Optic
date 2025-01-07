import sqlite3

# singleton : 
class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.connection = None
        return cls._instance

    def connect(self, db_name="lunettes_store.db"):
        if self.connection is None:
            self.connection = sqlite3.connect(db_name)
        return self.connection

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None



class Model:
    def __init__(self):
        self.db = Database().connect()

    def creation_table(self):
        cursor = self.db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lunettes (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                designation TEXT,
                reference TEXT,
                marque TEXT,
                couleur TEXT,
                quantite INTEGER,
                prix REAL
            )
        """)
        self.db.commit()

    def ajt_LUN(self, reference, marque, couleur, quantite, prix):
        designation = f"{marque} {reference} {couleur}"
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO lunettes (designation, reference, marque, couleur, quantite, prix)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (designation, reference, marque, couleur, quantite, prix))
        self.db.commit()

    def recup_toutes_LUN(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM lunettes")
        return cursor.fetchall()

    def recup_LUN_par_id(self, lunette_id):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM lunettes WHERE ID = ?", (lunette_id,))
        return cursor.fetchone()

    def sup_LUN(self, lunette_id):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM lunettes WHERE ID = ?", (lunette_id,))
        self.db.commit()

    def rechercher_LUN(self, indice):
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT * FROM lunettes
            WHERE marque LIKE ? OR reference LIKE ? OR couleur LIKE ?
        """, (f"%{indice}%", f"%{indice}%", f"%{indice}%"))
        return cursor.fetchall()

    def modif_LUN(self, lunette_id, reference, marque, couleur, quantite, prix):
        
        current_lunette = self.recup_LUN_par_id(lunette_id)
        current_reference, current_marque, current_couleur, current_quantite, current_prix = current_lunette[2], current_lunette[3], current_lunette[4], current_lunette[5], current_lunette[6]

        new_reference = reference if reference else current_reference
        new_marque = marque if marque else current_marque
        new_couleur = couleur if couleur else current_couleur
        new_quantite = quantite if quantite is not None else current_quantite
        new_prix = prix if prix is not None else current_prix

        designation = f"{new_marque} {new_reference} {new_couleur}"

        cursor = self.db.cursor()
        cursor.execute("""
            UPDATE lunettes
            SET designation = ?, reference = ?, marque = ?, couleur = ?, quantite = ?, prix = ?
            WHERE ID = ?
        """, (designation, new_reference, new_marque, new_couleur, new_quantite, new_prix, lunette_id))
        self.db.commit()



class View:
    def printMSG(self, msg):
        print(msg)

    def afficher_LUN(self, lunettes):
        for lunette in lunettes:
            print(f"ID: {lunette[0]} | Designation: {lunette[1]} | Reference: {lunette[2]} | "
                  f"Marque: {lunette[3]} | Couleur: {lunette[4]} | Quantite: {lunette[5]} | Prix: {lunette[6]}")


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def ajt_LUN(self, reference, marque, couleur, quantite, prix):
        self.model.ajt_LUN(reference, marque, couleur, quantite, prix)
        self.view.printMSG("Ajout enregistree")

    def voir_toutes_LUN(self):
        lunettes = self.model.recup_toutes_LUN()
        self.view.afficher_LUN(lunettes)

    def sup_LUN(self, lunette_id):
        self.model.sup_LUN(lunette_id)
        self.view.printMSG("Suppression enregistree")

    def rechercher_LUN(self, indice):
        lunettes = self.model.rechercher_LUN(indice)
        self.view.afficher_LUN(lunettes)

    def modif_LUN(self, lunette_id):
        current_lunette = self.model.recup_LUN_par_id(lunette_id)
        print(f"Modification de la lunette ID {lunette_id}:")
        
        reference = input(f"Entrez la nouvelle reference (actuelle : {current_lunette[2]}): ")
        marque = input(f"Entrez la nouvelle marque (actuelle : {current_lunette[3]}): ")
        couleur = input(f"Entrez la nouvelle couleur (actuelle : {current_lunette[4]}): ")
        quantite = input(f"Entrez la nouvelle quantité (actuelle : {current_lunette[5]}): ")
        quantite = int(quantite) if quantite else current_lunette[5]
        prix = input(f"Entrez le nouveau prix (actuel : {current_lunette[6]}): ")
        prix = float(prix) if prix else current_lunette[6]

        self.model.modif_LUN(lunette_id, reference, marque, couleur, quantite, prix)
        self.view.printMSG("Modification enregistree")



class GestionDeStockLUN:
    def __init__(self):
        self.model = Model()
        self.view = View()
        self.controller = Controller(self.model, self.view)
        self.model.creation_table()

    def run(self):
        while True:
            print("\nChoisissez une action: \n1 - Afficher la base de donnees\n2 - Ajouter à la base de donnees\n"
                  "3 - Supprimer de la base de donnees\n4 - Chercher dans la base de donnees\n"
                  "5 - Modifier une lunette\n6 - Sortir")
            choice = input("Entrez votre choix: ")

            if choice == "1":
                self.controller.voir_toutes_LUN()
            elif choice == "2":
                reference = input("Entrez la reference: ")
                marque = input("Entrez la marque: ")
                couleur = input("Entrez la couleur: ")
                quantite = int(input("Entrez la quantite: "))
                prix = float(input("Entrez le prix: "))
                self.controller.ajt_LUN(reference, marque, couleur, quantite, prix)
            elif choice == "3":
                lunette_id = int(input("Entrez l'ID de la lunette à supprimer: "))
                self.controller.sup_LUN(lunette_id)
            elif choice == "4":
                indice = input("Entrez un indice a recherche (marque, reference, ou couleur): ")
                self.controller.rechercher_LUN(indice)
            elif choice == "5":
                lunette_id = int(input("Entrez l'ID de la lunette à modifier: "))
                self.controller.modif_LUN(lunette_id)
            elif choice == "6":
                Database().close_connection()
                break
            else:
                print("Choix invalide")



if __name__ == "__main__":
    app = GestionDeStockLUN()
    app.run()
