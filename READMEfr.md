![](https://github.com/zebulon75018/wdialog/blob/master/img/unnamed.png?raw=true)
# Dialog Web Interface

Interface web moderne pour afficher des boîtes de dialogue depuis des scripts bash, compatible avec les spécifications de la commande `dialog`.

## 🎯 Fonctionnalités

- ✅ Compatible avec la syntaxe de la commande `dialog`
- 🎨 Interface web moderne et responsive avec Bootstrap
- 🔌 Communication en temps réel via WebSocket
- 📱 Design moderne et animé
- 🚀 Facile à intégrer dans vos scripts bash existants

## 📋 Types de widgets supportés

- `--yesno` : Boîte de dialogue Oui/Non
- `--msgbox` : Boîte de message
- `--inputbox` : Saisie de texte
- `--passwordbox` : Saisie de mot de passe
- `--textbox` : Affichage de fichier texte
- `--menu` : Menu de sélection
- `--checklist` : Liste à cocher (sélection multiple)
- `--radiolist` : Liste radio (sélection unique)
- `--gauge` : Barre de progression
- `--infobox` : Information temporaire
- `--calendar` : Sélection de date
- `--timebox` : Sélection d'heure
- `--fselect` : **[NOUVEAU]** Sélection de fichier/dossier ( non fonctionnel )
- `--inputmenu` : **[NOUVEAU]** Menu avec capacité de renommage
- `--mixedform` : **[NOUVEAU]** Formulaire avec champs mixtes (texte/password/readonly)
- `--mixedgauge` : **[NOUVEAU]** Barre de progression avec liste de statuts

## 🛠️ Installation

### Prérequis

- Python 3.7+
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner ou créer la structure du projet :**

```bash
mkdir dialog-web
cd dialog-web
```

2. **Installer les dépendances Python :**

```bash
pip install flask flask-socketio python-socketio
```

3. **Créer la structure des dossiers :**

```bash
mkdir templates
```

4. **Placer les fichiers :**

- `dialog_server.py` : Le serveur Flask principal
- `wdialog.py` : Le script client (à rendre exécutable)
- `templates/dialog_interface.html` : Le template HTML
- `example_usage.sh` : Exemple d'utilisation (optionnel)

5. **Rendre wdialog.py exécutable :**

```bash
chmod +x wdialog.py
```

## 🚀 Utilisation

### 1. Démarrer le serveur

Dans un premier terminal :

```bash
python3 dialog_server.py
```

Le serveur démarre sur :
- Interface web : http://localhost:5000
- Socket serveur : localhost:5001

### 2. Ouvrir l'interface web

Ouvrez votre navigateur et allez à : **http://localhost:5000**

Vous verrez l'écran d'attente qui indique que l'interface est prête à recevoir des requêtes.

### 3. Utiliser wdialog.py dans vos scripts bash

Dans un second terminal, vous pouvez maintenant utiliser `wdialog.py` comme vous utiliseriez `dialog` :

```bash
# Exemple simple
python3 wdialog.py --title "Test" --yesno "Voulez-vous continuer ?" 10 50
```

Ou dans un script bash :

```bash
#!/bin/bash

# Définir la commande
WDIALOG="python3 wdialog.py"

# Utiliser comme dialog
$WDIALOG --title "Confirmation" --yesno "Continuer ?" 10 50
if [ $? -eq 0 ]; then
    echo "Oui sélectionné"
else
    echo "Non sélectionné"
fi

# Saisie de texte
nom=$($WDIALOG --title "Nom" --inputbox "Entrez votre nom :" 10 50 2>&1)
echo "Nom : $nom"

# Menu
choix=$($WDIALOG --menu "Menu :" 15 50 3 \
    "1" "Option 1" \
    "2" "Option 2" \
    "3" "Option 3" 2>&1)
echo "Choix : $choix"
```

## 📖 Exemples d'utilisation

### Boîte Yes/No

```bash
python3 wdialog.py --title "Confirmation" --yesno "Voulez-vous continuer ?" 10 50
```

### Boîte de saisie

```bash
nom=$(python3 wdialog.py --title "Saisie" --inputbox "Entrez votre nom :" 10 50 2>&1)
echo "Nom : $nom"
```

### Menu

```bash
choix=$(python3 wdialog.py --title "Menu" --menu "Choisissez :" 15 50 3 \
    "opt1" "Option 1" \
    "opt2" "Option 2" \
    "opt3" "Option 3" 2>&1)
```

### Checklist

```bash
modules=$(python3 wdialog.py --checklist "Modules :" 15 60 3 \
    "apache" "Serveur Apache" on \
    "mysql" "Base de données" off \
    "php" "PHP" on 2>&1)
```

### Barre de progression

```bash
(
    for i in {0..100..10}; do
        echo $i
        sleep 0.2
    done
) | python3 wdialog.py --gauge "Installation..." 10 50 0
```

### Sélection de fichier (NOUVEAU)

```bash
fichier=$(python3 wdialog.py --fselect "/tmp/" 15 60 2>&1)
echo "Fichier sélectionné : $fichier"
```

### Menu avec renommage (NOUVEAU)

```bash
choix=$(python3 wdialog.py --inputmenu "Serveurs :" 15 60 3 \
    "srv1" "Serveur Web" \
    "srv2" "Serveur DB" \
    "srv3" "Cache Redis" 2>&1)
# Retourne soit le tag sélectionné, soit "RENAMED tag nouveau_nom"
```

### Formulaire mixte (NOUVEAU)

```bash
# Format: label y x item y x flen ilen itype
# itype: 0=texte, 1=password, 2=readonly
resultat=$(python3 wdialog.py --mixedform "Configuration :" 18 70 5 \
    "Nom:" 1 1 "John" 1 10 20 30 0 \
    "Pass:" 2 1 "" 2 10 20 30 1 \
    "ID:" 3 1 "12345" 3 10 10 10 2 \
    "Email:" 4 1 "john@example.com" 4 10 30 50 0 \
    "Tel:" 5 1 "+33612345678" 5 10 20 20 0 2>&1)
```

### Gauge avec statuts (NOUVEAU)

```bash
# Statuts: 0=Réussi, -1=Échoué, -2=Ignoré, -3=En cours
python3 wdialog.py --mixedgauge "Installation" 18 60 75 \
    "Téléchargement" "0" \
    "Installation" "-3" \
    "Configuration" "-2" \
    "Tests" "-2" \
    "Finalisation" "-2"
```

## 🎨 Personnalisation

### Options communes supportées

- `--title` : Titre de la boîte de dialogue
- `--backtitle` : Titre de fond
- `--ok-label` : Label du bouton OK
- `--cancel-label` : Label du bouton Annuler
- `--yes-label` : Label du bouton Oui
- `--no-label` : Label du bouton Non
- `--defaultno` : Mettre "Non" par défaut
- `--no-cancel` : Masquer le bouton Annuler
- `--extra-button` : Ajouter un bouton supplémentaire
- `--help-button` : Ajouter un bouton d'aide

### Exemple avec options

```bash
python3 wdialog.py \
    --title "Mon Titre" \
    --backtitle "Application v1.0" \
    --yes-label "Continuer" \
    --no-label "Arrêter" \
    --yesno "Voulez-vous continuer ?" 10 50
```

## 🔧 Configuration avancée

### Changer le port du serveur

Modifier dans `dialog_server.py` :

```python
socketio.run(app, host='0.0.0.0', port=5000, debug=True)
```

### Utiliser un serveur distant

Modifier dans `wdialog.py` l'adresse du serveur :

```python
wd = WDialog(server_host='192.168.1.100', server_port=5001)
```

## 📝 Codes de retour

Comme la commande `dialog` originale :

- `0` : OK / Yes sélectionné
- `1` : Cancel / No sélectionné
- `255` : Erreur ou timeout

## 🐛 Dépannage

### Le serveur ne démarre pas

Vérifiez que les ports 5000 et 5001 ne sont pas déjà utilisés :

```bash
lsof -i :5000
lsof -i :5001
```

### Erreur de connexion

Assurez-vous que :
1. Le serveur Flask est bien démarré
2. L'interface web est ouverte dans le navigateur
3. Le navigateur est connecté (vérifiez l'indicateur de statut en haut à droite)

### Les boutons ne répondent pas

Vérifiez la console JavaScript du navigateur (F12) pour voir les erreurs éventuelles.

## 📄 Structure du projet

```
dialog-web/
├── dialog_server.py          # Serveur Flask + WebSocket
├── wdialog.py               # Client Python (compatible dialog)
├── templates/
│   └── dialog_interface.html # Interface web
├── example_usage.sh          # Exemples d'utilisation
└── README.md                # Ce fichier
```

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Améliorer la documentation



## 🎉 Crédits

- Interface : Bootstrap 5 + jQuery
- Communication temps réel : Socket.IO
- Compatible avec : dialog (Linux)

---

**Bon scripting ! 🚀**
