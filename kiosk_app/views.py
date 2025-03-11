from django.shortcuts import render, redirect
from django.contrib import messages
import os
import sys

# Import des formulaires
from .forms import CustomerForm, AccountForm, AuthForm, AmountForm, TransferForm

# Import des classes avec gestion d'erreur
try:
    from customer import Customer
    from account import Account
    from wave_account import WaveAccount
    from om_account import OrangeMoneyAccount
except ImportError as e:
    print(f"Erreur d'importation: {e}")

def home(request):
    """Page d'accueil"""
    return render(request, 'home.html')

def create_wave_account(request):
    """Création d'un compte WAVE"""
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)
        account_form = AccountForm(request.POST)
        
        if customer_form.is_valid() and account_form.is_valid():
            try:
                # Récupération des données du formulaire client
                cni = customer_form.cleaned_data['cni']
                firstname = customer_form.cleaned_data['firstname']
                lastname = customer_form.cleaned_data['lastname']
                phone = customer_form.cleaned_data['phone']
                address = customer_form.cleaned_data['address']
                
                # Récupération des données du formulaire compte
                username = account_form.cleaned_data['username']
                code_pin = account_form.cleaned_data['code_pin']
                
                # Création du client
                customer = Customer(cni, firstname, lastname, phone, address)
                
                # Création du compte WAVE
                account = WaveAccount(customer, username, code_pin)
                
                # Association du compte au client
                customer.account = account
                
                messages.success(request, f"Compte WAVE créé avec succès pour {firstname} {lastname}")
                return redirect('home')
            except Exception as e:
                messages.error(request, f"Erreur lors de la création du compte: {str(e)}")
    else:
        customer_form = CustomerForm()
        account_form = AccountForm()
    
    return render(request, 'create_account.html', {
        'customer_form': customer_form,
        'account_form': account_form,
        'account_type': 'WAVE'
    })

def create_om_account(request):
    """Création d'un compte Orange Money"""
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)
        account_form = AccountForm(request.POST)
        
        if customer_form.is_valid() and account_form.is_valid():
            try:
                # Récupération des données
                cni = customer_form.cleaned_data['cni']
                firstname = customer_form.cleaned_data['firstname']
                lastname = customer_form.cleaned_data['lastname']
                phone = customer_form.cleaned_data['phone']
                address = customer_form.cleaned_data['address']
                
                username = account_form.cleaned_data['username']
                code_pin = account_form.cleaned_data['code_pin']
                
                # Création du client et du compte
                customer = Customer(cni, firstname, lastname, phone, address)
                account = OrangeMoneyAccount(customer, username, code_pin)
                customer.account = account
                
                messages.success(request, f"Compte Orange Money créé avec succès pour {firstname} {lastname}")
                return redirect('home')
            except Exception as e:
                messages.error(request, f"Erreur lors de la création du compte: {str(e)}")
    else:
        customer_form = CustomerForm()
        account_form = AccountForm()
    
    return render(request, 'create_account.html', {
        'customer_form': customer_form,
        'account_form': account_form,
        'account_type': 'OM'
    })

def customers_list(request):
    """Vue pour afficher la liste des clients"""
    try:
        customers = getattr(Customer, 'customer_list', [])
        return render(request, 'customers_list.html', {'customers': customers})
    except Exception as e:
        messages.error(request, f"Erreur lors de l'affichage des clients: {str(e)}")
        print(f"Erreur détaillée dans customers_list: {str(e)}")
        return render(request, 'customers_list.html', {'customers': []})

def accounts_list(request):
    """Vue pour afficher la liste des comptes"""
    try:
        accounts = getattr(Account, 'accounts', [])
        return render(request, 'accounts_list.html', {'accounts': accounts})
    except Exception as e:
        messages.error(request, f"Erreur lors de l'affichage des comptes: {str(e)}")
        print(f"Erreur détaillée dans accounts_list: {str(e)}")
        return render(request, 'accounts_list.html', {'accounts': []})

