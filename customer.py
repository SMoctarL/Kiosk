class Customer:
    nb_customer = 0
    customer_list = []

    def __init__(self, cni, firstname, lastname, phone, address):
        try:
            # Validation des données
            if not isinstance(cni, str) or len(cni) != 8 or not cni.isalnum():
                raise ValueError("CNI doit être une chaîne alphanumérique de 8 caractères")
                
            if not isinstance(firstname, str) or len(firstname) < 2:
                raise ValueError("Le prénom doit être une chaîne d'au moins 2 caractères")
            
            if not all(c.isalpha() or c.isspace() or c == '-' or c == "'" for c in firstname):
                raise ValueError("Le prénom ne doit contenir que des lettres, des espaces, des tirets ou des apostrophes")
                
            if not isinstance(lastname, str) or len(lastname) < 2:
                raise ValueError("Le nom doit être une chaîne d'au moins 2 caractères")
                
            if not all(c.isalpha() or c.isspace() or c == '-' or c == "'" for c in lastname):
                raise ValueError("Le nom ne doit contenir que des lettres, des espaces, des tirets ou des apostrophes")
                
            if not isinstance(phone, str) or len(phone) != 9 or not phone.isdigit() or not phone.startswith(('70', '76', '77', '78')):
                raise ValueError("Le téléphone doit être une chaîne de 9 chiffres commençant par 70, 76, 77 ou 78")
                
            if not isinstance(address, str) or len(address) < 2:
                raise ValueError("L'adresse doit être une chaîne d'au moins 2 caractères")
                
            # Incrémentation et initialisation
            Customer.nb_customer += 1
            self.id = f"user_{Customer.nb_customer}"
            self.cni = cni
            self.firstname = firstname
            self.lastname = lastname
            self.phone = phone
            self.address = address
            self.account = None
            
            # Ajout à la liste
            Customer.customer_list.append(self)
            
        except Exception as e:
            # En cas d'erreur, décrémenter le compteur pour éviter les sauts d'ID
            if hasattr(self, 'id') and self.id:
                Customer.nb_customer -= 1

            raise ValueError(f"Erreur lors de la création du client: {str(e)}")

    def __str__(self):
        return f"ID: {self.id}, Nom: {self.lastname}, Prénom: {self.firstname}, CNI: {self.cni}, Téléphone: {self.phone}, Adresse: {self.address}"

    @staticmethod
    def get_valid_firstname_input(name="prénom"):
        while True:
            firstname = input(f"Entrez votre {name}: ")
            if len(firstname) >= 2 and all(c.isalpha() or c.isspace() or c == '-' or c == "'" for c in firstname):
                return firstname
            print(f"Le {name} doit contenir au moins 2 caractères et seulement des lettres, espaces, tirets ou apostrophes.")

    @staticmethod
    def get_valid_lastname_input(name="nom"):
        while True:
            lastname = input(f"Entrez votre {name}: ")
            if len(lastname) >= 2 and all(c.isalpha() or c.isspace() or c == '-' or c == "'" for c in lastname):
                return lastname
            print(f"Le {name} doit contenir au moins 2 caractères et seulement des lettres, espaces, tirets ou apostrophes.")

    @staticmethod
    def get_valid_address_input(name="adresse"):
        while True:
            address = input(f"Entrez votre {name}: ")
            if len(address) >= 2:
                return address
            print(f"L'{name} doit contenir au moins 2 caractères.")

    @staticmethod
    def get_valid_phone_input():
        while True:
            phone = input("Entrez votre numéro de téléphone: ")
            phone = phone.replace(" ", "")  # Supprimer les espaces
            if len(phone) == 9 and phone.isdigit() and phone.startswith(('70', '76', '77', '78')):
                return phone
            print("Le numéro doit contenir 9 chiffres et commencer par 70, 76, 77 ou 78.")

    @staticmethod
    def get_valid_cni_input():
        while True:
            cni = input("Entrez votre numéro CNI: ")
            if len(cni) == 8 and cni.isalnum():
                return cni
            print("Le CNI doit contenir exactement 8 caractères alphanumériques.")

    @staticmethod
    def get_customer_input():
        print("\n--- Création d'un nouveau client ---")
        customer_data = {
            "cni": Customer.get_valid_cni_input(),
            "lastname": Customer.get_valid_lastname_input(),
            "firstname": Customer.get_valid_firstname_input(),
            "phone": Customer.get_valid_phone_input(),
            "address": Customer.get_valid_address_input()
        }
        return customer_data

    @classmethod
    def all(cls):
        """Affiche tous les clients créés"""
        if not cls.customer_list:
            print("Aucun client n'a été créé.")
            return
        
        print("\n=== Liste des clients ===")
        for customer in cls.customer_list:
            print(customer)
        print(f"Nombre total de clients: {len(cls.customer_list)}") 