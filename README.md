# Système POS pour Boutique de Vêtements

Application de point de vente (POS) développée avec Django pour gérer une boutique de vêtements.

## Fonctionnalités

- Gestion de l'inventaire
- Gestion des clients
- Système de caisse
- Gestion des promotions
- Rapports et statistiques

## Installation

1. Cloner le repository :
```bash
git clone https://github.com/dimiloud/boutique-pos-system.git
cd boutique-pos-system
```

2. Créer un environnement virtuel :
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Structure du Projet

```
boutique-pos-system/
├── config/              # Configuration Django
├── inventory/          # Gestion des produits
├── customers/          # Gestion des clients
├── sales/             # Gestion des ventes
├── static/            # Fichiers statiques
└── templates/         # Templates HTML
```

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou un pull request.

## Licence

Ce projet est sous licence MIT.