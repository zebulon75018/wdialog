i# Dialog Web Interface

Modern web interface to display dialog boxes from bash scripts, compatible with the `dialog` command specifications.  
This project is a WIP.

## 🎯 Features

- ✅ Compatible with the `dialog` command syntax
- 🎨 Modern, responsive web UI with Bootstrap
- 🔌 Real-time communication via WebSocket
- 📱 Modern, animated design
- 🚀 Easy to integrate into existing bash scripts

## 📋 Supported widget types

- `--yesno`: Yes/No dialog
- `--msgbox`: Message box
- `--inputbox`: Text input
- `--passwordbox`: Password input
- `--textbox`: Text file display
- `--menu`: Selection menu
- `--checklist`: Checklist (multiple selection)
- `--radiolist`: Radio list (single selection)
- `--gauge`: Progress bar
- `--infobox`: Temporary information
- `--calendar`: Date picker
- `--timebox`: Time picker
- `--fselect`: **[NEW]** File/folder selection
- `--inputmenu`: **[NEW]** Menu with rename capability
- `--mixedform`: **[NEW]** Form with mixed fields (text/password/readonly)
- `--mixedgauge`: **[NEW]** Progress bar with status list

## 🛠️ Installation

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Installation steps

1. **Clone or create the project structure:**

```bash
mkdir dialog-web
cd dialog-web

1.  **Install Python dependencies:**
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pip install flask flask-socketio python-socketio   `

1.  **Create the folders:**
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   mkdir templates   `

1.  **Place the files:**
    

*   dialog\_server.py: The main Flask server
    
*   wdialog.py: The client script (make it executable)
    
*   templates/dialog\_interface.html: The HTML template
    
*   example\_usage.sh: Usage example (optional)
    

1.  **Make wdialog.py executable:**
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   chmod +x wdialog.py   `

🚀 Usage
--------

### 1\. Start the server

In a first terminal:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python3 dialog_server.py   `

The server starts on:

*   Web interface: [http://localhost:5000](http://localhost:5000)
    
*   Socket server: localhost:5001
    

### 2\. Open the web interface

Open your browser and go to: [**http://localhost:5000**](http://localhost:5000)

You’ll see the waiting screen indicating the interface is ready to receive requests.

### 3\. Use wdialog.py in your bash scripts

In a second terminal, you can now use wdialog.py just like you would use dialog:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   # Simple example  python3 wdialog.py --title "Test" --yesno "Do you want to continue?" 10 50   `

Or in a bash script:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   #!/bin/bash  # Define the command  WDIALOG="python3 wdialog.py"  # Use like dialog  $WDIALOG --title "Confirmation" --yesno "Continue?" 10 50  if [ $? -eq 0 ]; then      echo "Yes selected"  else      echo "No selected"  fi  # Text input  name=$($WDIALOG --title "Name" --inputbox "Enter your name:" 10 50 2>&1)  echo "Name: $name"  # Menu  choice=$($WDIALOG --menu "Menu:" 15 50 3 \      "1" "Option 1" \      "2" "Option 2" \      "3" "Option 3" 2>&1)  echo "Choice: $choice"   `

📖 Examples
-----------

### Yes/No box

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python3 wdialog.py --title "Confirmation" --yesno "Do you want to continue?" 10 50   `

### Input box

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   name=$(python3 wdialog.py --title "Input" --inputbox "Enter your name:" 10 50 2>&1)  echo "Name: $name"   `

### Menu

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   choice=$(python3 wdialog.py --title "Menu" --menu "Choose:" 15 50 3 \      "opt1" "Option 1" \      "opt2" "Option 2" \      "opt3" "Option 3" 2>&1)   `

### Checklist

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   modules=$(python3 wdialog.py --checklist "Modules:" 15 60 3 \      "apache" "Apache server" on \      "mysql" "Database" off \      "php" "PHP" on 2>&1)   `

