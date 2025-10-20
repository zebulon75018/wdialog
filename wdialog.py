#!/usr/bin/env python3
"""
wdialog.py - Interface web pour dialog
Compatible avec les spécifications de dialog
"""

import sys
import socket
import json
import argparse

class WDialog:
    def __init__(self, server_host='127.0.0.1', server_port=5901):
        self.server_host = server_host
        self.server_port = server_port
        self.title = None
        self.backtitle = None
        self.ok_label = None
        self.cancel_label = None
        self.yes_label = None
        self.no_label = None
        self.extra_label = None
        self.help_label = None
        self.default_no = False
        self.no_cancel = False
        self.extra_button = False
        self.help_button = False
        
    def send_request(self, dialog_type, params):
        """Envoie une requête au serveur et attend la réponse"""
        try:
            # Créer la socket
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((self.server_host, self.server_port))
            
            # Préparer la requête
            request = {
                'type': dialog_type,
                'params': params,
                'title': self.title,
                'backtitle': self.backtitle,
                'labels': {
                    'ok': self.ok_label,
                    'cancel': self.cancel_label,
                    'yes': self.yes_label,
                    'no': self.no_label,
                    'extra': self.extra_label,
                    'help': self.help_label
                },
                'options': {
                    'default_no': self.default_no,
                    'no_cancel': self.no_cancel,
                    'extra_button': self.extra_button,
                    'help_button': self.help_button
                }
            }
            
            # Envoyer la requête
            request_json = json.dumps(request) + '\n\n'
            client.sendall(request_json.encode('utf-8'))
            
            # Recevoir la réponse
            response_data = b''
            while True:
                chunk = client.recv(4096)
                if not chunk:
                    break
                response_data += chunk
                if b'\n' in response_data:
                    break
            
            response = json.loads(response_data.decode('utf-8'))
            client.close()
            
            # Afficher la sortie si présente
            if 'output' in response and response['output']:
                print(response['output'], end='')
            
            # Retourner le code de sortie
            return response.get('exit_code', 0)
            
        except Exception as e:
            print(f"Erreur de connexion au serveur: {e}", file=sys.stderr)
            return 255

