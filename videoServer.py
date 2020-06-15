from flask import Flask, render_template, request, flash, redirect, url_for, session,logging, jsonify
from Getdata import ArticlesOrigin
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField,PasswordField, validators
from passlib.hash import sha256_crypt
import json
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
import random
from flask_cors import CORS, cross_origin 
import csv
from os import environ, path, makedirs
from flask_bootstrap import Bootstrap

basedir = path.abspath(path.dirname(__file__))
currentPort = 8081

def determineAPI(arg):
  if arg == 'dev':
    return baseAPIDevelopment
  if arg == 'prod':
    return baseAPINgrok

baseAPINgrok = 'https://' + '38a34430ddd0' + '.ngrok.io'
baseAPIDevelopment = 'http://localhost:5000'
mode = 'dev' # = dev OR prod



###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################


#Change ENV HERE

baseAPI = determineAPI('prod')  # =<< ( 'dev' | 'prod' )


###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################

#MY imported modules
from forms import IntakeForm, RegisterForm


"""
ToDo: try serving the test-shit.html as raw html 
  to see if we can avoid webpack implementation for now

  Implement make_response object 

  Strip out forms -> Using bare XMLHTTPRequest 
   
      XHR -> HTTP Client Binary -> HTTP Server Binary -> Flask Request Object { filename :: Binary Data } >>= open(mode= 'wb') -> SAVED FILE


"""

app = Flask(__name__, instance_relative_config=False, static_folder="static", template_folder="templates")
app.config.from_object('config.Config')

app.config['CORS_ORIGINS'] = ['*'] 
app.config['CORS_HEADERS'] = ['Content-Type']
cors = CORS(app) #   , resources={r"/api/*": {"origins": "*"}})

Bootstrap(app)

#config mysql
#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = '12345'
#app.config['MYSQL_DB'] = 'myflaskapp'
#app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#init mysql
#mysql =MySQL(app)


# SS -> Email Form


@app.route('/form/', methods=['GET', 'POST'])
def first_form():
  form = RegisterForm()
  
  name = form.name.data
  email = form.email.data
  job_type = form.job_types.data #figure out how to do dropdown input in flask form then update to actual thing

  if form.validate_on_submit():
    with open(basedir + '/data/emails/users.csv', 'a') as f: 
      w = csv.writer(f)
      w.writerow([name, email, job_type])

      userdir = basedir + '/data/videos/' + email + '/'
      if not path.exists(userdir):
        makedirs(userdir)

    return redirect(baseAPI + '/recorder/' + email + '/' + job_type + '/')

  return render_template('emailForm.html', form=form)


@app.route('/recorder/<email>/<job_type>/', methods=['GET', 'POST']) #get rid of page use ;+ redirect to thank you page through JS
def video_html(email, job_type): #x is their email
  roleQuestions = getQuestions(job_type)
  generalQuestions = ["Tell me about yourself.",
             "What are your strengths and weaknesses?", 
             "Why do you want to work here? (Pick your ideal company)",
             "What interests you about this role?",
             "What motivates you?",
             "What are you passionate about?",
             "Why are you leaving your current job?",
             "What did you like most about your last position? Least?",
             "What is your teaching philosophy?",
             "What are your long-term goals?"]

  userdir = basedir + '/data/videos/' + email + '/'
  if not path.exists(userdir):
    makedirs(userdir)

  video_data_bytes = request.get_data()
  t = type(video_data_bytes)
  print(video_data_bytes[:100])
  with open(basedir + '/data/videos/'+ email +'/videofile' + str(random.randint(1,1000000)) + '.mp4', 'wb') as f: 
    f.write(video_data_bytes) 
    f.close()
      

    #redirect
    
    #return redirect('https://5206e506.ngrok.io/recorder/' + email + '/' + str(page) +'/')
        #serve page with next question

  #else: 
  #  print('test: case =2')
    
  #  return redirect(baseAPI + '/thankYouSooooooooooooooooooooooooooooooooooMuch/')
    
  
  return render_template('test-shit.html', email=email, base=baseAPI, generalQuestions=generalQuestions, job_type=job_type, roleQuestions=roleQuestions)


