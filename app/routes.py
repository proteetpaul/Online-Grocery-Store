from flask import render_template, redirect, url_for, flash, request, session
import sqlalchemy
from sqlalchemy import func
from sqlalchemy import text
from app import app
from app import db

from app.forms import LoginForm, RegistrationForm, Consumer_Registration_Form, Manager_Registration_Form, Agent_Registration_Form, SearchForm
from app.models import Consumer, Manager, Delivery_agent
from flask_login import current_user,login_user, logout_user, login_required
from werkzeug.urls import url_parse

@app.route('/home')
@login_required
def home():
	return render_template('home.html',title='home')

@app.route('/login',methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form=LoginForm()
	if form.validate_on_submit():
		user=Consumer.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))

		session['username']=user.username
		session['user_type']='Consumer'
		login_user(user)
		flash('User successfully logged in')
		next_page=request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('home')
		return redirect(next_page)
	return render_template('login.html',title='Sign In',form=form)

@app.route('/logout')
def logout():
	print(session['username'])
	logout_user()
	session.pop('username',None)
	session.pop('user_type',None)
	return redirect(url_for('login'))

@app.route('/register_consumer', methods=['GET', 'POST'])
def register_consumer():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form=Consumer_Registration_Form()
	if form.validate_on_submit():
		# cid, username, email, password_hash, address, city_id, phone_no
		user = Consumer(username=form.username.data, email=form.email.data, 
						address=form.address.data, city_id=form.city_id.data, phone_no=form.phone_no.data)
		user.set_password(form.password.data)
		count=db.session.query(func.count('*')).select_from(Consumer).scalar()
		user.cid=count+1
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered consumer!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route('/register_manager', methods=['GET', 'POST'])
def register_manager():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form=Manager_Registration_Form()
	if form.validate_on_submit():
		# cid, username, email, password_hash, brand
		user = Manager(username=form.username.data, email=form.email.data, brand=form.brand.data)
		user.set_password(form.password.data)
		count=db.session.query(func.count('*')).select_from(Manager).scalar()
		user.manager_id=count+1
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered manager!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route('/register_agent', methods=['GET', 'POST'])
def register_agent():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form=Agent_Registration_Form()
	if form.validate_on_submit():
		# cid, username, email, password_hash, city_id
		user = Delivery_agent(username=form.username.data, email=form.email.data, city_id=form.city_id.data)
		user.set_password(form.password.data)
		count=db.session.query(func.count('*')).select_from(Delivery_agent).scalar()
		user.agent_id=count+1
		user.pending_deliveries=0
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered delivery agent!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

