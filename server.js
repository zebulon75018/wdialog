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

        this.optiondialog = [ 'calendar', 'checklist', 'dselect', 'editbox', 'form', 'fselect', 'gauge', 'infobox', 'inputbox', 'inputmenu', 'menu', 'mixedform', 'mixedgauge', 'msgbox' , 'passwordbox', 'passwordform', 'pause', 'progressbox', 'radiolist', 'tailbox', 'tailboxbg', 'textbox', 'timebox', 'yesno']

        this._template= "yesno.html";
    }

    parse( args ) {
        for (var i in args) {
            console.log(typeof(args[i]))
            if (args[i][0]=='-') {
                for (var j in this.optiondialog)
                {
                    if (args[i].replace("--","") ==  this.optiondialog[j])
                    {
                        console.log("FOUND "+this.optiondialog[j])
                        break;
                    }
                }
            }           
        }
        this._template= args[2].replace('--','') + ".html";
    }

    template() {
        return this._template;
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
    title : 'My First Nunjucks Page',
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
