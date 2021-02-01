from flask import render_template,session,request,redirect,url_for,flash
from shop import app , db ,brcypt
from .forms import RegistrationForm,LoginForm,ContactForm,SellForm
from .models import User,Contact,Sell
import os
import smtplib
from shop.products.models import Addproduct,Brand,Category
from datetime import date
from datetime import datetime
from datetime import timedelta
from flask_login import LoginManager, login_required, login_user, logout_user




#session timeout handling

# Define Flask-login configuration 

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)


@app.route('/')
def landingpage():
    return redirect('admin')
@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    products=Addproduct.query.all()   
    return render_template('admin/index.html',title='Admin Page',products=products)



@app.route('/brands')
def brands():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html',title="Brand page",brands=brands)

@app.route('/category')
def category():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/brand.html',title="Brand page",categories=categories)





@app.route('/register', methods=['GET', 'POST'])

def register():
    form = RegistrationForm(request.form)
    if request.method=="POST" and form.validate():
        hash_password=brcypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data,username=form.username.data, email=form.email.data,
                   password=hash_password)
        db.session.add(user)
        db.session.commit()
        server= smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login("Sparematenoreply@gmail.com","Sparemate@123")

        message="Admin registration complete"
        emails=['androgeek123@gmail.com',form.email.data,'skarjigi98@gmail.com']
        server.sendmail("Sparematenoreply@gmail.com",emails,message)










        flash(f'Welcome {form.username.data} Thanks for registering.Please proceed with login','success')

        return redirect(url_for('login'))  
    return render_template('admin/register.html', form=form,title="Registeration pages")
# add routes for other forms

@app.route('/login',methods=['GET', 'POST'])
def login():
    form=LoginForm(request.form)
    if request.method=="POST" and form.validate():
        #verify credentials here
        user=User.query.filter_by(email=form.email.data).first()
        admins=["androgeek123@gmail.com","rishi2k10@gmail.com","kotianviraj07@gmail.com"]
        for i in form.email.data:
            if form.email.data not in admins:
                flash(f'Sorry! You are not registered as an admin.','danger')
                return redirect('login')
         

        if user and brcypt.check_password_hash(user.password,form.password.data):
            session['email']=form.email.data
            session.permanent = True
            #server= smtplib.SMTP("smtp.gmail.com",587)
            #server.starttls()
            #server.login("Sparematenoreply@gmail.com","Sparemate@123")
            #today = date.today()
           # now = datetime.now()
            #message=f'Admin login activity detected\n\nDetected Email:{form.email.data}\n\nLast login date:{today}\n\nLast login time:{now}\n\n\nThank You\nSpareMate login detection system\n\nAuto generated email,do not reply.'
           # emails=['androgeek123@gmail.com',form.email.data,'skarjigi98@gmail.com']
            #server.sendmail("Sparematenoreply@gmail.com",emails,message)
            flash(f'Welcome {form.email.data}','success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            #wrong password or email handling
           flash('Incorrect credentials,please check your credentials or signup to login!','danger')
    
    return render_template('admin/login.html',form=form,title='Login Page')

#logout functionality
@app.route('/logout')
def logout():
    session.pop('email',None)
    flash(f'You have logged out successfuly.','success')
    return redirect(url_for('login'))
    

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm(request.form)
    if request.method=="POST" and form.validate():
        con= Contact(name=form.name.data,email=form.email.data,subject=form.subject.data,message=form.message.data)
        db.session.add(con)
        db.session.commit()
        flash('Contact form has been filled','success')
        return redirect(request.args.get('next') or url_for('admin'))
    else:         
         return render_template('admin/contact.html',form=form,title='Contact Page')



           


 

    
   


 
  
      
       
       



   


