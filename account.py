from prettytable import PrettyTable

class Account:
    # Attributs de classe
    currency = "CFA"
    account_count = 0
    account_transactions = []
    accounts = []
    
    def __init__(self, customer, username, code_pin):
        try:
            # Validation des données
            if not hasattr(customer, 'id'):
                raise ValueError("Le client doit avoir un ID valide")
                
            if not isinstance(username, str) or len(username) < 2:
                raise ValueError("Le nom d'utilisateur doit être une chaîne d'au moins 2 caractères")
                
            if not isinstance(code_pin, str) or len(code_pin) != 4 or not code_pin.isdigit():
                raise ValueError("Le code PIN doit être une chaîne de 4 chiffres")
            
            # Incrémentation et initialisation
            Account.account_count += 1
            self.account_number = f"ACC{Account.account_count:04d}"
            self.customer = customer
            self.username = username
            self.code_pin = code_pin
            self.balance = 0
            self.TYPE = "Standard"
            
            # Ajout à la liste des comptes
            Account.accounts.append(self)
            
        except Exception as e:
            # En cas d'erreur, décrémenter le compteur pour éviter les sauts de numéros
            if hasattr(self, 'account_number'):
                Account.account_count -= 1
                
            raise ValueError(f"Erreur lors de la création du compte: {str(e)}")
    
    def __str__(self):
        return f"Compte {self.account_number} - Client: {self.customer.firstname} {self.customer.lastname} - Solde: {self.balance} {Account.currency}"
    
    def show_balance(self):
        """Affiche le solde du compte"""
        print(f"Solde du compte {self.account_number}: {self.balance} {Account.currency}")
        return self.balance
    
    def deposit(self, amount):
        """Effectue un dépôt sur le compte"""
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Le montant doit être un nombre positif")
        
        self.balance += amount
        
        # Enregistrement de la transaction
        transaction = {
            "type": "DEPOT",
            "account": self.account_number,
            "amount": amount,
            "balance": self.balance
        }
        Account.account_transactions.append(transaction)
        
        print(f"Dépôt de {amount} {Account.currency} effectué. Nouveau solde: {self.balance} {Account.currency}")
        return True
    
    def withdraw(self, amount):
        """Effectue un retrait sur le compte"""
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Le montant doit être un nombre positif")
        
        if amount > self.balance:
            raise ValueError(f"Solde insuffisant. Solde actuel: {self.balance} {Account.currency}")
        
        self.balance -= amount
        
        # Enregistrement de la transaction
        transaction = {
            "type": "RETRAIT",
            "account": self.account_number,
            "amount": amount,
            "balance": self.balance
        }
        Account.account_transactions.append(transaction)
        
        print(f"Retrait de {amount} {Account.currency} effectué. Nouveau solde: {self.balance} {Account.currency}")
        return True
    
    def send(self, recipient_account, amount):
        """Envoie de l'argent à un autre compte"""
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Le montant doit être un nombre positif")
        
        if amount > self.balance:
            raise ValueError(f"Solde insuffisant. Solde actuel: {self.balance} {Account.currency}")
        
        # Débit du compte émetteur
        self.balance -= amount
        
        # Crédit du compte destinataire
        recipient_account.balance += amount
        
        # Enregistrement des transactions
        transaction_send = {
            "type": "ENVOI",
            "account": self.account_number,
            "recipient": recipient_account.account_number,
            "amount": amount,
            "balance": self.balance
        }
        Account.account_transactions.append(transaction_send)
        
        transaction_receive = {
            "type": "RECEPTION",
            "account": recipient_account.account_number,
            "sender": self.account_number,
            "amount": amount,
            "balance": recipient_account.balance
        }
        Account.account_transactions.append(transaction_receive)
        
        print(f"Transfert de {amount} {Account.currency} effectué vers le compte {recipient_account.account_number}.")
        print(f"Nouveau solde: {self.balance} {Account.currency}")
        return True
    
    @staticmethod
    def get_valid_username():
        while True:
            username = input("Entrez votre nom d'utilisateur: ")
            if len(username) >= 2 and all(c.isalnum() or c.isspace() for c in username):
                return username
            print("Le nom d'utilisateur doit contenir au moins 2 caractères (lettres, chiffres et espaces autorisés).")
    
    @staticmethod
    def get_valid_code_pin():
        while True:
            code_pin = input("Entrez votre code PIN (4 chiffres): ")
            if len(code_pin) == 4 and code_pin.isdigit():
                return code_pin
            print("Le code PIN doit contenir exactement 4 chiffres.")
    
    @classmethod
    def all(cls):
        """Affiche tous les comptes créés"""
        if not cls.accounts:
            print("Aucun compte n'a été créé.")
            return
        
        table = PrettyTable()
        table.field_names = ["N° Compte", "Client", "Type", "Solde"]
        
        for account in cls.accounts:
            table.add_row([
                account.account_number,
                f"{account.customer.firstname} {account.customer.lastname}",
                account.TYPE,
                f"{account.balance} {cls.currency}"
            ])
        
        print(table)
        print(f"Nombre total de comptes: {len(cls.accounts)}") 