from flask import Flask, render_template, request
import random, socket, threading
import time
import json

#tcp server
TCP_IP = '127.0.0.1'
TCP_PORT = 7005
BUFFER_SIZE  = 20
conn = None
datajson =None
def launchServer(e):
    global conn
    global datajson
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    print('waiting for connection')
    while True:
       conn, addr = s.accept()
       print ('Connection address:', addr)
       recv_data = conn.recv(1024)  # Should be ready to read
       try: 
          datajson = json.loads(recv_data.decode("utf-8"))
          print(datajson)
       except Exception as e:
           pass



#flask app
app = Flask(__name__)
e = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global conn
    global e
    global datajson
    if request.method == 'POST':    
        try:
           conn.send(request.form['result'].encode('utf-8'))
        except Exception as e:
            pass
        datajson= None
        return render_template("index.html")
    #print(datajson)
    if request.method == 'GET':
        if datajson is None:
            return render_template("index.html")
        e.set()
        print(datajson["cmd"])
        print(datajson["cmd"]["cmd"])
        e.clear()
        return render_template("%s.html" % (datajson["cmd"]["cmd"].replace("--","")),text=datajson["cmd"]["options"]["text"])

if __name__ == "__main__":
    e = threading.Event()
    t = threading.Thread(target=launchServer,args=(e,))
    t.daemon = True
    t.start()
    app.run(debug=True,port=5003, use_reloader=False)
