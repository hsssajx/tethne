
"""
    This script contains various methods (views of a webpage) in relation to User Login, creating datasets
    and viewving the dataset details.
    
    views ( methods)
    ```````
    /login        - Login check
    /register     - register a new user.
    
    .. autosummary::
    
    login
    register
    ....
    ....
    
    """


# Import Statements   
from flask import Flask, session, redirect, url_for, escape, request,render_template,flash
from flask_wtf import Form
from forms import LoginForm,RegisterForm,ForgotForm,GenerateDataSetsForm
import ZODB.config
import transaction
from hashlib import sha256 # for password
from persistent import Persistent
from persistent.list import PersistentList as List
from persistent.mapping import PersistentMapping as Dict
#from flask_login import current_user,login_user,LoginManager,logout_user , \
#                     current_user , login_required
from flask import abort
import json
import subprocess,os
import datetime
import logging
from logging import Formatter, FileHandler


# Initializing the application
app = Flask(__name__)
app.config.from_object('config')
app.debug = True

from ZODB.FileStorage import FileStorage
from ZODB.DB import DB
import models as mod                    #calling the DB Script


@app.before_first_request
def set_db_defaults():
    
    """
    This is to be called only once during the script.
    Setting the ZODB databases. 
    
    """
    storage = FileStorage('./storage/userdb.fs')
    conn = DB(storage)
    #print "3.Login start:",conn, type(conn),
    dbroot = conn.open().root()
    try:
        for val in ['userdb','graphdb','datadb','dsdb']:
            if val in dbroot.keys():
                pass
    except:
        if not val in dbroot.keys():
            print " donot create this always"
            dbroot[val] = Dict()
            print "TRY user db dbroot:",dbroot['dsdb'], type (dbroot['dsdb'])

        
def get_user_details():
    storage = FileStorage('./storage/userdb.fs')
    conn = DB(storage)
    #print "Get User Deatails:",conn, type(conn),
    dbroot = conn.open().root() 
    columns = [ 'S.No', 'User Name', 'Institution', 'Email ID'] 
    results = []
    abc = [('1',dbroot['userdb'][key].name,dbroot['userdb'][key].id, dbroot['userdb'][key].institution) for key in dbroot['userdb'].keys()]
    #remove unicode characters
    new_list =[','.join(list(each_item)) for each_item in abc]
    unicode_removed_list = [n.encode('ascii','ignore') for n in new_list]
    for val1 in unicode_removed_list:
        each_list = val1.split(',') 
        results.append(each_list)
    return results
     

def del_user_details():
    storage = FileStorage('./storage/userdb.fs')
    conn = DB(storage)
    #print "Get User Deatails:",conn, type(conn),
    dbroot = conn.open().root() 
    
def update_user_details():
    """
    Convert aulast, auinit, and jtitle into the fuzzy identifier ayjid
    Returns 'Unknown paper' if all id components are missing (None).

    Parameters
    ----------
    Kwargs : dict
        A dictionary of keyword arguments.
    aulast : string
        Author surname.
    auinit: string
        Author initial(s).
    date : string
        Four-digit year.
    jtitle : string
        Title of the journal.

    Returns
    -------
    ayj : string
        Fuzzy identifier ayjid, or 'Unknown paper' if all id components are
        missing (None).
    """
    storage = FileStorage('./storage/userdb.fs')
    conn = DB(storage)
    #print "Get User Deatails:",conn, type(conn),
    dbroot = conn.open().root() 
    return results 
    #return json.dumps(results)   



@app.route('/auth', methods=['GET','POST'])
def auth():
    print "comes in auth"
    #print session
    if session is None:
        flash ( "Please Login First!!!!!")
        return redirect(url_for("login"))
    if session['username'] is None:
         flash ( "Please Login First!!")
         return redirect(url_for("login"))
    if session['username'] != 'admin':
        flash ("Only Admins can view this page!!")
        return redirect(url_for('user'))

     
@app.route('/index', methods=['GET','POST'])
def index():
    if 'username' in session:
        print " comes here in index", session, type(session) 
        return 'Logged in as %s' % escape(session['username'])
    #return render_template('forms/register.html', form = form)
    return 'You are not logged in'            
    
@app.route('/ok', methods=['GET','POST'])
def ok():
    #form = LoginForm(request.form)
    #return redirect(url_for('login'))
    return render_template('pages/placeholder.home.html')
               
@app.route('/admin', methods=['GET','POST'])
def admin():
    if session['username'] != 'admin':
        flash ("Only Admins can view this page!!")
        return redirect(url_for('user'))
 
    #redirect(url_for("auth"))       
    
    if request.method == 'GET'  : #and name != None
        columns = [ 'S.No', 'User Name', 'Institution', 'Email ID']
        results =get_user_details()
           #results = json.dumps(user_details)
           #print "results:", results
    return render_template('pages/admin.home.html', columns=columns,results=results)
    return 'Hello World!'
    
