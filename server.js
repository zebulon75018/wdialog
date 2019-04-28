var nunjucks  = require('nunjucks');
var express   = require('express');
var net = require('net');

var app       = express();
const port = 3000;



/*
calendar, checklist, dselect, editbox, form, fselect, gauge, infobox, inputbox, inputmenu, menu, mixedform, mixedgauge, msgbox (message), passwordbox, passwordform, pause, progressbox, radiolist, tailbox, tailboxbg, textbox, timebox, and yesno (yes/no).
*/
class argParser {
    constructor() {
        this.title ="";
        this.backtitle="";
        this._content = "";
        this.optiondialog = [ { 'name'  :'calendar', 'func' : null}, 
        { 'name'  :'checklist', 'func' : null},
		{ 'name'  :		 'dselect', 'func' : null},
		{ 'name'  :		 'editbox',  'func' : null},
		{ 'name'  :		 'form',  'func' : null},
		{ 'name'  :		'fselect', 'func' : null},
		{ 'name'  :		 'gauge', 'func' : null},
        { 'name'  :		 'infobox',  'func' : function(self,i) {
            self._content = self.args[i+1];
            self._template= self.args[i].replace('--','') + ".html";
            } 
        },
		{ 'name'  :		'inputbox', 'func' : null},
		{ 'name'  :		 'inputmenu', 'func' : null},
		{ 'name'  :		 'menu', 'func' : null},
		{ 'name'  :		 'mixedform', 'func' : null},
		{ 'name'  :		 'mixedgauge', 'func' : null},
        { 'name'  :		 'msgbox' , 'func' : function(self,i) {
            self._content = self.args[i+1];
            self._template= self.args[i].replace('--','') + ".html";
            }
        },
		{ 'name'  :		 'passwordbox', 'func' : null},
		{ 'name'  :		 'passwordform', 'func' : null},
		{ 'name'  :		  'pause', 'func' : null},
		{ 'name'  :		 'progressbox', 'func' : null},
		{ 'name'  :		 'radiolist', 'func' : null},
		{ 'name'  :		 'tailbox', 'func' : null},
		{ 'name'  :		 'tailboxbg', 'func' : null},
		{ 'name'  :		 'textbox', 'func' : null},
		{ 'name'  :		 'timebox', 'func' : null},
		{ 'name'  :		 'yesno', 'func' : function(self,i) {
                self._content = self.args[i+1];
                self._template= self.args[i].replace('--','') + ".html";
            }
        },
        { 'name' : 'title' , 'func' : function(self,i) {
            self.title =  self.args[i+1];
            },
        }, 
        { 'name' : 'backtitle' , 'func' : function(self,i) {
            self.backtitle =  self.args[i+1];
            }
        }   
         
        ]
        this._template= "yesno.html";
	this._content = "";
    }


    parse( args ) {
        this.args = args;
        for (var i in args) {
            console.log(args[i])
            console.log(typeof(args[i]))
            if (args[i][0]=='-') {
                for (var j in this.optiondialog)
                {
                    if (args[i].replace("--","") ==  this.optiondialog[j].name)
                    {
                        this.optiondialog[j].func(this,parseInt(i));
                    }
                }
            }           
        }
    }

    template() {
        return this._template;
    }
    content() {
        return this._content;
    }

}

var argparse = new argParser();

var server = net.createServer(function(socket) {
    this.thesocket = socket;
    console.log('Connected');
    socket.on('data', function(data) {
        
        console.log('DATA ' + socket.remoteAddress + ': ' + data);
        argparse.parse(JSON.parse(data))
        // Write the data back to the socket, the client will receive it as data from the server
        //socket.write('You said "' + data + '"');
        
    });
    
    // Add a 'close' event handler to this instance of socket
    socket.on('close', function(data) {
        console.log('CLOSED: ' + socket.remoteAddress +' '+ socket.remotePort);
    });
	//socket.write('Echo server\r\n');
	//socket.pipe(socket);
});

server.listen(1337, '127.0.0.1');

nunjucks.configure('templates', {
  autoescape: true,
  express   : app
});

app.get('/', function(req, res) {
  res.render(argparse.template(), {
    title : argparse.title,
    backtitle : argparse.backtitle,
    content : argparse.content(),
    items : [
      { name : 'item #1' },
      { name : 'item #2' },
      { name : 'item #3' },
      { name : 'item #4' },
    ]
  });
});

app.get('/reply', function(req, res) {
    try {
        console.log(req.query.result)
        server.thesocket.write(req.query.result);
        res.render('index.html');
    } catch (err) {
        return err.message;
        }
}); 

app.listen(port, () => console.log(`Example app listening on port ${port}!`));
