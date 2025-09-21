from flask import Flask, request, render_template_string
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return '<a href="/echo?msg=hello">try echo</a>'

# Vulnerable endpoint: command injection via subprocess with shell=True
@app.route('/echo')
def echo():
    msg = request.args.get('msg', '')
    # insecure: using shell=True with untrusted input -> Semgrep should catch this
    subprocess.run(f"echo {msg}", shell=True)
    # insecure: reflected XSS - rendering user input without escaping
    return render_template_string(f"<h1>Echo:</h1><div>{msg}</div>")

if __name__ == '__main__':
    # bind to 0.0.0.0 so scanners can reach it
    app.run(host='0.0.0.0', port=5000, debug=False)
