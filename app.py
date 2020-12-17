from flask import Flask,render_template,request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")


    
@app.route('/register',methods=['POST','GET'])
def register():
    #Form Registration
    if request.method == 'POST':
        usn =  request.form.get('usn')
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('pass')
        phone = request.form.get('phone')
        return name
    return render_template('register.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        usn =  request.form.get('usn')
        password = request.form.get('pass')
        return usn
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)