import os
import sys
import subprocess
from customer import Customer
from account import Account
from wave_account import WaveAccount
from om_account import OrangeMoneyAccount

# Import du nouveau module d'interface graphique
from gui import run_app

def create_customer():
    """Crée et retourne un objet de la classe Customer"""
    customer_data = Customer.get_customer_input()
    customer = Customer(
        customer_data["cni"],
        customer_data["firstname"],
        customer_data["lastname"],
        customer_data["phone"],
        customer_data["address"]
    )
    print(f"Client créé avec succès! ID: {customer.id}")
    return customer

def get_customer(customer_id):
    """Cherche et retourne un client par son ID, ou None s'il n'existe pas"""
    for customer in Customer.customer_list:
        if customer.id == customer_id:
            return customer
    return None

def create_wave_account():
    """Crée un client et un compte Wave associé"""
    customer = create_customer()
    print("\n--- Création d'un compte WAVE ---")
    username = Account.get_valid_username()
    code_pin = Account.get_valid_code_pin()
    account = WaveAccount(customer, username, code_pin)
    print(f"Compte WAVE créé avec succès! Numéro: {account.account_number}")
    return account

def create_om_account():
    """Crée un client et un compte Orange Money associé"""
    customer = create_customer()
    print("\n--- Création d'un compte Orange Money ---")
    username = Account.get_valid_username()
    code_pin = Account.get_valid_code_pin()
    account = OrangeMoneyAccount(customer, username, code_pin)
    print(f"Compte Orange Money créé avec succès! Numéro: {account.account_number}")
    return account

def get_and_validate_amount():
    """Demande un montant, vérifie s'il est positif et le retourne converti en entier"""
    while True:
        try:
            amount = int(input("Entrez le montant: "))
            if amount <= 0:
                print("Le montant doit être positif.")
                continue
            return amount
        except ValueError:
            print("Veuillez entrer un nombre valide.")

def auth_user(account):
    """Authentifie un utilisateur par son username et code PIN"""
    if not account:
        print("Compte inexistant.")
        return False
        
    username = input("Entrez votre nom d'utilisateur: ")
    code_pin = input("Entrez votre code PIN: ")
    
    if username == account.username and code_pin == account.code_pin:
        print("Authentification réussie!")
        return True
    else:
        print("Nom d'utilisateur ou code PIN incorrect.")
        return False

def make_deposit():
    """Effectue un dépôt sur un compte client"""
    customer_id = input("Entrez l'ID du client: ")
    customer = get_customer(customer_id)
    
    if not customer:
        print(f"Client avec ID {customer_id} non trouvé.")
        return
    
    if not customer.account:
        print(f"Le client {customer_id} n'a pas de compte associé.")
        return
    
    if not auth_user(customer.account):
        return
    
    amount = get_and_validate_amount()
    customer.account.deposit(amount)

def make_withdraw():
    """Effectue un retrait sur un compte client"""
    customer_id = input("Entrez l'ID du client: ")
    customer = get_customer(customer_id)
    
    if not customer:
        print(f"Client avec ID {customer_id} non trouvé.")
        return
    
    if not customer.account:
        print(f"Le client {customer_id} n'a pas de compte associé.")
        return
    
    if not auth_user(customer.account):
        return
    
    amount = get_and_validate_amount()
    customer.account.withdraw(amount)

def make_payment():
    """Effectue un paiement depuis un compte OM"""
    customer_id = input("Entrez l'ID du client: ")
    customer = get_customer(customer_id)
    
    if not customer:
        print(f"Client avec ID {customer_id} non trouvé.")
        return
    
    if not customer.account:
        print(f"Le client {customer_id} n'a pas de compte associé.")
        return
    
    if not isinstance(customer.account, OrangeMoneyAccount):
        print("Seuls les comptes Orange Money peuvent effectuer des paiements.")
        return
    
    if not auth_user(customer.account):
        return
    
    amount = get_and_validate_amount()
    customer.account.payment(amount)

def make_transfer():
    """Effectue un transfert entre deux comptes"""
    # Compte émetteur
    sender_id = input("Entrez l'ID du client émetteur: ")
    sender = get_customer(sender_id)
    
    if not sender:
        print(f"Client émetteur avec ID {sender_id} non trouvé.")
        return
    
    if not sender.account:
        print(f"Le client émetteur {sender_id} n'a pas de compte associé.")
        return
    
    if not auth_user(sender.account):
        return
    
    # Compte destinataire
    recipient_id = input("Entrez l'ID du client destinataire: ")
    recipient = get_customer(recipient_id)
    
    if not recipient:
        print(f"Client destinataire avec ID {recipient_id} non trouvé.")
        return
    
    if not recipient.account:
        print(f"Le client destinataire {recipient_id} n'a pas de compte associé.")
        return
    
    # Montant et transfert
    amount = get_and_validate_amount()
    sender.account.send(recipient.account, amount)