def main():
    parser = argparse.ArgumentParser(description='Web Dialog - Interface web pour dialog')
    
    # Options communes
    parser.add_argument('--title', type=str, help='Titre de la boîte de dialogue')
    parser.add_argument('--backtitle', type=str, help='Titre de fond')
    parser.add_argument('--ok-label', type=str, help='Label du bouton OK')
    parser.add_argument('--cancel-label', type=str, help='Label du bouton Cancel')
    parser.add_argument('--yes-label', type=str, help='Label du bouton Yes')
    parser.add_argument('--no-label', type=str, help='Label du bouton No')
    parser.add_argument('--extra-label', type=str, help='Label du bouton Extra')
    parser.add_argument('--help-label', type=str, help='Label du bouton Help')
    parser.add_argument('--defaultno', action='store_true', help='Défaut sur No')
    parser.add_argument('--no-cancel', '--nocancel', action='store_true', help='Pas de bouton Cancel')
    parser.add_argument('--extra-button', action='store_true', help='Bouton Extra')
    parser.add_argument('--help-button', action='store_true', help='Bouton Help')
    
    # Types de widgets
    parser.add_argument('--yesno', nargs=3, metavar=('text', 'height', 'width'), help='Boîte Yes/No')
    parser.add_argument('--msgbox', nargs=3, metavar=('text', 'height', 'width'), help='Boîte de message')
    parser.add_argument('--inputbox', nargs='+', metavar='arg', help='Boîte de saisie: text height width [init]')
    parser.add_argument('--passwordbox', nargs='+', metavar='arg', help='Boîte de mot de passe: text height width [init]')
    parser.add_argument('--textbox', nargs=3, metavar=('file', 'height', 'width'), help='Affichage de texte')
    parser.add_argument('--menu', nargs='+', metavar='arg', help='Menu: text height width menu-height tag1 item1 ...')
    parser.add_argument('--checklist', nargs='+', metavar='arg', help='Checklist: text height width list-height tag1 item1 status1 ...')
    parser.add_argument('--radiolist', nargs='+', metavar='arg', help='Radiolist: text height width list-height tag1 item1 status1 ...')
    parser.add_argument('--gauge', nargs='+', metavar='arg', help='Gauge: text height width [percent]')
    parser.add_argument('--infobox', nargs=3, metavar=('text', 'height', 'width'), help='Boîte d\'information')
    parser.add_argument('--calendar', nargs='+', metavar='arg', help='Calendrier: text height width [day month year]')
    parser.add_argument('--timebox', nargs='+', metavar='arg', help='Timebox: text height width [hour minute second]')
    parser.add_argument('--fselect', nargs='+', metavar='arg', help='Sélection de fichier: filepath height width')
    parser.add_argument('--inputmenu', nargs='+', metavar='arg', help='Menu avec rename: text height width menu-height tag1 item1 ...')
    parser.add_argument('--mixedform', nargs='+', metavar='arg', help='Formulaire mixte: text height width formheight label1 y1 x1 item1 ...')
    parser.add_argument('--mixedgauge', nargs='+', metavar='arg', help='Gauge mixte: text height width percent tag1 item1 ...')
    
    args = parser.parse_args()
    
    # Créer l'instance WDialog
    wd = WDialog()
    
    # Configurer les options communes
    if args.title:
        wd.title = args.title
    if args.backtitle:
        wd.backtitle = args.backtitle
    if args.ok_label:
        wd.ok_label = args.ok_label
    if args.cancel_label:
        wd.cancel_label = args.cancel_label
    if args.yes_label:
        wd.yes_label = args.yes_label
    if args.no_label:
        wd.no_label = args.no_label
    if args.extra_label:
        wd.extra_label = args.extra_label
    if args.help_label:
        wd.help_label = args.help_label
    
    wd.default_no = args.defaultno
    wd.no_cancel = args.no_cancel
    wd.extra_button = args.extra_button
    wd.help_button = args.help_button
    
    # Traiter le type de widget
    exit_code = 1
    
    if args.yesno:
        text, height, width = args.yesno
        exit_code = wd.send_request('yesno', {
            'text': text,
            'height': height,
            'width': width
        })
    
    elif args.msgbox:
        text, height, width = args.msgbox
        exit_code = wd.send_request('msgbox', {
            'text': text,
            'height': height,
            'width': width
        })
    
    elif args.inputbox:
        if len(args.inputbox) < 3:
            print("Erreur: --inputbox nécessite au moins 3 arguments (text height width)", file=sys.stderr)
            sys.exit(255)
        text, height, width = args.inputbox[0], args.inputbox[1], args.inputbox[2]
        init = args.inputbox[3] if len(args.inputbox) > 3 else ''
        exit_code = wd.send_request('inputbox', {
            'text': text,
            'height': height,
            'width': width,
            'init': init
        })
    
    elif args.passwordbox:
        if len(args.passwordbox) < 3:
            print("Erreur: --passwordbox nécessite au moins 3 arguments (text height width)", file=sys.stderr)
            sys.exit(255)
        text, height, width = args.passwordbox[0], args.passwordbox[1], args.passwordbox[2]
        init = args.passwordbox[3] if len(args.passwordbox) > 3 else ''
        exit_code = wd.send_request('passwordbox', {
            'text': text,
            'height': height,
            'width': width,
            'init': init
        })
    
    elif args.textbox:
        file, height, width = args.textbox
        try:
            with open(file, 'r') as f:
                content = f.read()
            exit_code = wd.send_request('textbox', {
                'text': content,
                'height': height,
                'width': width,
                'file': file
            })
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier: {e}", file=sys.stderr)
            exit_code = 255
    
    elif args.menu:
        if len(args.menu) < 4:
            print("Erreur: --menu nécessite au moins 4 arguments", file=sys.stderr)
            sys.exit(255)
        text, height, width, menu_height = args.menu[0:4]
        items = args.menu[4:]
        menu_items = []
        for i in range(0, len(items), 2):
            if i + 1 < len(items):
                menu_items.append({'tag': items[i], 'item': items[i+1]})
        
        exit_code = wd.send_request('menu', {
            'text': text,
            'height': height,
            'width': width,
            'menu_height': menu_height,
            'items': menu_items
        })
    
    elif args.checklist:
        if len(args.checklist) < 4:
            print("Erreur: --checklist nécessite au moins 4 arguments", file=sys.stderr)
            sys.exit(255)
        text, height, width, list_height = args.checklist[0:4]
        items = args.checklist[4:]
        checklist_items = []
        for i in range(0, len(items), 3):
            if i + 2 < len(items):
                checklist_items.append({
                    'tag': items[i],
                    'item': items[i+1],
                    'status': items[i+2].lower() in ['on', 'true', '1']
                })
        
        exit_code = wd.send_request('checklist', {
            'text': text,
            'height': height,
            'width': width,
            'list_height': list_height,
            'items': checklist_items
        })
    
    elif args.radiolist:
        if len(args.radiolist) < 4:
            print("Erreur: --radiolist nécessite au moins 4 arguments", file=sys.stderr)
            sys.exit(255)
        text, height, width, list_height = args.radiolist[0:4]
        items = args.radiolist[4:]
        radiolist_items = []
        for i in range(0, len(items), 3):
            if i + 2 < len(items):
                radiolist_items.append({
                    'tag': items[i],
                    'item': items[i+1],
                    'status': items[i+2].lower() in ['on', 'true', '1']
                })
        
        exit_code = wd.send_request('radiolist', {
            'text': text,
            'height': height,
            'width': width,
            'list_height': list_height,
            'items': radiolist_items
        })
    
    elif args.gauge:
        if len(args.gauge) < 3:
            print("Erreur: --gauge nécessite au moins 3 arguments", file=sys.stderr)
            sys.exit(255)
        text, height, width = args.gauge[0:3]
        percent = int(args.gauge[3]) if len(args.gauge) > 3 else 0
        exit_code = wd.send_request('gauge', {
            'text': text,
            'height': height,
            'width': width,
            'percent': percent
        })
    
    elif args.infobox:
        text, height, width = args.infobox
        exit_code = wd.send_request('infobox', {
            'text': text,
            'height': height,
            'width': width
        })
    
    elif args.calendar:
        if len(args.calendar) < 3:
            print("Erreur: --calendar nécessite au moins 3 arguments", file=sys.stderr)
            sys.exit(255)
        text, height, width = args.calendar[0:3]
        day = int(args.calendar[3]) if len(args.calendar) > 3 else 0
        month = int(args.calendar[4]) if len(args.calendar) > 4 else 0
        year = int(args.calendar[5]) if len(args.calendar) > 5 else 0
        exit_code = wd.send_request('calendar', {
            'text': text,
            'height': height,
            'width': width,
            'day': day,
            'month': month,
            'year': year
        })
    
    elif args.timebox:
        if len(args.timebox) < 3:
            print("Erreur: --timebox nécessite au moins 3 arguments", file=sys.stderr)
            sys.exit(255)
        text, height, width = args.timebox[0:3]
        hour = int(args.timebox[3]) if len(args.timebox) > 3 else 0
        minute = int(args.timebox[4]) if len(args.timebox) > 4 else 0
        second = int(args.timebox[5]) if len(args.timebox) > 5 else 0
        exit_code = wd.send_request('timebox', {
            'text': text,
            'height': height,
            'width': width,
            'hour': hour,
            'minute': minute,
            'second': second
        })
    
    elif args.fselect:
        if len(args.fselect) < 3:
            print("Erreur: --fselect nécessite au moins 3 arguments", file=sys.stderr)
            sys.exit(255)
        filepath = args.fselect[0] if args.fselect[0] else '.'
        height, width = args.fselect[1], args.fselect[2]
        exit_code = wd.send_request('fselect', {
            'filepath': filepath,
            'height': height,
            'width': width
        })
    
    elif args.inputmenu:
        if len(args.inputmenu) < 4:
            print("Erreur: --inputmenu nécessite au moins 4 arguments", file=sys.stderr)
            sys.exit(255)
        text, height, width, menu_height = args.inputmenu[0:4]
        items = args.inputmenu[4:]
        menu_items = []
        for i in range(0, len(items), 2):
            if i + 1 < len(items):
                menu_items.append({'tag': items[i], 'item': items[i+1]})
        
        exit_code = wd.send_request('inputmenu', {
            'text': text,
            'height': height,
            'width': width,
            'menu_height': menu_height,
            'items': menu_items
        })
    
    elif args.mixedform:
        if len(args.mixedform) < 4:
            print("Erreur: --mixedform nécessite au moins 4 arguments", file=sys.stderr)
            sys.exit(255)
        text, height, width, formheight = args.mixedform[0:4]
        fields_data = args.mixedform[4:]
        fields = []
        # Format: label y x item y x flen ilen itype
        for i in range(0, len(fields_data), 9):
            if i + 8 < len(fields_data):
                fields.append({
                    'label': fields_data[i],
                    'label_y': int(fields_data[i+1]),
                    'label_x': int(fields_data[i+2]),
                    'item': fields_data[i+3],
                    'item_y': int(fields_data[i+4]),
                    'item_x': int(fields_data[i+5]),
                    'flen': int(fields_data[i+6]),
                    'ilen': int(fields_data[i+7]),
                    'itype': int(fields_data[i+8])
                })
        
        exit_code = wd.send_request('mixedform', {
            'text': text,
            'height': height,
            'width': width,
            'formheight': formheight,
            'fields': fields
        })
    
    elif args.mixedgauge:
        if len(args.mixedgauge) < 4:
            print("Erreur: --mixedgauge nécessite au moins 4 arguments", file=sys.stderr)
            sys.exit(255)
        text, height, width, percent = args.mixedgauge[0:4]
        items_data = args.mixedgauge[4:]
        items = []
        for i in range(0, len(items_data), 2):
            if i + 1 < len(items_data):
                items.append({'tag': items_data[i], 'item': items_data[i+1]})
        
        exit_code = wd.send_request('mixedgauge', {
            'text': text,
            'height': height,
            'width': width,
            'percent': int(percent),
            'items': items
        })
    
    else:
        parser.print_help()
        exit_code = 255
    
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