### Progress bar

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   (      for i in {0..100..10}; do          echo $i          sleep 0.2      done  ) | python3 wdialog.py --gauge "Installation..." 10 50 0   `

### File selection (NEW)

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   file=$(python3 wdialog.py --fselect "/tmp/" 15 60 2>&1)  echo "Selected file: $file"   `

### Menu with rename (NEW)

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   choice=$(python3 wdialog.py --inputmenu "Servers:" 15 60 3 \      "srv1" "Web Server" \      "srv2" "DB Server" \      "srv3" "Redis Cache" 2>&1)  # Returns either the selected tag, or "RENAMED tag new_name"   `

### Mixed form (NEW)

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   # Format: label y x item y x flen ilen itype  # itype: 0=text, 1=password, 2=readonly  result=$(python3 wdialog.py --mixedform "Configuration:" 18 70 5 \      "Name:" 1 1 "John" 1 10 20 30 0 \      "Pass:" 2 1 "" 2 10 20 30 1 \      "ID:" 3 1 "12345" 3 10 10 10 2 \      "Email:" 4 1 "john@example.com" 4 10 30 50 0 \      "Phone:" 5 1 "+33612345678" 5 10 20 20 0 2>&1)   `

### Gauge with statuses (NEW)

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   # Statuses: 0=Success, -1=Failed, -2=Skipped, -3=In progress  python3 wdialog.py --mixedgauge "Installation" 18 60 75 \      "Download" "0" \      "Installation" "-3" \      "Configuration" "-2" \      "Tests" "-2" \      "Finalization" "-2"   `

🎨 Customization
----------------

### Supported common options

*   \--title: Dialog title
    
*   \--backtitle: Background title
    
*   \--ok-label: OK button label
    
*   \--cancel-label: Cancel button label
    
*   \--yes-label: Yes button label
    
*   \--no-label: No button label
    
*   \--defaultno: Set “No” as default
    
*   \--no-cancel: Hide the Cancel button
    
*   \--extra-button: Add an extra button
    
*   \--help-button: Add a Help button
    

### Example with options

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python3 wdialog.py \      --title "My Title" \      --backtitle "Application v1.0" \      --yes-label "Continue" \      --no-label "Stop" \      --yesno "Do you want to continue?" 10 50   `

🔧 Advanced configuration
-------------------------

### Change the server port

Edit in dialog\_server.py:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   socketio.run(app, host='0.0.0.0', port=5000, debug=True)   `

### Use a remote server

Edit the server address in wdialog.py:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   wd = WDialog(server_host='192.168.1.100', server_port=5001)   `

📝 Return codes
---------------

Same as the original dialog command:

*   0: OK / Yes selected
    
*   1: Cancel / No selected
    
*   255: Error or timeout
    

🐛 Troubleshooting
------------------

### The server doesn’t start

Check that ports 5000 and 5001 are not already in use:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   lsof -i :5000  lsof -i :5001   `

### Connection error

Make sure that:

1.  The Flask server is running
    
2.  The web interface is open in the browser
    
3.  The browser is connected (check the status indicator in the top-right)
    

### Buttons don’t respond

Check the browser’s JavaScript console (F12) for possible errors.

📄 Project structure
--------------------

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   dialog-web/  ├── dialog_server.py          # Flask + WebSocket server  ├── wdialog.py               # Python client (dialog-compatible)  ├── templates/  │   └── dialog_interface.html # Web interface  ├── example_usage.sh          # Usage examples  └── README.md                # This file   `

🤝 Contributing
---------------

Contributions are welcome! Feel free to:

*   Report bugs
    
*   Propose new features
    
*   Improve the documentation
    

📜 License
----------

This project is free to use for personal and commercial projects.

🎉 Credits
----------

*   Interface: Bootstrap 5 + jQuery
    
*   Real-time communication: Socket.IO
    
*   Compatible with: dialog (Linux)
    

**Happy scripting! 🚀**

