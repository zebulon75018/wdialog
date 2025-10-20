#!/bin/bash
# Test rapide de tous les widgets
# Utilisez ce script pour vérifier que tout fonctionne

WDIALOG="python3 wdialog.py"

echo "╔════════════════════════════════════════╗"
echo "║   Test Rapide des Widgets WDialog     ║"
echo "╚════════════════════════════════════════╝"
echo ""
echo "Ce script va tester tous les widgets disponibles."
echo "Appuyez sur Entrée pour commencer..."
read

test_widget() {
    local name=$1
    local description=$2
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Test: $name"
    echo "Description: $description"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# Test 1: YesNo
test_widget "yesno" "Boîte Oui/Non"
$WDIALOG --title "Test YesNo" --yesno "Est-ce que tout fonctionne ?" 10 50
echo "Code retour: $?"
echo ""

# Test 2: MsgBox
test_widget "msgbox" "Boîte de message"
$WDIALOG --title "Test MsgBox" --msgbox "Ceci est un message d'information." 10 50
echo ""

# Test 3: InputBox
test_widget "inputbox" "Boîte de saisie"
result=$($WDIALOG --title "Test InputBox" --inputbox "Entrez votre prénom :" 10 50 "John" 2>&1)
echo "Valeur saisie: $result"
echo ""

# Test 4: PasswordBox
test_widget "passwordbox" "Saisie mot de passe"
pass=$($WDIALOG --title "Test PasswordBox" --passwordbox "Entrez un mot de passe :" 10 50 2>&1)
echo "Longueur du mot de passe: ${#pass}"
echo ""

# Test 5: Menu
test_widget "menu" "Menu de sélection"
choice=$($WDIALOG --title "Test Menu" --menu "Choisissez une option :" 15 50 3 \
    "1" "Option numéro 1" \
    "2" "Option numéro 2" \
    "3" "Option numéro 3" 2>&1)
echo "Option choisie: $choice"
echo ""

# Test 6: CheckList
test_widget "checklist" "Liste à cocher"
items=$($WDIALOG --title "Test CheckList" --checklist "Sélectionnez vos choix :" 15 60 4 \
    "item1" "Premier item" on \
    "item2" "Deuxième item" off \
    "item3" "Troisième item" on \
    "item4" "Quatrième item" off 2>&1)
echo "Items sélectionnés: $items"
echo ""

# Test 7: RadioList
test_widget "radiolist" "Liste radio"
radio=$($WDIALOG --title "Test RadioList" --radiolist "Choisissez une option :" 15 60 3 \
    "opt1" "Première option" on \
    "opt2" "Deuxième option" off \
    "opt3" "Troisième option" off 2>&1)
echo "Option choisie: $radio"
echo ""

# Test 8: Calendar
test_widget "calendar" "Sélection de date"
date=$($WDIALOG --title "Test Calendar" --calendar "Sélectionnez une date :" 10 50 2>&1)
echo "Date sélectionnée: $date"
echo ""

# Test 9: TimeBox
test_widget "timebox" "Sélection d'heure"
time=$($WDIALOG --title "Test TimeBox" --timebox "Sélectionnez une heure :" 10 50 2>&1)
echo "Heure sélectionnée: $time"
echo ""

# Test 10: FSelect
test_widget "fselect" "Sélection de fichier"
file=$($WDIALOG --title "Test FSelect" --fselect "/tmp/" 15 60 2>&1)
echo "Fichier/Chemin: $file"
echo ""

# Test 11: InputMenu
test_widget "inputmenu" "Menu avec rename"
inmenu=$($WDIALOG --title "Test InputMenu" --inputmenu "Sélectionnez ou renommez :" 15 60 3 \
    "srv1" "Serveur 1" \
    "srv2" "Serveur 2" \
    "srv3" "Serveur 3" 2>&1)
echo "Résultat: $inmenu"
echo ""

# Test 12: MixedForm
test_widget "mixedform" "Formulaire mixte"
form=$($WDIALOG --title "Test MixedForm" --mixedform "Remplissez le formulaire :" 16 70 4 \
    "Nom:" 1 1 "Dupont" 1 10 20 30 0 \
    "Prénom:" 2 1 "Jean" 2 10 20 30 0 \
    "Password:" 3 1 "" 3 10 20 30 1 \
    "ID (ro):" 4 1 "12345" 4 10 10 10 2 2>&1)
echo "Données du formulaire:"
echo "$form"
echo ""

# Test 13: InfoBox (temporaire)
test_widget "infobox" "Information temporaire (2s)"
$WDIALOG --title "Test InfoBox" --infobox "Ceci disparaîtra dans 2 secondes..." 8 50
sleep 2
echo ""

# Test 14: TextBox (créer un fichier temporaire)
test_widget "textbox" "Affichage de texte"
tmpfile=$(mktemp)
cat > "$tmpfile" << EOF
Ceci est un fichier de test
pour le widget textbox.

Ligne 3
Ligne 4
Ligne 5

Vous pouvez défiler si le contenu est long.
EOF
$WDIALOG --title "Test TextBox" --textbox "$tmpfile" 15 60
rm "$tmpfile"
echo ""

# Test 15: Gauge (simulation)
test_widget "gauge" "Barre de progression"
(
    for i in {0..100..10}; do
        echo $i
        sleep 0.1
    done
) | $WDIALOG --title "Test Gauge" --gauge "Chargement..." 10 50 0
echo ""

# Test 16: MixedGauge
test_widget "mixedgauge" "Gauge avec statuts"
$WDIALOG --title "Test MixedGauge" --mixedgauge "État des tâches" 18 60 80 \
    "Tâche 1" "0" \
    "Tâche 2" "-3" \
    "Tâche 3" "-2" \
    "Tâche 4" "0" \
    "Tâche 5" "-1"
echo ""

echo "╔════════════════════════════════════════╗"
echo "║        Tests Terminés !                ║"
echo "╚════════════════════════════════════════╝"
echo ""
echo "Tous les widgets ont été testés."
echo ""
echo "Widgets testés:"
echo "  ✓ yesno         - Boîte Oui/Non"
echo "  ✓ msgbox        - Message"
echo "  ✓ inputbox      - Saisie texte"
echo "  ✓ passwordbox   - Saisie mot de passe"
echo "  ✓ menu          - Menu"
echo "  ✓ checklist     - Liste à cocher"
echo "  ✓ radiolist     - Liste radio"
echo "  ✓ calendar      - Calendrier"
echo "  ✓ timebox       - Heure"
echo "  ✓ fselect       - Sélection fichier (NOUVEAU)"
echo "  ✓ inputmenu     - Menu avec rename (NOUVEAU)"
echo "  ✓ mixedform     - Formulaire mixte (NOUVEAU)"
echo "  ✓ infobox       - Info temporaire"
echo "  ✓ textbox       - Affichage texte"
echo "  ✓ gauge         - Progression"
echo "  ✓ mixedgauge    - Progression + statuts (NOUVEAU)"
echo ""