@app.route('/user_data')
def get_user_data():
    
        print "comes here"
        print " session can be accessed here as well", session, session['username']
        columns = [ 'S.No', 'User Name', 'Institution', 'Email ID']
        results =get_user_details()
        return results
               
@app.route('/user', methods=['GET','POST'])
def user():
    print " session can be accessed here as well", session, session['username']
    return render_template('pages/user.home.html', user = session['username'])
               
@app.route('/place', methods=['GET','POST'])
def place():
    print "Are u coming here or not?" 
    return render_template('pages/placeholder.home.html')

@app.route('/', methods=['GET','POST'])
def home():
    return redirect(url_for('login'))

# Loader callback. Reload the user-id from the value stored in the session.
@login_manager.user_loader
def load_user(userid):
    #here use the ZODB user class and returns the user object
    pass


# TRY WITH GET. the perfect method
@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'GET'  : #and name != None
        #form = LoginForm(request.form)
        return render_template('forms/login_new.html')
        print " Its coming out"
    try:
        username = request.form['username']
        password = request.form['password']
    except:
        print "comes to except"
        pass
    print "comes out", request.form , "uname", username , "pass", password, type(password)
    #if form.validate():
    if 1:
          #new
          name = username
          session['username'] = username
          userpassword = password 
          #new
          print "Session",session, session['username']
          storage = FileStorage('./storage/userdb.fs')
          conn = DB(storage)
          print "3.Login start:",conn, type(conn),
          dbroot = conn.open().root()
          try: 
              print "####values()", dbroot['userdb'].values(), "#####keys",dbroot['userdb'].keys(), type(dbroot['userdb'])
              if name in dbroot['userdb'].keys():
                  for key in dbroot['userdb'].keys():
                      if key == 'admin' and name == 'admin':
                                  # Need to get username from the form  password = sha256(password
                                  dbpswd = dbroot['userdb'][key].password
                                  loginpswd = sha256(userpassword).hexdigest()
                                  if dbpswd == loginpswd:                                 
                                      #return render_template('pages/admin.home.html')
                                      return redirect(url_for('admin'))
                                  else:
                                      flash("Login Failed : Please provide the correct Username / password") 
                                      return redirect(url_for('login'))
                                 
                                  
                      if key != 'admin' and name != 'admin':
                                 if name == key:
                                  # Need to get username from the form  password = sha256(password
                                  dbpswd = dbroot['userdb'][key].password
                                  loginpswd = sha256(userpassword).hexdigest()
                                  if dbpswd == loginpswd:                                 
                                      #return render_template('pages/user.home.html')
                                      return redirect(url_for('user'))
                                  else:
                                      flash("Login Failed : Please provide the correct Username / password") 
                                      return redirect(url_for('login'))
                                
                      else:
                          print "No such user"
                          pass
              else:       
                      #render_template('pages/user.error.html')
                  flash("User, Please register First !!") 
                  return redirect(url_for('login'))       
          except:
              print " donot come here : except"
              pass           
                     

    return redirect(url_for('login'))
            
#return render_template('forms/login.html', form = form)


def generate_user_list(template_name, **kwargs):
    user_count = get_user_count()
    return render_template(template_name, uc = usercount, var2=var2, var3=var3, **kwargs)
    
@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    #print "##form OBJECT::: register---->", form, request.form,
    if request.method == 'POST':
            #session['username'] = request.form['username']
#                 if 'Register' in request.form:
#                     print "inside if"
#                 else:
#                     print "inside else"
        storage = FileStorage('./storage/userdb.fs')
        conn = DB(storage)
        print "Type start:",conn, type(conn)
        dbroot = conn.open().root()
        #db()   # to check if the DB is already initialized
        # this part is commented as it is moved up in db()
        try:
            for val in ['userdb','graphdb','datadb','dsdb']:
                if val in dbroot.keys():
                    pass
        except:
                if not val in dbroot.keys():
                    print " donot create this always"
                    dbroot[val] = Dict()
                    print "TRY user db dbroot:",dbroot['userdb'], type (dbroot['userdb'])
        
        print "else:::::-->", request.form , form.email.data
        u=mod.User(form.name.data,form.email.data,\
                    sha256(form.password.data).hexdigest(), \
                    form.password.data,form.institution.data,\
                    form.security_question.data, form.security_answer.data        
                   )
        print "User:--->", u, "form.name.data",form.name.data
        dbroot['userdb'][u.name] = u
        session['username'] = u.name
        transaction.commit()
        print "Database added successfully", dbroot['userdb'][u.name], u.name, u
        flash('Registered successfuly')
        return redirect(url_for('login'))
    return render_template('forms/register.html', form = form)

@app.route('/forgot',methods=['GET','POST'])
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form = form)    