def transactions_list(request):
    """Vue pour afficher la liste des transactions"""
    try:
        transactions = getattr(Account, 'account_transactions', [])
        return render(request, 'transactions_list.html', {'transactions': transactions})
    except Exception as e:
        messages.error(request, f"Erreur lors de l'affichage des transactions: {str(e)}")
        print(f"Erreur détaillée dans transactions_list: {str(e)}")
        return render(request, 'transactions_list.html', {'transactions': []})

def get_customer(customer_id):
    """Utilitaire pour récupérer un client par son ID"""
    try:
        customer_list = getattr(Customer, 'customer_list', [])
        for customer in customer_list:
            if customer.id == customer_id:
                return customer
        return None
    except Exception as e:
        print(f"Erreur détaillée dans get_customer: {str(e)}")
        return None

def show_balance(request, customer_id):
    """Affichage du solde d'un compte"""
    try:
        customer = get_customer(customer_id)
        if not customer or not customer.account:
            messages.error(request, "Client ou compte introuvable")
            return redirect('customers_list')
        
        if request.method == 'POST':
            auth_form = AuthForm(request.POST)
            if auth_form.is_valid():
                username = auth_form.cleaned_data['username']
                code_pin = auth_form.cleaned_data['code_pin']
                
                # Vérification des identifiants
                if username == customer.account.username and code_pin == customer.account.code_pin:
                    # Appel explicite à la méthode show_balance pour s'assurer qu'elle fonctionne
                    balance = customer.account.balance
                    return render(request, 'balance_result.html', {'customer': customer, 'balance': balance})
                else:
                    messages.error(request, "Identifiants incorrects")
        else:
            auth_form = AuthForm()
        
        return render(request, 'balance_form.html', {'customer': customer, 'auth_form': auth_form})
    except Exception as e:
        messages.error(request, f"Erreur lors de la consultation du solde: {str(e)}")
        print(f"Erreur détaillée dans show_balance: {str(e)}")
        return redirect('customers_list')

def make_deposit(request, customer_id):
    """Effectuer un dépôt"""
    customer = get_customer(customer_id)
    if not customer or not customer.account:
        messages.error(request, "Client ou compte introuvable")
        return redirect('customers_list')
    
    if request.method == 'POST':
        auth_form = AuthForm(request.POST)
        amount_form = AmountForm(request.POST)
        
        if auth_form.is_valid() and amount_form.is_valid():
            username = auth_form.cleaned_data['username']
            code_pin = auth_form.cleaned_data['code_pin']
            amount = amount_form.cleaned_data['amount']
            
            # Vérification des identifiants
            if username == customer.account.username and code_pin == customer.account.code_pin:
                try:
                    # Conversion explicite du montant en entier
                    amount = int(amount)
                    customer.account.deposit(amount)
                    messages.success(request, f"Dépôt de {amount} CFA effectué avec succès")
                    return redirect('customers_list')
                except Exception as e:
                    messages.error(request, f"Erreur lors du dépôt: {str(e)}")
                    print(f"Erreur détaillée dans make_deposit: {str(e)}")
            else:
                messages.error(request, "Identifiants incorrects")
    else:
        auth_form = AuthForm()
        amount_form = AmountForm()
    
    return render(request, 'operation_form.html', {
        'customer': customer, 
        'auth_form': auth_form, 
        'amount_form': amount_form,
        'operation': 'deposit',
        'operation_title': 'Dépôt'
    })

def make_withdraw(request, customer_id):
    """Effectuer un retrait"""
    customer = get_customer(customer_id)
    if not customer or not customer.account:
        messages.error(request, "Client ou compte introuvable")
        return redirect('customers_list')
    
    if request.method == 'POST':
        auth_form = AuthForm(request.POST)
        amount_form = AmountForm(request.POST)
        
        if auth_form.is_valid() and amount_form.is_valid():
            username = auth_form.cleaned_data['username']
            code_pin = auth_form.cleaned_data['code_pin']
            amount = amount_form.cleaned_data['amount']
            
            # Vérification des identifiants
            if username == customer.account.username and code_pin == customer.account.code_pin:
                try:
                    # Conversion explicite du montant en entier
                    amount = int(amount)
                    customer.account.withdraw(amount)
                    messages.success(request, f"Retrait de {amount} CFA effectué avec succès")
                    return redirect('customers_list')
                except Exception as e:
                    messages.error(request, f"Erreur lors du retrait: {str(e)}")
                    print(f"Erreur détaillée dans make_withdraw: {str(e)}")
            else:
                messages.error(request, "Identifiants incorrects")
    else:
        auth_form = AuthForm()
        amount_form = AmountForm()
    
    # Récupération de la limite de retrait
    withdraw_limit = getattr(customer.account, 'withdraw_limit', 'Non définie')
    
    return render(request, 'operation_form.html', {
        'customer': customer, 
        'auth_form': auth_form, 
        'amount_form': amount_form,
        'operation': 'withdraw',
        'operation_title': 'Retrait',
        'limit': withdraw_limit
    })

