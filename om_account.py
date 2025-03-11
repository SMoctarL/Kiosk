from account import Account

class OrangeMoneyAccount(Account):
    # Limites spécifiques à Orange Money
    withdraw_limit = 150000
    transfer_limit = 400000
    payment_limit = 100000
    TYPE = "OM"
    
    def __init__(self, customer, username, code_pin):
        try:
            super().__init__(customer, username, code_pin)
            # Définition du type de compte
            self.TYPE = OrangeMoneyAccount.TYPE
        except Exception as e:
            raise ValueError(f"Erreur lors de la création du compte Orange Money: {str(e)}")
    
    def withdraw(self, amount):
        """Effectue un retrait avec vérification de la limite OM"""
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Le montant doit être un nombre positif")
            
        if amount > self.withdraw_limit:
            raise ValueError(f"Le montant dépasse la limite de retrait OM ({self.withdraw_limit} {Account.currency})")
            
        try:
            return super().withdraw(amount)
        except Exception as e:
            raise ValueError(f"Erreur lors du retrait: {str(e)}")
    
    def send(self, recipient_account, amount):
        """Effectue un transfert avec vérification de la limite OM"""
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Le montant doit être un nombre positif")
            
        if amount > self.transfer_limit:
            raise ValueError(f"Le montant dépasse la limite de transfert OM ({self.transfer_limit} {Account.currency})")
            
        try:
            return super().send(recipient_account, amount)
        except Exception as e:
            raise ValueError(f"Erreur lors du transfert: {str(e)}")
    
    def payment(self, amount):
        """Effectue un paiement (fonctionnalité spécifique à OM)"""
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Le montant doit être un nombre positif")
            
        if amount > self.payment_limit:
            raise ValueError(f"Le montant dépasse la limite de paiement OM ({self.payment_limit} {Account.currency})")
            
        if amount > self.balance:
            raise ValueError(f"Solde insuffisant. Solde actuel: {self.balance} {Account.currency}")
        
        try:
            self.balance -= amount
            
            # Enregistrement de la transaction
            transaction = {
                "type": "PAIEMENT",
                "account": self.account_number,
                "amount": amount,
                "balance": self.balance
            }
            Account.account_transactions.append(transaction)
            
            print(f"Paiement de {amount} {Account.currency} effectué. Nouveau solde: {self.balance} {Account.currency}")
            return True
        except Exception as e:
            raise ValueError(f"Erreur lors du paiement: {str(e)}") 