def getQuestions(job_type):
  questions = {
    "Software Developer": [
      "Tell me about a tough software development problem you've taken on, and how you solved it.",
      "What obstacles have you run into while working on a software project, and how did you deal with them?",
      "Are you working on a passion project? What is it?",
      "What is your favourite language, tool, or library to use and why?",
      "If you had to describe to someone your problem solving approach that you take when starting on a brand new problem what would you say?",
      "There was an article that a great developer can have the same effect as a team of 5 average developers. If you had to guess, how could that be?",
      "What started your interest in coding?",
      "Tell me about a time you worked through a communication issue when working with a stakeholder? (OR) : If you haven’t been a part of communicating with stakeholders, communication issues with project managers",
      "Tell me about a time when you learned something about coding from normal day-to-day life",
      "What is something you want to learn about? Doesn’t have to be coding focused"
      
    ],
    "Designer": [
      "As a Designer, sometimes you will be given a large scope of work upfront, how do you typically begin on a project?",
      "Do you have any sources of inspiration for your work? Who/what are they?",
      "Tell us about a time you had to communicate your knowledge of design to another profession",
      "When you’ve worked in a team before, how would you describe what your role ended up being? How did that complement the rest of the team?",
      "What is your favourite product ever? What is the first thing you would change about it?",
      "Walk me through the project that you most enjoyed working on and tell me why it’s important/would be important to its intended user",
      "If you were to ask the first question ever to your target user, what would you ask and why?"
    ],

    "Product Manager": [
      "How do your past roles, prior to product management, influence your perspective on what makes a great PM?",
      "What is your main priority at the start of a project?",
      "How would you explain Agile Project Management to someone who believes it is 'just being lazy about planning'"

    ],
    "Sales": [
      "Tell me about a time that you handled an objection from a customer, colleague, or boss",
      "Pick up the closest item to you (notebook, pen, paper, etc.) and sell it to me without selling it as the function it does (i.e. if you choose a pen, you can’t sell it to me as the best writing tool out there)",
      "Tell me about a time that you dealt with an unhappy customer",
      "What motivates you as a sales rep?"
    ],
    "Business Analyst":[
      "How would you deal with working with difficult stakeholders?",
      "What is the importance of analytical reporting?",
      "Walk me through how you would approach a new project.",
      "What tools do you think a business analyst should prioritize"

    ],
    "Management Consulting": [
      "How would you calculate how many traffic lights there are in Toronto, ON?",
      "What are your long-term goals?",
      "What do you do for fun?",
      "Tell me about a time when you had to solve a difficult problem? What was your process?",
      "How would you describe your leadership style?",

    ],
    "Finance": [
      "How would you calculate how many traffic lights there are in Toronto, ON?",
      "If you could only choose one profitability model to forecast for your projects, which would it be and why?",
      "Walk me through a time that you have used financial benchmarking.",
      "What financial methodologies are you familiar with for conducting an analysis?",
      "What components would you use to portray the financial health of your company to an investor?",
      "If you could choose one evaluation metric to use when reviewing company stock, which would it be and why?"
    
    ],
    "Marketing": [
      "What measures of success would you set for a marketing social media campaign?",
      "How would you describe our company brand?",
      "A customer left a negative review of our product on a social media site. How do you respond to the customer?",
      "Tell me about your favourite product. How would you market it?",
      "Tell me about a project you worked on where you had a team of people with different ideas from you. How did you manage the situation?",
      "You have been given a project to re-brand a product that has been performing poorly. How do you approach this?",
      "What are the three most important skills for a marketing career?"
    ],
    "Other": [] #keep empty
  }  
  roleSpecific = questions[job_type] 
  return roleSpecific

  


  

