from django.shortcuts import render, redirect
from .models import Users
from django.contrib import messages

# Create your views here.
def index(request):
	return render(request, 'registration/index.html')

def register(request):
	result = Users.loginmgr.register(request.POST['first'], request.POST['last'], request.POST['email'], request.POST['passw'], request.POST['confirm'])
	if result[0]:
		request.session['name'] = result[1].first_name
		return redirect('/success')
	else:
		for error in result[1]:
			messages.error(request, error)
	return redirect('/')

def login(request):
	result = Users.loginmgr.login(request.POST['mail'], request.POST['password'])
	if result[0]:
		request.session['name'] = result[1].first_name
		return redirect('/success')
	else:
		for error in result[1]:
			messages.error(request, error)
	return redirect('/')

def success(request):
	return render(request, 'registration/success.html')