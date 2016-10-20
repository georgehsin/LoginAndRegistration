from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
name_regex = re.compile(r'^[A-Za-z]{2}')
password_regex = re.compile(r'^.{8}')
# Create your models here.
class LoginManager(models.Manager):
	def register(self, first_name, last_name, email, passw, confirm):
		errors = []
		if not name_regex.match(first_name):
			errors.append('first name must be no fewer than 2 characters and letters only')
		if not name_regex.match(last_name):
			errors.append('last name must be no fewer than 2 characters and letters only')
		if not EMAIL_REGEX.match(email):
			errors.append('valid email required')
		if not password_regex.match(passw):
			errors.append('password must be no fewer than 8 characters')
		if passw != confirm:
			errors.append('passwords must match')
		if len(errors) != 0:
			return (False, errors)
		else:
			passw = passw.encode()
			hashed = bcrypt.hashpw(passw, bcrypt.gensalt())
			e = Users.loginmgr.create(first_name = first_name, last_name = last_name, email = email, password = hashed)
			e.save()
			return (True, e)
	def login(self, mail, password):
		errors = []
		try:
			result = Users.loginmgr.get(email = mail)
		except:
			errors.append('please enter a valid email address')
			return (False, errors)
		if not bcrypt.hashpw(password.encode(), result.password.encode()) == result.password.encode():
			errors.append('password is incorrect')
			return (False, errors)
		return (True, result)

class Users(models.Model):
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	loginmgr = LoginManager()