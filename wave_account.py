from account import Account

class WaveAccount(Account):
    # Limites spécifiques à Wave
    withdraw_limit = 200000
    transfer_limit = 500000
    TYPE = "WAVE"
    
    def __init__(self, customer, username, code_pin):
        try:
            super().__init__(customer, username, code_pin)
            self.TYPE = WaveAccount.TYPE
        except Exception as e:
            raise ValueError(f"Erreur lors de la création du compte WAVE: {str(e)}")
    
    def withdraw(self, amount):
        """Effectue un retrait avec vérification de la limite Wave"""
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Le montant doit être un nombre positif")
            
        if amount > self.withdraw_limit:
            raise ValueError(f"Le montant dépasse la limite de retrait Wave ({self.withdraw_limit} {Account.currency})")
            
        try:
            return super().withdraw(amount)
        except Exception as e:
            raise ValueError(f"Erreur lors du retrait: {str(e)}")
    
    def send(self, recipient_account, amount):
        """Effectue un transfert avec vérification de la limite Wave"""
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Le montant doit être un nombre positif")
            
        if amount > self.transfer_limit:
            raise ValueError(f"Le montant dépasse la limite de transfert Wave ({self.transfer_limit} {Account.currency})")
            
        try:
            return super().send(recipient_account, amount)
        except Exception as e:
            raise ValueError(f"Erreur lors du transfert: {str(e)}") 