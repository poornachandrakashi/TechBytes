from flask import Flask,render_template,flash,url_for,redirect,session,logging,request
import mysql.connector
from functools import wraps
from passlib.hash import sha256_crypt

app = Flask(__name__)


#Config Mysql
mydb=mysql.connector.connect(host='localhost',user="root",passwd="",database="techbytes")


@app.route('/')
def home():
    return render_template("home.html")

#hello this is navya
    
@app.route('/register',methods=['POST','GET'])
def register():
    #Form Registration
    if request.method == 'POST':
        usn =  request.form.get('usn')
        name = request.form.get('name')
        email = request.form.get('email')
        passwords = request.form.get('pass')
        phone = request.form.get('phone')
        # Creating Cursor
        cur=mydb.cursor()
        
        
        cur.execute("INSERT INTO auth(usn,name,email,passwords,phone) VALUES(%s,%s,%s,%s,%s)",(usn,name,email,passwords,phone))
        
        #Commit to db
        mydb.commit()
        
        #close Connection
        cur.close()
        
        flash("Your are not registered and can log in","success")
        
        redirect('/home')
        # return form.email.data
        return render_template('home.html')
        
    return render_template('register.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        usn =  request.form.get('usn')
        password_candidate = request.form.get('pass')
        
        
        #Create Cursor
        cur=mydb.cursor(buffered=True)
        
        #Get user by username
        
        result=cur.execute("select * from auth where usn = %s",[usn])

        if result == None:
            #Getting the stored hashed
            data=cur.fetchone()
            password=data[4]
            #Comparing the password
            if password_candidate==password:
                session['logged_in']=True
                session['usn']=usn
                flash("Congrats you are logged in")
                return "Password Matched"
                app.logger.info('Password Matched')
                
            else:
                app.logger.info("Password not matched")
                error="Invalid login"
                flash("password not matched")
                return "Password Not Matched"
            #Close connection
            cur.close()
        else:
            app.logger.info("No User")
            flash("No user found")
            return "hello"

                    
    return render_template('login.html')

@app.route('/lostFetch')
def lostFetch():
    return "Hello!!! this is Lost and found fetching"

@app.route('/lostinsert',methods = ['POST','GET'])
def lostinsert():
    if request.method == 'POST':
        image = request.files['img']
        name=request.form.get('itemN')
        wheres=request.form.get('itemL')
        description=request.form.get('des')
        filename = name + ".jpg"
        filename = os.path.join('static/images/lostfound/',filename)
        image.save(filename)
        
        
        # Creating Cursor
        cur=mydb.cursor()
        
        
        cur.execute("INSERT INTO lostfound(name,wheres,description) VALUES(%s,%s,%s)",(name,wheres,description))
        
        #Commit to db
        mydb.commit()
        
        #close Connection
        cur.close()
        
        return "Successfully added into the database"
    return render_template("lostFoundAdd.html")

@app.route('/home')
def homepage():
    return "This is homepage"

@app.route('/classifiedadd')
def classifiedadd():
    return "Classified Add"

@app.route('/classifiedFetch')
def classifiedfetch():
    return "classified Fetch"

#Articles
#study materials
#College Updates
#Student details


if __name__ == "__main__":
    app.secret_key='poorna1999'
    app.run(debug=True)