def make_transfer(request, customer_id):
    """Effectuer un transfert"""
    customer = get_customer(customer_id)
    if not customer or not customer.account:
        messages.error(request, "Client ou compte introuvable")
        return redirect('customers_list')
    
    if request.method == 'POST':
        auth_form = AuthForm(request.POST)
        transfer_form = TransferForm(request.POST)
        
        if auth_form.is_valid() and transfer_form.is_valid():
            username = auth_form.cleaned_data['username']
            code_pin = auth_form.cleaned_data['code_pin']
            recipient_id = transfer_form.cleaned_data['recipient_id']
            amount = transfer_form.cleaned_data['amount']
            
            # Vérification des identifiants
            if username == customer.account.username and code_pin == customer.account.code_pin:
                # Recherche du destinataire
                recipient = get_customer(recipient_id)
                if recipient and recipient.account:
                    try:
                        # Conversion explicite du montant en entier
                        amount = int(amount)
                        customer.account.send(recipient.account, amount)
                        messages.success(request, f"Transfert de {amount} CFA effectué avec succès vers {recipient.firstname} {recipient.lastname}")
                        return redirect('customers_list')
                    except Exception as e:
                        messages.error(request, f"Erreur lors du transfert: {str(e)}")
                        print(f"Erreur détaillée dans make_transfer: {str(e)}")
                else:
                    messages.error(request, "Destinataire introuvable ou sans compte")
            else:
                messages.error(request, "Identifiants incorrects")
    else:
        auth_form = AuthForm()
        transfer_form = TransferForm()
    
    # Récupération de la limite de transfert
    transfer_limit = getattr(customer.account, 'transfer_limit', 'Non définie')
    
    return render(request, 'transfer_form.html', {
        'customer': customer, 
        'auth_form': auth_form, 
        'transfer_form': transfer_form,
        'limit': transfer_limit
    })

def make_payment(request, customer_id):
    """Effectuer un paiement (uniquement pour Orange Money)"""
    customer = get_customer(customer_id)
    if not customer or not customer.account or not hasattr(customer.account, 'payment'):
        messages.error(request, "Client ou compte introuvable ou non compatible avec les paiements")
        return redirect('customers_list')
    
    if request.method == 'POST':
        auth_form = AuthForm(request.POST)
        amount_form = AmountForm(request.POST)
        
        if auth_form.is_valid() and amount_form.is_valid():
            username = auth_form.cleaned_data['username']
            code_pin = auth_form.cleaned_data['code_pin']
            amount = amount_form.cleaned_data['amount']
            
            # Vérification des identifiants
            if username == customer.account.username and code_pin == customer.account.code_pin:
                try:
                    # Conversion explicite du montant en entier
                    amount = int(amount)
                    customer.account.payment(amount)
                    messages.success(request, f"Paiement de {amount} CFA effectué avec succès")
                    return redirect('customers_list')
                except Exception as e:
                    messages.error(request, f"Erreur lors du paiement: {str(e)}")
                    print(f"Erreur détaillée dans make_payment: {str(e)}")
            else:
                messages.error(request, "Identifiants incorrects")
    else:
        auth_form = AuthForm()
        amount_form = AmountForm()
    
    # Récupération de la limite de paiement
    payment_limit = getattr(customer.account, 'payment_limit', 'Non définie')
    
    return render(request, 'operation_form.html', {
        'customer': customer, 
        'auth_form': auth_form, 
        'amount_form': amount_form,
        'operation': 'payment',
        'operation_title': 'Paiement',
        'limit': payment_limit
    }) 