from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, TextField, SelectField #, FileField
from wtforms.validators import (DataRequired, Email, EqualTo, Length, URL) 

jobList = [
  ('Designer', 'Designer'),  
  ('Software Developer', 'Software Developer'),
  #('Data Science', 'Data Science'),
  #('Civil Engineering', 'Civil Engineering'),
  #('Biomedical Engineering', 'Biomedical Engineering'),
  #('Chemical Engineering', 'Chemical Engineering'),
  ('Sales', 'Sales'),
  #('Communications', 'Communications'),
  ('Business Analyst', 'Business Analyst'),
  #('Accounting', 'Accounting'),
  #('Human Resources', 'Human Resources'),
  #('Legal', 'Legal'),
  #('Educational', 'Educational'),
  ('Management Consulting', 'Management Consulting'),
  ('Finance', 'Finance'),
  ('Marketing', 'Marketing'),
  ('Other', 'Other')
]

class IntakeForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    email = StringField('Email', [DataRequired()])
    email2 = StringField('Email', [DataRequired()])
    body = TextField('Message', [DataRequired(), Length(min=4, message=('Your message is too short'))])
    #recaptcha = ReCaptchaField()
    video = FileField('Video File')
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
  name = StringField('Name', [Length(min=1,max=50)])
  #username = StringField('Username', [Length(min=4, max=25)])
  email = StringField('Email',[Length(min=6, max=50)])
  job_types = SelectField(label='Job Type', choices=jobList)
  submit = SubmitField('Submit')
  #password = PasswordField('Password', [
  #    validators.DataRequired(),
  #    validators.EqualTo('confirm', message='Passwords do not match')
  #  ])
  #confirm = PasswordField('Confirm Password')
  


