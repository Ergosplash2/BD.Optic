

class Model:
    def __init__(self, ID, designation, reference, marque, couleur, quantite, prix):
        self.ID = ID
        self.designation = designation
        self.reference = reference
        self.marque = marque
        self.couleur = couleur
        self.quantite = quantite
        self.prix = prix
    

class View:
    def printMSG(self, msg):
        print(msg)
    def displayLUN(self, LUN):
        print(f"ID: {LUN.ID} | Prix: {LUN.prix}")

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
    
    #def ajtLUN(self,):
    #def supLUN(self, ID):
    #def modifier_info(self, ID):
    #def search(self):

class GestionDeStockLUN:
    def main(self):
        self.model = Model()
        self.view = View()
        self.controller = Controller(lunettes_model, View)

if __name__ == "__main__":
    app = GestionDeStockLUN()
    app.run()
