from flask import Flask, render_template, request
import openpyxl

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def gfg():
    return render_template('index.html',template_folder='templates')

@app.route('/developer', methods=['GET', 'POST'])
def developer():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone_number = request.form.get('number')
        domain = request.form.get('domain')
        github_link = request.form.get('glink')
        linkedin_link = request.form.get('llink')
        experience = request.form.get('experience')
        
        wb = openpyxl.load_workbook('Developers.xlsx')
        sheet = wb.active
        sheet.append([name, email, phone_number, domain, github_link, linkedin_link, experience])
        wb.save('Developers.xlsx')

    return render_template('index1.html',template_folder='templates')

@app.route('/client', methods=['GET', 'POST'])
def client():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone_number = request.form.get('number')
        '''domain = request.form.get('domain')
        requirement = request.form.get('Requirement')
        budget=request.form.get('Budget')
        time=request.form.get('time')'''

        wb = openpyxl.load_workbook('Clients.xlsx')
        sheet = wb.active
        sheet.append([name, email, phone_number])
        wb.save('Clients.xlsx')
    
    return render_template('index2.html',template_folder='templates')


if __name__ == '__main__':
    app.run()