@app.route('/create_datasets/', methods = ['GET','POST'])
def create_datasets():
    """
    Create Data Collection
    """
    form = GenerateDataSetsForm(request.form)
    user = session['username']
    if request.method == 'POST'  :
        try:
            input_type = request.form['filetype']
            input_path = request.form['fileinput']
           
        except:
            print "comes to except"
            pass
        print " comes out here"
        print "comes out create data", request.form, request.form['filetype'],request.form['fileinput']
    
        #status = os.system("python ../tethne -I example_data -O ./ --read-file  -P  /Users/ramki/tethne/testsuite/testin/2_testrecords.txt -F WOS | tee datasets_log.txt")
        status = os.system("python ../tethne -I " + session['username'] + " -O ./ --read-file  -P  /Users/ramki/tethne/testsuite/testin/2_testrecords.txt -F " + input_type + "| tee datasets_log.txt")
        #status = os.system("python ../tethne -I " + session['username'] + " -O ./ --read-file  -P " + input_path + " -F " + input_type + "| tee datasets_log.txt")
        print "try", status
        print os.getcwd()
        # Check if the command succeeded.
        if status is 0:
           log = "Dataset created successfully."
        else:
           log = "There seems to be some error while creating datasets."

        # Read the log file line by line and display it in the webpage.
        cmd  = 'cat datasets_log.txt'
        cmd2 = os.popen(cmd,'r',1)
        log=""
        for file in cmd2.readlines():     
             log +=file
             if file in "pickle":
                print "inside",file

        #Initialize the DB
    
        storage = FileStorage('./storage/userdb.fs')
        conn = DB(storage)
        print "3.Login start:",conn, type(conn),
        dbroot = conn.open().root()
        if not dbroot.has_key('dsdb'):
            dbroot['dsdb'] = Dict()
    
        #db() # call to check dsdb is initialized - this is not working
                
        # Add it to the DB
        dataobj=mod.DataCollection(session['username'],"samplepickleobject",datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        print "DS:--->", dataobj
        dbroot['dsdb'][dataobj.user_id] = dataobj
        transaction.commit()
        print "Database added successfully", dbroot['dsdb'][dataobj.user_id].date
    


    
        return render_template('pages/generate.datasets.html', user = user, text= log)
    
    return render_template('pages/generate.datasets.html', user = user, form= form)


@app.route('/create_slices/', methods = ['GET','POST'])
def create_slices():
    """
    Create datasets slices
    """
    form = GenerateDataSetsForm(request.form)
    user = session['username']
    if request.method == 'POST'  :
        try:
            input_type = request.form['filetype']
            input_path = request.form['fileinput']
        
        except:
            print "comes to except"
            pass
        print " comes out here"
        print "comes out create data", request.form, request.form['filetype'],request.form['fileinput']
        
        #status = os.system("python ../tethne -I example_data -O ./ --read-file  -P  /Users/ramki/tethne/testsuite/testin/2_testrecords.txt -F WOS | tee datasets_log.txt")
        status = os.system("python ../tethne -I " + session['username'] + " -O ./ --read-file  -P  /Users/ramki/tethne/testsuite/testin/2_testrecords.txt -F " + input_type + "| tee datasets_log.txt")
        #status = os.system("python ../tethne -I " + session['username'] + " -O ./ --read-file  -P " + input_path + " -F " + input_type + "| tee datasets_log.txt")
        print "try", status
        print os.getcwd()
        # Check if the command succeeded.
        if status is 0:
            log = "Dataset created successfully."
        else:
            log = "There seems to be some error while creating datasets."
        
        # Read the log file line by line and display it in the webpage.
        cmd  = 'cat datasets_log.txt'
        cmd2 = os.popen(cmd,'r',1)
        log=""
        for file in cmd2.readlines():
            log +=file
            if file in "pickle":
                print "inside",file

        #Initialize the DB
        
        storage = FileStorage('./storage/userdb.fs')
        conn = DB(storage)
        print "3.Login start:",conn, type(conn),
        dbroot = conn.open().root()
        if not dbroot.has_key('dsdb'):
            dbroot['dsdb'] = Dict()

        #db() # call to check dsdb is initialized - this is not working

        # Add it to the DB
        dataobj=mod.DataCollection(session['username'],"samplepickleobject",datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        print "DS:--->", dataobj
        dbroot['dsdb'][dataobj.user_id] = dataobj
        transaction.commit()
        print "Database added successfully", dbroot['dsdb'][dataobj.user_id].date

        return render_template('pages/generate.datasets.slices.html', user = user, text= log)

    return render_template('pages/generate.datasets.slices.html', user = user, form= form)




@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You are logged out')
    return redirect(url_for('login'))

# Error handlers.
@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500

@app.errorhandler(404)
def internal_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')



# Default port:
if __name__ == '__main__':
    #app.before_first_request()
    app.run()
    

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