@app.route('/submit/<email>', methods = ['POST'])
def post(email):
  print(email)


   

    
    #serve the thank you page as a redirect
    #   plan is to redirect to linkedin, or back to squarespace
     

  #if request is JSON -> email
  #else -> is video
  #                     # fileField -> Data -> Do Stuff
  # if form.validate_on_submit():
    
  #   #video = request.form.get('video')

  #page_lookup_q = ['1. Tell me about yourself', '2. Tell me about a time you overcame an obstacle', '3. What are your strengths & weaknesses']
  #question = page_lookup_q[int(page)-1]


#  video_data_bytes = request.get_data()
 # t = type(video_data_bytes)
 # print(t)
  #with open(basedir + '/data/videos/'+ email +'/videofile' + str(random.randint(1,1000000)) + '.mp4', 'wb') as f: 
  #  f.write(video_data_bytes)
  #  f.close()
  #  return redirect('https://5206e506.ngrok.io/recorder/' + email + '/' + str(page + 1) +'/')

    #return thank you page

  

  
@app.route('/thankYouSooooooooooooooooooooooooooooooooooMuch/', methods=['GET'])
def thank_you():
  print(' I WAS CALLED ')
  return render_template('thank_you.html')

#def thank you page!!

if __name__ == "__main__":
  app.secret_key='secret123'
  app.run(host="localhost", port=currentPort, debug=False)
  

























#Articles = ArticlesOrigin()


# @app.route('/getRecorder')
# def index():
#   return render_template('home.html') #can add server-held data 
#   #return render_template('data_blocks.html')

#@app.route('/articles')
#def articlesGet():
#  return render_template('articles.html', articles=Articles)


# @app.route('/article/<string:id>/') #so you declare the type then the variable namespace eg id
# def article(id):
#   return render_template('article.html', id=id)


  
#@app.route('/register', methods=['GET','POST'])
#def register():
#  form = RegisterForm(request.form)
  #write_to_file
#  if request.method == 'POST' and form.validate():
 #   
  #  name = form.name.data 
   # email = form.email.data
    #username = form.username.data
    #password = sha256_crypt(str(form.password.data))
    
    #data = [name, email, username]
  
    #csv_writer = csv.writer("datafile.csv")
    #csv_writer.writerow(data)


    #print(form)
    
    #cur = mysql.connection.cursor()
    #insert the form data into the DB
    #cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))
    #mysql.connection.commit()
    #cur.close()
    
    #flash('You are now registered and can login', 'success') # recomment once you know how this works for real
    #redirect(url_for('index'))
    
    
    #return redirect(url_for('login'))
  #return render_template('register.html', form=form)
  
  
#class RegisterVideoForm(Form):
#  email = StringField('Name', [validators.length(min=1, max=50)])
#  video = FileField('Video', validators=[FileRequired()])


































#@app.route('/')
#@cross_origin()
#def giveVideoForm():
#  form = RegisterVideoForm(request.form)
#  if request.method == 'POST' and form.validate():
#    video = form.video.data
#    email = form.email.data
#    
#    filepath = "/home/galensprout/Desktop/" + email + "/" + str(random.randint(1,100000000))
#    
#  return render_template('videoForm.html', form=form)
  
  
# @app.route('/videoSubmit', methods=['POST'])
# def videoIntake():
#   data = reqObj.POST
#   video_data = request.files
#     #check if 'Content-Type' is too
    
  
# property files

#     MultiDict object containing all uploaded files. Each key in files is the name from the <input type="file" name="">. 
#     Each value in files is a Werkzeug FileStorage object.
#     It basically behaves like a standard file object you know from Python, with the difference that it also has a save() 
#     function that can store the file on the filesystem.
#     Note that files will only contain data if the request method was POST, PUT or PATCH and the <form> that posted to the 
#     request had enctype="multipart/form-data". It will be empty otherwise.
#     See the MultiDict / FileStorage documentation for more details about the used data structure.
    
#Form for files on front end     
    
    
    
    
#@app.route('/api')
#@cross_origin()
#def api():
##
#   form = RegisterVideoForm(request.form)
#  return render_template('videoForm.html', form=form)#jsonify({'data': 'this is working! just not for video'})
    
    


    
    
    
    
    
    
  


  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
   
  
  
  
  
  
  
