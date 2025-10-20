#!/bin/bash
# Exemples d'utilisation des nouveaux widgets
# fselect, inputmenu, mixedform, mixedgauge

WDIALOG="python3 wdialog.py"

echo "=== Démonstration des nouveaux widgets ==="
echo ""

# 1. FSelect - Sélection de fichier
echo "1. Test de --fselect (sélection de fichier)"
fichier=$($WDIALOG --title "Sélection de fichier" \
    --fselect "/tmp/" 15 60 2>&1)
response=$?

if [ $response -eq 0 ]; then
    echo "Fichier sélectionné : $fichier"
else
    echo "Sélection annulée"
fi

echo ""
sleep 1

# 2. InputMenu - Menu avec possibilité de renommer
echo "2. Test de --inputmenu (menu avec rename)"
choix=$($WDIALOG --title "Gestion des serveurs" \
    --inputmenu "Sélectionnez un serveur (vous pouvez le renommer) :" 15 60 5 \
    "srv1" "Serveur Web Principal" \
    "srv2" "Serveur Base de Données" \
    "srv3" "Serveur Cache Redis" \
    "srv4" "Serveur Backup" \
    "srv5" "Serveur Load Balancer" 2>&1)
response=$?

if [ $response -eq 0 ]; then
    echo "Résultat : $choix"
    if [[ $choix == RENAMED* ]]; then
        echo "Un serveur a été renommé !"
    else
        echo "Serveur sélectionné : $choix"
    fi
else
    echo "Sélection annulée"
fi

echo ""
sleep 1

# 3. MixedForm - Formulaire avec différents types de champs
echo "3. Test de --mixedform (formulaire mixte)"
# Format: label y x item y x flen ilen itype
# itype: 0=normal, 1=password, 2=readonly
resultat=$($WDIALOG --title "Configuration utilisateur" \
    --mixedform "Entrez les informations utilisateur :" 20 70 8 \
    "Nom d'utilisateur:" 1 1 "john_doe" 1 25 20 30 0 \
    "Email:" 2 1 "john@example.com" 2 25 30 50 0 \
    "Mot de passe:" 3 1 "" 3 25 20 30 1 \
    "Confirmer MdP:" 4 1 "" 4 25 20 30 1 \
    "ID (readonly):" 5 1 "12345" 5 25 10 10 2 \
    "Téléphone:" 6 1 "+33 6 12 34 56 78" 6 25 20 20 0 \
    "Département:" 7 1 "IT" 7 25 15 15 0 \
    "Date création:" 8 1 "2025-01-15" 8 25 15 15 2 2>&1)
response=$?

if [ $response -eq 0 ]; then
    echo "Données du formulaire :"
    echo "$resultat"
else
    echo "Formulaire annulé"
fi

echo ""
sleep 1

# 4. MixedGauge - Gauge avec liste d'items et statuts
echo "4. Test de --mixedgauge (gauge avec statuts)"
$WDIALOG --title "Installation du système" \
    --mixedgauge "Installation en cours..." 20 60 75 \
    "Vérification" "0" \
    "Téléchargement" "0" \
    "Installation" "-3" \
    "Configuration" "-2" \
    "Tests" "-2" \
    "Finalisation" "-2"

echo "Installation affichée (se ferme automatiquement)"
echo ""
sleep 1

# 5. Exemple combiné : Workflow complet
echo "5. Workflow complet avec plusieurs widgets"
echo ""

# Étape 1 : Sélectionner un projet
projet=$($WDIALOG --title "Nouveau projet" \
    --inputmenu "Sélectionnez un projet ou créez-en un :" 15 60 3 \
    "web" "Application Web" \
    "mobile" "Application Mobile" \
    "desktop" "Application Desktop" 2>&1)

if [ $? -ne 0 ]; then
    echo "Workflow annulé"
    exit 0
fi

echo "Projet sélectionné : $projet"

# Étape 2 : Configuration du projet avec mixedform
config=$($WDIALOG --title "Configuration - $projet" \
    --mixedform "Configurez votre projet :" 18 70 6 \
    "Nom du projet:" 1 1 "MonProjet" 1 20 25 50 0 \
    "Version:" 2 1 "1.0.0" 2 20 10 15 0 \
    "Description:" 3 1 "Mon super projet" 3 20 30 100 0 \
    "Auteur:" 4 1 "$USER" 4 20 20 50 0 \
    "License:" 5 1 "MIT" 5 20 15 20 0 \
    "Date:" 6 1 "$(date +%Y-%m-%d)" 6 20 15 15 2 2>&1)

if [ $? -ne 0 ]; then
    echo "Configuration annulée"
    exit 0
fi

echo "Configuration enregistrée :"
echo "$config"
echo ""

# Étape 3 : Sélection du dossier de destination
destination=$($WDIALOG --title "Destination" \
    --fselect "$HOME/projets/" 15 60 2>&1)

if [ $? -ne 0 ]; then
    echo "Sélection du dossier annulée"
    exit 0
fi

echo "Dossier de destination : $destination"
echo ""

# Étape 4 : Simulation de la création avec mixedgauge
$WDIALOG --title "Création du projet" \
    --mixedgauge "Création en cours..." 18 60 100 \
    "Structure dossiers" "0" \
    "Fichiers config" "0" \
    "Dépendances" "0" \
    "Git init" "0" \
    "Documentation" "0"

echo ""
echo "=== Workflow terminé avec succès ! ==="
echo ""

# 6. Démonstration des statuts mixedgauge
echo "6. Démonstration des différents statuts de mixedgauge"
$WDIALOG --title "Statuts de tâches" \
    --mixedgauge "État des différentes tâches" 20 65 65 \
    "Tâche réussie" "0" \
    "Tâche échouée" "-1" \
    "Tâche ignorée" "-2" \
    "Tâche en cours" "-3" \
    "Backup DB" "0" \
    "Deploy serveur" "-1" \
    "Tests unitaires" "0" \
    "Tests intégration" "-3"

echo ""

# 7. FSelect avec différents points de départ
echo "7. Test fselect avec différents chemins"

# Sélection depuis /tmp
fichier_tmp=$($WDIALOG --title "Fichier temporaire" \
    --fselect "/tmp/test.txt" 12 60 2>&1)
echo "Fichier tmp : $fichier_tmp"

# Sélection depuis home
fichier_home=$($WDIALOG --title "Fichier home" \
    --fselect "$HOME/" 12 60 2>&1)
echo "Fichier home : $fichier_home"

echo ""
echo "=== Démonstration terminée ==="
echo ""
echo "Les nouveaux widgets disponibles sont :"
echo "  --fselect      : Sélection de fichier"
echo "  --inputmenu    : Menu avec capacité de renommage"
echo "  --mixedform    : Formulaire avec champs mixtes (texte/password/readonly)"
echo "  --mixedgauge   : Barre de progression avec liste de statuts"
