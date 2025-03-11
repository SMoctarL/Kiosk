# Kiosk - Système de Gestion de Point Multiservice

Une application permettant de gérer des comptes clients WAVE et Orange Money.

## Fonctionnalités

- Création de comptes clients (WAVE et OM)
- Dépôt sur un compte client
- Retrait sur un compte client
- Transfert d'un compte client à un autre
- Paiement (uniquement pour les comptes OM)
- Consultation du solde
- Affichage de la liste des clients
- Affichage de la liste des transactions
- Authentification des comptes pour toutes les transactions

## Installation

1. Clonez ce dépôt sur votre machine locale
2. Créez un environnement virtuel Python (recommandé) :
   ```
   python -m venv venv
   ```
3. Activez l'environnement virtuel :
   - Sous Windows :
     ```
     venv\Scripts\activate
     ```
   - Sous macOS/Linux :
     ```
     source venv/bin/activate
     ```
4. Installez les dépendances requises :
   ```
   pip install -r requirements.txt
   ```

## Utilisation

Pour lancer l'application avec l'interface graphique, exécutez :
```
python main.py
```

## Structure du projet

- `main.py` : Point d'entrée de l'application
- `gui.py` : Interface graphique
- `customer.py` : Définition de la classe Customer
- `account.py` : Définition de la classe Account
- `wave_account.py` : Définition de la classe WaveAccount
- `om_account.py` : Définition de la classe OrangeMoneyAccount

## Contraintes techniques

Les comptes WAVE ont les limites suivantes :
- Limite de retrait : 100 000 CFA
- Limite de transfert : 500 000 CFA

Les comptes Orange Money ont les limites suivantes :
- Limite de retrait : 200 000 CFA
- Limite de transfert : 1 000 000 CFA
- Limite de paiement : 500 000 CFA

## Auteur

 SMoctarL-Ce projet a été développé dans le cadre d'un exercice de programmation orientée objet en Python. 