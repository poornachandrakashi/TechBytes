from flask import Flask,render_template,flash,url_for,redirect,session,logging,request
import mysql.connector
from functools import wraps
#from passlib.hash import sha256_crypt
import os

from wtforms import Form,StringField,TextAreaField,PasswordField,validators


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



# @app.route('/lostFetch')
# def lostFetch():
#     return "Hello!!! this is Lost and found fetching"

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


@app.route('/classifiedadd',methods=['POST','GET'])
def classifiedadd():
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
        
        
        cur.execute("INSERT INTO classified(name,wheres,description) VALUES(%s,%s,%s)",(name,wheres,description))
        
        #Commit to db
        mydb.commit()
        
        #close Connection
        cur.close()
        
        return "Successfully added into the database"
    return render_template("classifiedadd.html")

@app.route('/classifiedFetch')
def classifiedfetch():
    return "classified Fetch"

#Articles
#study materials
#College Updates
#Student details


#Article validation
class ArticleForm(Form):
    title = StringField('title', [validators.Length(min=1, max=2000)])
    body = TextAreaField('body', render_kw={'rows':20})
    
#Adding articles    
@app.route('/add_article',methods=['POST','GET'])
def add_article():
    form=ArticleForm(request.form)
    if request.method=='POST' and form.validate():
        title = form.title.data
        body = form.body.data
        image = request.files['img']
        # ts = time.gmtime()
        name=session['usn']
        # uploadtime = time.strftime("%Y%m%d%H%M%S", ts)
        filename = "image" + title + ".jpg"
        filename = os.path.join('static/images/articles/',filename)
    # app.logger.info("File to upload: ")
    # app.logger.info(filename)
        image.save(filename)
        
        #Create cursor
        cur=mydb.cursor()
        
        #Execute
        cur.execute("INSERT INTO articles(title,body,author) VALUES(%s,%s,%s)",(title,body,session["usn"]))
        #commit
        mydb.commit()
        
        #close connection
        cur.close()
        
        flash('Article Created','Success')
        
        return "Article added!!!"
    return render_template('add_article.html',form=form)

#Editing articles    
@app.route('/edit_article/<string:id>',methods=['POST','GET'])
def edit_article(id):
    
    #Create Cursor
    cur=mydb.cursor()
    
    #Get article by id
    result=cur.execute("SELECT * FROM articles WHERE id = %s", [id])
    
    article = cur.fetchall()
    
    cur.close()
    
    
    
    form=ArticleForm(request.form)
    
    #Populate the article
    form.title.data = article['title']
    form.body.data = article['body']
    
    if request.method=='POST' and form.validate():
        title=request.form['title']
        body=request.form['body']
        
        #Create cursor
        cur=mydb.cursor()
        
        #Execute
        cur.execute("UPDATE articles SET title=%s, body=%s WHERE id=%s",(title, body, id))
        #commit
        mydb.commit()
        
        #close connection
        cur.close()
        
        flash('Article Updated','Success')
        
        return "Article Edited"
    return render_template('edit_article.html',form=form)


#Users dashboard
@app.route('/dashboard')
def dashboard():
    #Create cursor
    
    cur=mydb.cursor()
    #Get Articles
    result= cur.execute('SELECT * FROM articles WHERE author="{}"'.format(session['usn']))
    
    articles=cur.fetchall()
    # if result > 0:
    #     return render_template('dashboard.html', articles=articles)
    # else:
    #     msg = 'No Articles Found'
    #     return render_template('dashboard.html', msg=msg)
        
    
    return render_template('dashboard.html',articles=articles)  
    #Close Connection
    cur.close()  

#Delete Article
@app.route('/delete_article/<string:id>',methods=['POST'])
def delete_article(id):
    #Creating cursor
    cur = mydb.cursor()
    
    #Execute cursor
    cur.execute("DELETE FROM articles WHERE id=%s",[id])
    
    mydb.commit()
    
    cur.close()
    
    flash('Article Deleted','success')
    
    return redirect('/dashboard')
          

if __name__ == "__main__":
    app.secret_key='poorna1999'
    app.run(debug=True)