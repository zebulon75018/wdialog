
var net = require('net');

var client = new net.Socket();
client.connect(1337, '127.0.0.1', function() {
	console.log('Connected');
	client.write( JSON.stringify(process.argv ));
});

client.on('data', function(data) {
    this.result = data;
	console.log('Received: ' + data);
	client.destroy(); // kill client after server's response
});

client.on('close', function() {
    console.log('Connection closed');
    
    if ( this.result ) {
        process.exit(0);
    } else 
    {
        process.exit(1); 
    }
});