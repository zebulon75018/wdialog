#!/bin/bash

# inputbox - demonstrate the input dialog box with a temporary file

# Define the dialog exit status codes
: ${DIALOG_OK=0}
: ${DIALOG_CANCEL=1}
: ${DIALOG_HELP=2}
: ${DIALOG_EXTRA=3}
: ${DIALOG_ITEM_HELP=4}
: ${DIALOG_ESC=255}

python client2.py --title "Hello" --yesno 'Hello world!' 6 20

return_value=$?

echo $return_value

# Act on it
case $return_value in
  $DIALOG_OK)
    python client2.py --title "Hello" --msgbox 'You pressed OK!' 6 20
    echo "Result: Ok";;
  $DIALOG_CANCEL)
    python client2.py --title "Hello" --msgbox 'You pressed Cancel!' 6 20
    echo "Cancel pressed." ;;
esac
