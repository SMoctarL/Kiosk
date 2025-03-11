import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style
from PIL import Image, ImageTk
import sys
import re

from customer import Customer
from account import Account
from wave_account import WaveAccount
from om_account import OrangeMoneyAccount

class MetallicStyle(ttk.Style):
    """Style personnalisé pour un thème métallique noir et blanc"""
    def __init__(self):
        super().__init__(theme="superhero")
        
        self.configure('.', font=('Roboto', 10))
        self.configure('TFrame', background='#2d2d2d')
        self.configure('TLabel', background='#2d2d2d', foreground='white')
        self.configure('Header.TLabel', font=('Roboto', 16, 'bold'), foreground='#c0c0c0')
        self.configure('Title.TLabel', font=('Roboto', 24, 'bold'), foreground='white')
        self.configure('Accent.TButton', background='#4a4a4a', foreground='white')
        self.configure('TEntry', fieldbackground='#3d3d3d', foreground='white')
        self.configure('TNotebook', background='#2d2d2d')
        self.configure('TNotebook.Tab', background='#3d3d3d', foreground='white')
        self.configure('Treeview', background='#3d3d3d', foreground='white', fieldbackground='#3d3d3d')
        self.configure('Treeview.Heading', background='#444444', foreground='white')

class InputDialog(tk.Toplevel):
    """Boîte de dialogue personnalisée pour les entrées"""
    def __init__(self, parent, title, prompt, validator=None, show=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x150")
        self.resizable(False, False)
        self.configure(background='#2d2d2d')
        self.result = None
        self.validator = validator
        
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Label
        ttk.Label(main_frame, text=prompt).pack(anchor=tk.W, pady=(0, 10))
        
        # Champ de saisie
        self.entry = ttk.Entry(main_frame, width=30, show=show)
        self.entry.pack(fill=tk.X, pady=(0, 20))
        self.entry.focus_set()
        
        # Boutons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="Annuler", command=self.cancel).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="OK", style="Accent.TButton", command=self.validate).pack(side=tk.RIGHT)
        
        # Binding
        self.bind("<Return>", lambda event: self.validate())
        self.bind("<Escape>", lambda event: self.cancel())
        
        # Modal
        self.transient(parent)
        self.grab_set()
        self.wait_window(self)
    
    def validate(self):
        value = self.entry.get()
        if self.validator and not self.validator(value):
            return
        self.result = value
        self.destroy()
    
    def cancel(self):
        self.result = None
        self.destroy()

class KioskApp(tk.Tk):
    """Application principale Kiosk avec interface graphique"""
    def __init__(self):
        super().__init__()
        
        # Configuration de la fenêtre
        self.title("Kiosk - Système de Gestion")
        self.geometry("1000x700")
        self.style = MetallicStyle()
        
        # Variables
        self.current_customer = None
        self.current_account = None
        
        # Création de l'interface
        self.create_widgets()
        self.center_window()
        
    def center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_widgets(self):
        """Création des widgets de l'interface"""
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # En-tête
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, padx=20, pady=20)
        
        ttk.Label(header_frame, text="KIOSK", style="Title.TLabel").pack(side=tk.LEFT)
        ttk.Label(header_frame, text="Système de Gestion Multiservice", style="Header.TLabel").pack(side=tk.LEFT, padx=20)
        
        # Séparateur
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=20)
        
        # Contenu
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Notebook (onglets)
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Onglet 1: Accueil / Création de compte
        self.create_home_tab()
        
        # Onglet 2: Gestion des comptes
        self.create_account_management_tab()
        
        # Onglet 3: Transactions
        self.create_transactions_tab()
        
        # Onglet 4: Informations
        self.create_info_tab()
        
        # Barre d'état
        status_frame = ttk.Frame(main_frame, style="TFrame")
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        self.status_label = ttk.Label(status_frame, text="Prêt")
        self.status_label.pack(side=tk.LEFT)
        
        # Pied de page
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill=tk.X, padx=20, pady=10)
        ttk.Button(footer_frame, text="Quitter", command=self.quit_app).pack(side=tk.RIGHT)
        
    def create_home_tab(self):
        """Création de l'onglet d'accueil"""
        home_frame = ttk.Frame(self.notebook)
        self.notebook.add(home_frame, text="Accueil")
        
        # Sous-titres
        ttk.Label(home_frame, text="Création de Comptes", style="Header.TLabel").pack(anchor=tk.W, pady=(20, 10))
        ttk.Separator(home_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # Boutons d'action
        buttons_frame = ttk.Frame(home_frame)
        buttons_frame.pack(fill=tk.X, pady=20)
        
        # Carte Wave
        wave_frame = ttk.LabelFrame(buttons_frame, text="Compte WAVE")
        wave_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(wave_frame, text="Créez un compte Wave pour profiter des services suivants:").pack(anchor=tk.W, pady=5)
        ttk.Label(wave_frame, text="• Dépôt jusqu'à 1 000 000 CFA").pack(anchor=tk.W, pady=2)
        ttk.Label(wave_frame, text="• Retrait limité à 100 000 CFA").pack(anchor=tk.W, pady=2)
        ttk.Label(wave_frame, text="• Transfert limité à 500 000 CFA").pack(anchor=tk.W, pady=2)
        
        ttk.Button(wave_frame, text="Créer un compte WAVE", style="success.TButton", 
                 command=self.create_wave_account).pack(anchor=tk.CENTER, pady=20)
        
        # Carte Orange Money
        om_frame = ttk.LabelFrame(buttons_frame, text="Compte ORANGE MONEY")
        om_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(om_frame, text="Créez un compte Orange Money pour profiter des services suivants:").pack(anchor=tk.W, pady=5)
        ttk.Label(om_frame, text="• Dépôt jusqu'à 1 000 000 CFA").pack(anchor=tk.W, pady=2)
        ttk.Label(om_frame, text="• Retrait limité à 200 000 CFA").pack(anchor=tk.W, pady=2)
        ttk.Label(om_frame, text="• Transfert limité à 1 000 000 CFA").pack(anchor=tk.W, pady=2)
        ttk.Label(om_frame, text="• Paiement limité à 500 000 CFA").pack(anchor=tk.W, pady=2)
        
        ttk.Button(om_frame, text="Créer un compte OM", style="success.TButton", 
                 command=self.create_om_account).pack(anchor=tk.CENTER, pady=20)
        
    def create_account_management_tab(self):
        """Création de l'onglet de gestion des comptes"""
        account_frame = ttk.Frame(self.notebook)
        self.notebook.add(account_frame, text="Gestion des Comptes")
        
        # Sous-titres
        ttk.Label(account_frame, text="Liste des clients", style="Header.TLabel").pack(anchor=tk.W, pady=(20, 10))
        ttk.Separator(account_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # Tableau des clients
        table_frame = ttk.Frame(account_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Treeview pour les clients
        columns = ("ID", "CNI", "Nom", "Prénom", "Téléphone", "Adresse", "Compte")
        self.customers_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.customers_tree.heading(col, text=col)
            self.customers_tree.column(col, width=100)
        
        self.customers_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.customers_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.customers_tree.configure(yscrollcommand=scrollbar.set)
        
        # Boutons d'action
        btn_frame = ttk.Frame(account_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Rafraîchir", command=self.refresh_customers).pack(side=tk.LEFT, padx=5)
        ttk.Label(btn_frame, text="Actions sur le compte sélectionné:").pack(side=tk.LEFT, padx=20)
        
        ttk.Button(btn_frame, text="Dépôt", style="info.TButton", 
                 command=self.make_deposit).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Retrait", style="info.TButton", 
                 command=self.make_withdraw).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Transfert", style="info.TButton", 
                 command=self.make_transfer).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Paiement", style="info.TButton", 
                 command=self.make_payment).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Solde", style="info.TButton", 
                 command=self.show_balance).pack(side=tk.LEFT, padx=5)
        
    def create_transactions_tab(self):
        """Création de l'onglet des transactions"""
        transactions_frame = ttk.Frame(self.notebook)
        self.notebook.add(transactions_frame, text="Transactions")
        
        # Sous-titres
        ttk.Label(transactions_frame, text="Historique des transactions", style="Header.TLabel").pack(anchor=tk.W, pady=(20, 10))
        ttk.Separator(transactions_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # Tableau des transactions
        table_frame = ttk.Frame(transactions_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Treeview pour les transactions
        columns = ("Type", "Compte", "Montant", "Solde", "Détails")
        self.transactions_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.transactions_tree.heading(col, text=col)
            self.transactions_tree.column(col, width=100)
        
        self.transactions_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.transactions_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.transactions_tree.configure(yscrollcommand=scrollbar.set)
        
        # Bouton rafraîchir
        ttk.Button(transactions_frame, text="Rafraîchir", 
                 command=self.refresh_transactions).pack(anchor=tk.W, pady=10)
        
    def create_info_tab(self):
        """Création de l'onglet d'informations"""
        info_frame = ttk.Frame(self.notebook)
        self.notebook.add(info_frame, text="Informations")
        
        # Sous-titres
        ttk.Label(info_frame, text="Liste des comptes", style="Header.TLabel").pack(anchor=tk.W, pady=(20, 10))
        ttk.Separator(info_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # Tableau des comptes
        table_frame = ttk.Frame(info_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Treeview pour les comptes
        columns = ("Numéro", "Type", "Client", "Solde")
        self.accounts_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.accounts_tree.heading(col, text=col)
            self.accounts_tree.column(col, width=150)
        
        self.accounts_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.accounts_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.accounts_tree.configure(yscrollcommand=scrollbar.set)
        
        # Bouton rafraîchir
        ttk.Button(info_frame, text="Rafraîchir", 
                 command=self.refresh_accounts).pack(anchor=tk.W, pady=10)
    
    # Fonctions pour la création de comptes
    def create_wave_account(self):
        try:
            customer_data = self.get_customer_data()
            if not customer_data:
                return
                
            customer = Customer(
                customer_data["cni"],
                customer_data["firstname"],
                customer_data["lastname"],
                customer_data["phone"],
                customer_data["address"]
            )
            
            username = self.get_valid_input("Nom d'utilisateur", "Entrez le nom d'utilisateur:", 
                                          lambda x: len(x) >= 2 and x.isalpha())
            if not username:
                return
                
            code_pin = self.get_valid_input("Code PIN", "Entrez le code PIN (2-4 chiffres):", 
                                          lambda x: x.isdigit() and 2 <= len(x) <= 4, show="*")
            if not code_pin:
                return
            
            account = WaveAccount(customer, username, code_pin)
            messagebox.showinfo("Succès", f"Compte WAVE créé avec succès!\nNuméro: {account.account_number}")
            
            self.refresh_customers()
            self.refresh_accounts()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la création du compte: {str(e)}")
    
    def create_om_account(self):
        try:
            customer_data = self.get_customer_data()
            if not customer_data:
                return
                
            customer = Customer(
                customer_data["cni"],
                customer_data["firstname"],
                customer_data["lastname"],
                customer_data["phone"],
                customer_data["address"]
            )
            
            username = self.get_valid_input("Nom d'utilisateur", "Entrez le nom d'utilisateur:", 
                                          lambda x: len(x) >= 2 and x.isalpha())
            if not username:
                return
                
            code_pin = self.get_valid_input("Code PIN", "Entrez le code PIN (2-4 chiffres):", 
                                          lambda x: x.isdigit() and 2 <= len(x) <= 4, show="*")
            if not code_pin:
                return
            
            account = OrangeMoneyAccount(customer, username, code_pin)
            messagebox.showinfo("Succès", f"Compte Orange Money créé avec succès!\nNuméro: {account.account_number}")
            
            self.refresh_customers()
            self.refresh_accounts()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la création du compte: {str(e)}")
    
    # Fonctions utilitaires
    def get_customer_data(self):
        """Récupère les données du client à partir de formulaires de saisie"""
        # CNI
        cni = self.get_valid_input("Numéro CNI", "Entrez le numéro CNI (8 caractères):", 
                                 lambda x: len(x) == 8 and x.isalnum())
        if not cni:
            return None
            
        # Nom
        lastname = self.get_valid_input("Nom", "Entrez le nom:", 
                                      lambda x: len(x) >= 2 and x.isalpha())
        if not lastname:
            return None
            
        # Prénom
        firstname = self.get_valid_input("Prénom", "Entrez le prénom:", 
                                       lambda x: len(x) >= 2 and x.isalpha())
        if not firstname:
            return None
            
        # Téléphone
        phone = self.get_valid_input("Téléphone", "Entrez le numéro de téléphone (9 chiffres):", 
                                   lambda x: len(x) == 9 and x.isdigit() and x.startswith(('70', '76', '77', '78')))
        if not phone:
            return None
            
        # Adresse
        address = self.get_valid_input("Adresse", "Entrez l'adresse:", 
                                     lambda x: len(x) >= 2 and all(c.isalpha() or c.isspace() for c in x))
        if not address:
            return None
            
        return {
            "cni": cni,
            "lastname": lastname,
            "firstname": firstname,
            "phone": phone,
            "address": address
        }
    
    def get_valid_input(self, title, prompt, validator=None, show=None):
        """Affiche une boîte de dialogue pour demander une entrée valide"""
        dialog = InputDialog(self, title, prompt, validator, show)
        return dialog.result
    
    def get_selected_customer(self):
        """Récupère le client sélectionné dans la liste"""
        selected_items = self.customers_tree.selection()
        if not selected_items:
            messagebox.showwarning("Sélection requise", "Veuillez sélectionner un client dans la liste.")
            return None
            
        customer_id = self.customers_tree.item(selected_items[0], "values")[0]
        customer = None
        
        for c in Customer.customer_list:
            if c.id == customer_id:
                customer = c
                break
                
        if not customer:
            messagebox.showerror("Erreur", f"Client avec ID {customer_id} non trouvé.")
            return None
            
        if not customer.account:
            messagebox.showerror("Erreur", f"Le client {customer_id} n'a pas de compte associé.")
            return None
            
        return customer
    
    def auth_account(self, account):
        """Authentifie un compte utilisateur"""
        username = self.get_valid_input("Authentification", "Entrez votre nom d'utilisateur:")
        if username is None:
            return False
            
        code_pin = self.get_valid_input("Authentification", "Entrez votre code PIN:", show="*")
        if code_pin is None:
            return False
            
        if username == account.username and code_pin == account.code_pin:
            return True
        else:
            messagebox.showerror("Erreur d'authentification", "Nom d'utilisateur ou code PIN incorrect.")
            return False
    
    # Fonctions pour les opérations sur les comptes
    def make_deposit(self):
        """Effectue un dépôt sur un compte client"""
        customer = self.get_selected_customer()
        if not customer:
            return
            
        if not self.auth_account(customer.account):
            return
            
        amount_str = self.get_valid_input("Dépôt", "Entrez le montant à déposer:", 
                                        lambda x: x.isdigit() and int(x) > 0)
        if not amount_str:
            return
            
        amount = int(amount_str)
        customer.account.deposit(amount)
        messagebox.showinfo("Succès", f"Dépôt de {amount} CFA effectué avec succès.\nNouveau solde: {customer.account.balance} CFA")
        
        self.refresh_accounts()
        self.refresh_transactions()
    
    def make_withdraw(self):
        """Effectue un retrait sur un compte client"""
        customer = self.get_selected_customer()
        if not customer:
            return
            
        if not self.auth_account(customer.account):
            return
            
        amount_str = self.get_valid_input("Retrait", "Entrez le montant à retirer:", 
                                        lambda x: x.isdigit() and int(x) > 0)
        if not amount_str:
            return
            
        amount = int(amount_str)
        result = customer.account.withdraw(amount)
        
        if result:
            messagebox.showinfo("Succès", f"Retrait de {amount} CFA effectué avec succès.\nNouveau solde: {customer.account.balance} CFA")
        
        self.refresh_accounts()
        self.refresh_transactions()
    
    def make_transfer(self):
        """Effectue un transfert entre deux comptes"""
        # Compte émetteur
        sender = self.get_selected_customer()
        if not sender:
            return
            
        if not self.auth_account(sender.account):
            return
            
        # Compte destinataire
        recipient_id = self.get_valid_input("Transfert", "Entrez l'ID du client destinataire:")
        if not recipient_id:
            return
            
        recipient = None
        for c in Customer.customer_list:
            if c.id == recipient_id:
                recipient = c
                break
                
        if not recipient:
            messagebox.showerror("Erreur", f"Client destinataire avec ID {recipient_id} non trouvé.")
            return
            
        if not recipient.account:
            messagebox.showerror("Erreur", f"Le client destinataire {recipient_id} n'a pas de compte associé.")
            return
            
        # Montant et transfert
        amount_str = self.get_valid_input("Transfert", "Entrez le montant à transférer:", 
                                        lambda x: x.isdigit() and int(x) > 0)
        if not amount_str:
            return
            
        amount = int(amount_str)
        result = sender.account.send(recipient.account, amount)
        
        if result:
            messagebox.showinfo("Succès", f"Transfert de {amount} CFA effectué avec succès vers {recipient.account.account_number}.\nNouveau solde: {sender.account.balance} CFA")
        
        self.refresh_accounts()
        self.refresh_transactions()
    
    def make_payment(self):
        """Effectue un paiement depuis un compte OM"""
        customer = self.get_selected_customer()
        if not customer:
            return
            
        if not isinstance(customer.account, OrangeMoneyAccount):
            messagebox.showerror("Erreur", "Seuls les comptes Orange Money peuvent effectuer des paiements.")
            return
            
        if not self.auth_account(customer.account):
            return
            
        amount_str = self.get_valid_input("Paiement", "Entrez le montant à payer:", 
                                        lambda x: x.isdigit() and int(x) > 0)
        if not amount_str:
            return
            
        amount = int(amount_str)
        result = customer.account.payment(amount)
        
        if result:
            messagebox.showinfo("Succès", f"Paiement de {amount} CFA effectué avec succès.\nNouveau solde: {customer.account.balance} CFA")
        
        self.refresh_accounts()
        self.refresh_transactions()
    
    def show_balance(self):
        """Affiche le solde d'un compte client"""
        customer = self.get_selected_customer()
        if not customer:
            return
            
        if not self.auth_account(customer.account):
            return
            
        balance = customer.account.show_balance()
        messagebox.showinfo("Solde", f"Solde du compte {customer.account.account_number}: {balance} CFA")
    
    # Fonctions pour rafraîchir les données affichées
    def refresh_customers(self):
        """Rafraîchit la liste des clients"""
        # Effacer les données existantes
        for item in self.customers_tree.get_children():
            self.customers_tree.delete(item)
            
        # Ajouter les données mises à jour
        for customer in Customer.customer_list:
            account_number = customer.account.account_number if customer.account else "Aucun"
            self.customers_tree.insert("", "end", values=(
                customer.id,
                customer.cni,
                customer.lastname,
                customer.firstname,
                customer.phone,
                customer.address,
                account_number
            ))
    
    def refresh_accounts(self):
        """Rafraîchit la liste des comptes"""
        # Effacer les données existantes
        for item in self.accounts_tree.get_children():
            self.accounts_tree.delete(item)
            
        # Ajouter les données mises à jour
        for account in Account.accounts:
            self.accounts_tree.insert("", "end", values=(
                account.account_number,
                getattr(account, "TYPE", "Standard"),
                f"{account.customer.firstname} {account.customer.lastname}",
                f"{account.balance} {Account.CURRENCY}"
            ))
    
    def refresh_transactions(self):
        """Rafraîchit la liste des transactions"""
        # Effacer les données existantes
        for item in self.transactions_tree.get_children():
            self.transactions_tree.delete(item)
            
        # Ajouter les données mises à jour
        for transaction in Account.account_transactions:
            details = ""
            if transaction["type"] == "ENVOI":
                details = f"Vers: {transaction['recipient']}"
            elif transaction["type"] == "RECEPTION":
                details = f"De: {transaction['sender']}"
                
            self.transactions_tree.insert("", "end", values=(
                transaction["type"],
                transaction["account"],
                transaction["amount"],
                transaction["balance"],
                details
            ))
    
    def quit_app(self):
        """Quitte l'application"""
        if messagebox.askyesno("Quitter", "Êtes-vous sûr de vouloir quitter?"):
            self.destroy()
            sys.exit(0)

def run_app():
    app = KioskApp()
    app.mainloop()

if __name__ == "__main__":
    run_app() 