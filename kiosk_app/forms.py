from django import forms
import re

class CustomerForm(forms.Form):
    cni = forms.CharField(
        label="Numéro CNI", 
        max_length=8, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: AB123456'})
    )
    firstname = forms.CharField(
        label="Prénom", 
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'})
    )
    lastname = forms.CharField(
        label="Nom", 
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'})
    )
    phone = forms.CharField(
        label="Téléphone", 
        max_length=9, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 771234567'})
    )
    address = forms.CharField(
        label="Adresse", 
        max_length=200, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresse'})
    )
    
    def clean_cni(self):
        cni = self.cleaned_data.get('cni')
        if not cni:
            return cni
            
        if len(cni) != 8:
            raise forms.ValidationError("Le numéro CNI doit contenir exactement 8 caractères.")
            
        if not all(c.isalnum() for c in cni):
            raise forms.ValidationError("Le numéro CNI doit contenir uniquement des lettres et des chiffres.")
            
        return cni
    
    def clean_firstname(self):
        firstname = self.cleaned_data.get('firstname')
        if not firstname:
            return firstname
            
        # Permettre les espaces et les caractères spéciaux comme les accents ou les tirets
        if len(firstname) < 2:
            raise forms.ValidationError("Le prénom doit contenir au moins 2 caractères.")
            
        # Vérification moins stricte pour permettre les caractères accentués et les espaces
        if not all(c.isalpha() or c.isspace() or c == '-' or c == "'" for c in firstname):
            raise forms.ValidationError("Le prénom ne doit contenir que des lettres, des espaces, des tirets ou des apostrophes.")
            
        return firstname
    
    def clean_lastname(self):
        lastname = self.cleaned_data.get('lastname')
        if not lastname:
            return lastname
            
        if len(lastname) < 2:
            raise forms.ValidationError("Le nom doit contenir au moins 2 caractères.")
            
        # Vérification moins stricte pour permettre les caractères accentués et les espaces
        if not all(c.isalpha() or c.isspace() or c == '-' or c == "'" for c in lastname):
            raise forms.ValidationError("Le nom ne doit contenir que des lettres, des espaces, des tirets ou des apostrophes.")
            
        return lastname
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            return phone
            
        # Supprimer les espaces éventuels
        phone = phone.replace(' ', '')
        
        if len(phone) != 9:
            raise forms.ValidationError("Le numéro de téléphone doit contenir exactement 9 chiffres.")
            
        if not phone.isdigit():
            raise forms.ValidationError("Le numéro de téléphone doit contenir uniquement des chiffres.")
            
        if not phone.startswith(('70', '76', '77', '78')):
            raise forms.ValidationError("Le numéro de téléphone doit commencer par 70, 76, 77 ou 78.")
            
        return phone
    
    def clean_address(self):
        address = self.cleaned_data.get('address')
        if not address:
            return address
            
        if len(address) < 2:
            raise forms.ValidationError("L'adresse doit contenir au moins 2 caractères.")
            
        # Permettre plus de caractères dans l'adresse (lettres, chiffres, espaces, etc.)
        invalid_chars = set(r'<>{}[]|\\^`~')
        if any(c in invalid_chars for c in address):
            raise forms.ValidationError("L'adresse contient des caractères non autorisés.")
            
        return address

class AccountForm(forms.Form):
    username = forms.CharField(
        label="Nom d'utilisateur", 
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom d'utilisateur"})
    )
    code_pin = forms.CharField(
        label="Code PIN", 
        max_length=4, 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Code PIN (2-4 chiffres)'})
    )
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            return username
            
        if len(username) < 2:
            raise forms.ValidationError("Le nom d'utilisateur doit contenir au moins 2 caractères.")
            
        # Permettre les lettres et éventuellement des chiffres
        if not username.replace(' ', '').isalnum():
            raise forms.ValidationError("Le nom d'utilisateur ne doit contenir que des lettres et des chiffres.")
            
        return username
    
    def clean_code_pin(self):
        code_pin = self.cleaned_data.get('code_pin')
        if not code_pin:
            return code_pin
            
        if not code_pin.isdigit():
            raise forms.ValidationError("Le code PIN doit contenir uniquement des chiffres.")
            
        if not (2 <= len(code_pin) <= 4):
            raise forms.ValidationError("Le code PIN doit contenir entre 2 et 4 chiffres.")
            
        return code_pin

class AuthForm(forms.Form):
    username = forms.CharField(
        label="Nom d'utilisateur", 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom d'utilisateur"})
    )
    code_pin = forms.CharField(
        label="Code PIN", 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Code PIN'})
    )

class AmountForm(forms.Form):
    amount = forms.IntegerField(
        label="Montant", 
        min_value=1, 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Montant'})
    )

class TransferForm(forms.Form):
    recipient_id = forms.CharField(
        label="ID du destinataire", 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "ID du client destinataire"})
    )
    amount = forms.IntegerField(
        label="Montant", 
        min_value=1, 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Montant'})
    ) 