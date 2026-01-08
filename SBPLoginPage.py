from flask import Flask, render_template, request, redirect, url_for
import os
import re


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
    nothing = request.args.get('nothing')
    cucumber_error = request.args.get('cucumber_error')

    competitors = []
  
    with open(os.path.join(DATA_DIR, 'competitors.txt')) as f:
        competitors = [line.strip() for line in f if line.strip()]
    
    return render_template(
        'admin_guardrails.html',
        name=name,
        competitors=competitors,
        success=success,
        nothing=nothing,
        cucumber_error=cucumber_error
    )



# handles submit and file storage
@app.route('/submit_guardrails', methods=['POST'])
def submit_guardrails():
    selected = request.form.getlist('guardrails')


    # If none required OR nothing selected
    if not selected:
        return redirect(url_for('admin_guardrails', name='admin', nothing=1))
    
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

        elif val == 'cucumberexp':
            if not txt or not is_valid_cucumber(txt):
                return redirect(url_for('admin_guardrails', name='admin', cucumber_error=1))

           # Write Cucumber in txt file
            with open(os.path.join(DATA_DIR, 'CucumberExpression.txt'), 'w') as f:
                    f.write(txt.strip())
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

    return redirect(url_for('admin_guardrails', name='admin', success=1))




#Function for cucumber expression
def is_valid_cucumber(expr):
    if not expr:
        return False

    # Must contain at least one placeholder
    if not re.search(r'\{(int|float|word|string|positive_number|negative_number)\}', expr):
        return False

    # Try converting to regex and compiling
    try:
        regex = cucumber_to_regex(expr)
        re.compile(regex)
        return True
    except re.error:
        return False


def cucumber_to_regex(expr):
    expr = re.escape(expr)
    expr = expr.replace(r'\{word\}', r'(\w+)')
    expr = expr.replace(r'\{int\}', r'(\d+)')
    expr = expr.replace(r'\{float\}', r'([\d.]+)')
    expr = expr.replace(r'\{string\}', r'"([^"]*)"')
    return '^' + expr + '$'





if __name__ == '__main__':
    app.run(debug=True)
