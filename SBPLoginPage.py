from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)
FILE_PATH = os.path.join(DATA_DIR, 'selected_guardrails.txt')

@app.route('/')
def hello_world():
    return render_template('SBPLogin.html')

@app.route('/form_login', methods=['POST'])
def form_login():
    user = request.form['username']
    pwd = request.form['password']

    if user == 'admin' and pwd == 'admin':
        return redirect(url_for('admin_guardrails', name='admin'))
    else:
        return render_template('SBPLogin.html', info="Invalid credentials")
    
# admin page routing
@app.route('/admin_guardrails/<name>')
def admin_guardrails(name):
    return render_template('admin_guardrails.html', name=name)

# handles submit and file storage
@app.route('/submit_guardrails', methods=['POST'])
def submit_guardrails():
    selected = request.form.getlist('guardrails')

    structured = []

    for val in selected:
        sub_key = f"sub_{val}"
        subs = request.form.getlist(sub_key)

        if subs:
            block = val + "[\n" + ",\n".join(subs) + "\n]"
            structured.append(block)
        else:
            structured.append(val)

    output = ",\n".join(structured)

    with open(FILE_PATH, 'w') as f:
        f.write(output)

    return redirect(url_for('admin_guardrails', name='admin'))





if __name__ == '__main__':
    app.run(debug=True)
