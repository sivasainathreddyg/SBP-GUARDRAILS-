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
    success = request.args.get('success')

    competitors = []
  
    with open(os.path.join(DATA_DIR, 'competitors.txt')) as f:
        competitors = [line.strip() for line in f if line.strip()]
    
    return render_template(
        'admin_guardrails.html',
        name=name,
        competitors=competitors,
        success=success
    )



# handles submit and file storage
@app.route('/submit_guardrails', methods=['POST'])
def submit_guardrails():
    selected = request.form.getlist('guardrails')
    structured = []

    detect_pii_subs = []
    selected_competitors = []
    codefinder_subs = []

    for val in selected:
        subs = request.form.getlist(f"sub_{val}")
        txt = request.form.get(f"input_{val}")

        if val == 'detectpii':
            detect_pii_subs = subs
            structured.append(val)

        elif val == 'competitor':
            selected_competitors.extend(subs)
            if txt:
                selected_competitors.append(txt.strip())
            structured.append(val)

        elif val == 'codefinder':
            codefinder_subs = subs
            structured.append(val)

        else:
            if subs:
                structured.append(val + "[\n" + ",\n".join(subs) + "\n]")
            else:
                structured.append(val)

    # Write selected parent guardrails only
    with open(FILE_PATH, 'w') as f:
        f.write(",\n".join(structured))

    # Write Detect PII sub-options
    detect_pii_file = os.path.join(DATA_DIR, 'detectPII.txt')
    with open(detect_pii_file, 'w') as f:
        for item in detect_pii_subs:
            f.write(item + "\n")

    # Write code finder sub-list
    with open(os.path.join(DATA_DIR, 'CodeFinder.txt'), 'w') as f:
        for x in codefinder_subs:
            f.write(x + "\n")

    # code for competitors.txt
    if selected_competitors:
        comp_file = os.path.join(DATA_DIR, 'competitors.txt')

        cleaned = []
        seen = set()
        for c in selected_competitors:
            c = c.strip()
            if c and c.lower() not in seen:
                seen.add(c.lower())
                cleaned.append(c)

        with open(comp_file, 'w') as f:
            for c in cleaned:
                f.write(c + "\n")

    return redirect(url_for('admin_guardrails', name='admin'))








if __name__ == '__main__':
    app.run(debug=True)
