from flask import Flask,render_template,flash,url_for,redirect,session,logging,request
import mysql.connector
from functools import wraps
import os
from wtforms import Form,StringField,TextAreaField,PasswordField,validators


app = Flask(__name__)


#Config Mysql
mydb=mysql.connector.connect(host='localhost',user="root",passwd="",database="techbytes")


@app.route('/')
def home():
    return render_template("main.html")

@app.route('/add_study',methods=['POST','GET'])
def addstudy():
    if request.method == 'POST':
        cont = request.form.get('usn')
        sub = request.form.get('pass')
        link = request.form.get('password')
    # Creating Cursor
        cur=mydb.cursor()
        
        
        cur.execute("INSERT INTO study(contributors,subject,link) VALUES(%s,%s,%s)",(cont,sub,link))
        
        #Commit to db
        mydb.commit()
        
        #close Connection
        cur.close()
        return render_template('main.html')    
        
    return render_template('add_study.html')

#hello this is navya
# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap
    
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

#Login page
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        #Geeting the form field
        usn=request.form.get('usn')
        password_candidate=request.form.get('pass')
        
        #Create Cursor
        cur=mydb.cursor(buffered=True)

        #Get user by username
        
        result=cur.execute("select * from auth where usn = %s",[usn])
        
        if result == None:
            #Getting the stored hashed
            data=cur.fetchone()
            password=data[3]
            #Comparing the password
            if password_candidate==password:
                session['logged_in']=True
                session['usn']=usn
                flash("Congrats you are logged in")
                return redirect('/')
                app.logger.info('Password Matched')
                # return "success"
                
            else:
                app.logger.info("Password not matched")
                error="Invalid login"
                flash("password not matched")
                return render_template('login.html',error=error)
                
            #Close connection
            cur.close()
        else:
            app.logger.info("No User")
            flash("No user found")
            # return render_template('login.html',error=error)
            return "it didnt check password"
    return render_template('login.html')


#Fetch Profile on one screen
@app.route('/classifiedfetch')
@is_logged_in
def fetch_profile():
    cur=mydb.cursor()
    cur.execute('SELECT * FROM classified')
    profiles=cur.fetchall()
    
    return render_template('classifiedfetch.html',profiles=profiles)  
    cur.close()


# @app.route('/lostFetch')
# def lostFetch():
#     return "Hello!!! this is Lost and found fetching"

@app.route('/lostinsert',methods = ['POST','GET'])
@is_logged_in
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

#lost and found fetchging
@app.route('/lostfoundfetch')
@is_logged_in
def lostfoundfetch():
    cur=mydb.cursor()
    cur.execute('SELECT * FROM lostfound')
    profiles=cur.fetchall()
    return render_template('lostFoundFetch.html',profile=profiles)

#Study Materials fetch
@app.route('/studyfetch')
@is_logged_in
def studyfetch():
    cur=mydb.cursor()
    cur.execute('SELECT * FROM study')
    profiles=cur.fetchall()
    return render_template('fetch_study.html',profile=profiles)

@app.route('/classifiedadd',methods=['POST','GET'])
@is_logged_in
def classifiedadd():
    if request.method == 'POST':
        image = request.files['img']
        user=session['usn']
        title=request.form.get('itemN')
        category=request.form.get('itemL')
        description=request.form.get('des')
        filename = user + ".jpg"
        filename = os.path.join('static/images/classified/',filename)
        image.save(filename)
        
        
        # Creating Cursor
        cur=mydb.cursor()
        
        
        cur.execute("INSERT INTO classified(user,title,category,description) VALUES(%s,%s,%s,%s)",(user,title,category,description))
        
        #Commit to db
        mydb.commit()
        
        #close Connection
        cur.close()
        
        return "Successfully added into the database"
    return render_template("classifiedadd.html")

@app.route('/classifiedFetch')
@is_logged_in
def classifiedfetch():
    cur=mydb.cursor()
    cur.execute('SELECT * FROM classified')
    profiles=cur.fetchall()
    return render_template('classifiedfetch.html',profile=profiles)

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
@is_logged_in
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
        
        return redirect('/dashboard')
    return render_template('add_article.html',form=form)

#Articles fetch page    
@app.route('/articles')
@is_logged_in
def articles():
    cur=mydb.cursor()
    #Get Articles
    result= cur.execute('SELECT * FROM articles')
    
    articles=cur.fetchall()
    # if result > 0:
    #     return render_template('dashboard.html', articles=articles)
    # else:
    #     msg = 'No Articles Found'
    #     return render_template('dashboard.html', msg=msg)
        
    
    return render_template('articles.html',articles=articles)  
    #Close Connection
    cur.close()  


#Editing articles    
@app.route('/edit_article/<string:id>',methods=['POST','GET'])
@is_logged_in
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

#Fetching particular article
@app.route('/article/<string:id>')
@is_logged_in
def article(id):
    cur = mydb.cursor()
    
    # Get article
    
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])

    article = cur.fetchall()

    return render_template('article.html', article=article)
    cur.close()



#Users dashboard
@app.route('/dashboard')
@is_logged_in
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
@is_logged_in
def delete_article(id):
    #Creating cursor
    cur = mydb.cursor()
    
    #Execute cursor
    cur.execute("DELETE FROM articles WHERE id=%s",[id])
    
    mydb.commit()
    
    cur.close()
    
    flash('Article Deleted','success')
    
    return redirect('/dashboard')

#Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash("Successfully Logged out!!!")
    return redirect('/login')
          

if __name__ == "__main__":
    app.secret_key='poorna1999'
    app.run(debug=True)