def show_balance():
    """Affiche le solde d'un compte client"""
    customer_id = input("Entrez l'ID du client: ")
    customer = get_customer(customer_id)
    
    if not customer:
        print(f"Client avec ID {customer_id} non trouvé.")
        return
    
    if not customer.account:
        print(f"Le client {customer_id} n'a pas de compte associé.")
        return
    
    if not auth_user(customer.account):
        return
    
    customer.account.show_balance()

def show_all_accounts():
    """Affiche la liste de tous les comptes"""
    Account.all()

def show_all_customers():
    """Affiche la liste de tous les clients"""
    Customer.all()

def show_all_transactions():
    """Affiche la liste de toutes les transactions"""
    if not Account.account_transactions:
        print("Aucune transaction n'a été effectuée.")
        return
    
    try:
        from prettytable import PrettyTable
        table = PrettyTable()
        table.field_names = ["Type", "Compte", "Montant", "Solde", "Détails"]
        for transaction in Account.account_transactions:
            details = ""
            if transaction["type"] == "ENVOI":
                details = f"Vers: {transaction['recipient']}"
            elif transaction["type"] == "RECEPTION":
                details = f"De: {transaction['sender']}"
            
            table.add_row([
                transaction["type"],
                transaction["account"],
                transaction["amount"],
                transaction["balance"],
                details
            ])
        print(table)
    except ImportError:
        print("\n--- Liste des transactions ---")
        for transaction in Account.account_transactions:
            print(f"Type: {transaction['type']}, Compte: {transaction['account']}, Montant: {transaction['amount']}, Solde: {transaction['balance']}")

def show_main_menu():
    """Affiche le menu principal"""
    print("\n" + "="*50)
    print("Bienvenue dans le système de Kiosk".center(50))
    print("="*50)
    print("1. Create Wave Account")
    print("2. Create OM Account")
    print("3. Manage accounts")
    print("4. Quitter")
    print("="*50)

def show_admin_menu():
    """Affiche le menu administrateur"""
    print("\n" + "="*50)
    print("Menu de gestion des comptes".center(50))
    print("="*50)
    print("1. Make Deposit")
    print("2. Make Withdraw")
    print("3. Make Payment")
    print("4. Make Transfer")
    print("5. Show Balance")
    print("6. Show all customers")
    print("7. Show all transactions")
    print("8. Show all accounts")
    print("9. Back to main menu")
    print("="*50)

def console_mode():
    """Fonction principale du programme en mode console"""
    while True:
        show_main_menu()
        choice = input("Choisissez une option (1-4): ")
        
        if choice == "1":
            create_wave_account()
        elif choice == "2":
            create_om_account()
        elif choice == "3":
            admin_menu()
        elif choice == "4":
            print("Merci d'avoir utilisé notre système. Au revoir!")
            sys.exit(0)
        else:
            print("Option invalide. Veuillez réessayer.")

def admin_menu():
    """Gère le menu administrateur"""
    while True:
        show_admin_menu()
        choice = input("Choisissez une option (1-9): ")
        
        if choice == "1":
            make_deposit()
        elif choice == "2":
            make_withdraw()
        elif choice == "3":
            make_payment()
        elif choice == "4":
            make_transfer()
        elif choice == "5":
            show_balance()
        elif choice == "6":
            show_all_customers()
        elif choice == "7":
            show_all_transactions()
        elif choice == "8":
            show_all_accounts()
        elif choice == "9":
            return
        else:
            print("Option invalide. Veuillez réessayer.")

def run_django_app():
    """Lance l'application Django"""
    print("Démarrage de l'application web Kiosk...")
    
    # Vérifier si les dépendances sont installées
    try:
        import django
        print(f"Django version {django.get_version()} détectée.")
    except ImportError:
        print("Django n'est pas installé. Installation des dépendances...")
        subprocess.call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Lancer le serveur Django
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kiosk_project.settings')
        from django.core.management import execute_from_command_line
        
        # Vérifier si la base de données existe
        if not os.path.exists('db.sqlite3'):
            print("Initialisation de la base de données...")
            execute_from_command_line(['manage.py', 'migrate'])
        
        # Lancer le serveur
        print("Lancement du serveur web sur http://127.0.0.1:8000/")
        print("Appuyez sur CTRL+C pour arrêter le serveur.")
        execute_from_command_line(['manage.py', 'runserver'])
    except Exception as e:
        print(f"Erreur lors du démarrage du serveur Django: {str(e)}")
        sys.exit(1)

def main():
    """Démarre l'application en mode graphique"""
    # Lancer l'interface graphique
    run_app()
    
    # La version console est toujours disponible mais n'est plus exécutée par défaut
    # Pour utiliser la version console, décommentez la ligne suivante et commentez run_app()
    # console_mode()

if __name__ == "__main__":
    run_django_app() 