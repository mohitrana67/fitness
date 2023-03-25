from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from users.models import User as u
import json
import logging

# logging.basicConfig(filename="Logs/Users/users.log", level=logging.DEBUG,
#                         format='%(asctime)s:%(created)f:%(funcName)s:%(message)s')

from django.db.models import Q

@csrf_exempt
def createUser(request):
    data = {}
    message = ""
    status = 0
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        email = body["email"]
        username = body["username"]
        f_name = body["f_name"]
        l_name = body["l_name"]
        password = body["password"]
        # Now we will check if the email and username already exists
        try:
            if(u.objects.filter(Q(email=email)|Q(username=username))):
                message = f"User with email: {email} or username: {username} already exists!!! Email and username needs to be unique."
                status = 409
            else:
                try:
                    user = u.objects.create_user(
                        email=email,
                        username=username,
                        f_name=f_name,
                        l_name=l_name,
                        password=password
                    )
                    message = f"User Created with email {email}"
                    status = 200
                except Exception as e:
                    raise e
        except Exception as e:
            raise e
    else:
        status = 404
        message = "You are only authorized to POST into this link!"

    return JsonResponse({
        "Data": data,
        "Message": message,
        "Status": status
    })

@csrf_exempt
def login(request):
    message = ""
    data = {}
    status = 200
    logging.debug("We are going to attempt logging in a user!!")
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        email = body["email"]
        password = body["password"]
        # Check if email is in the system or not
        try:
            user_available = u.objects.get(email=email)
            try:
                user = authenticate(email=email, password=password)
                if user is not None:
                    # Here we need to create a token and pass it to the token table
                    try:
                        token = Token.objects.create(user=user)
                        status = 200
                        data["token"] = token.key
                        message = "You are logged in!!!"
                        log.debug(message)
                    except Exception as e:
                        token = Token.objects.get(user=user).key
                        status = 200
                        data["token"] = token
                        message = "You are already logged in!!!"
                    data["user_id"] = u.objects.get(email=email).id
                else:
                    status = 401
                    message = f"Please enter valid password for email {email}"
            except Exception as e:
                print(e)
                status = 401
        except Exception as e:
            status = 404
            message = f"User with email {email} not found! Please signup first!"
            print(e)
    else:
        message = "You are only entitled for POST request!"
        status = 404
    
    return JsonResponse({
        "Data": data,
        "Message": message,
        "Status": status
    })

@csrf_exempt
def listUsers(request):
    data = {}
    message = ""
    status = 0
    if request.method == "GET":
        users = u.objects.filter(is_active=True)
        print(users)
        for i in users:
            data[i.email]={
                "username":i.username,
                "f_name":i.f_name,
                "l_name":i.l_name,
                "superuser":i.is_superuser,
                "staff":i.is_staff
            }
    else:
        message = "You are only entitled to GET to this link!!!"
        status = 404

    return JsonResponse({
        "Data":data,
        "Message":message,
        "Status":status
    })

@csrf_exempt
def deleteUser(request,email_id):
    data = {}
    message = ""
    status = 0
    if request.method == "DELETE":
        try:
            user = u.objects.filter(email=email_id)
            if user:
                user.delete()
                message = "User deleted"
                status = 200
            else:
                message = "User not found"
                status = 404
        except Exception as e:
            raise e
    else:
        message = "You are only entitled to DELETE to this link!!!"
        status = 404
    
    return JsonResponse({
        "Data": data,
        "Message": message,
        "Status": status
    })

@csrf_exempt
def updateUser(request,email_id):
    data = {}
    message = ""
    status = 0
    if request.method == "PUT":
        try:
            user = u.objects.get(email=email_id)
        except Exception as e:
            raise e
    else:
        message = "You are only entitled to PUT to this link!!!"
        status = 404
    
    return JsonResponse({
        "Data":data,
        "Message":message,
        "Status":status
    })

@csrf_exempt
def logout(request):
    message = ""
    data = {}
    status = 200
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        headers = json.load(body_unicode)
        token = headers["token"]
        try:
            Token.objects.filter(key = token).delete()
            message = "User Logged out successfully!!"
            status = 404
        except Exception as e:
            print(f"Exception occured as {e}")
    else:
        message = "You are only entitled for POST request!"
        status = 404
    
    return JsonResponse({
        "Data": data,
        "Message": message,
        "Status": status
    })

@csrf_exempt
def getUser(request):
    message = ""
    data = {}
    status = 0
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        token = body["token"]
        try:
            user_id = Token.objects.get(key=token).user_id
            data["user_id"] = user_id
            message = "You fetched it correctly!"
            status = 200
        except Exception as e:
            message = "User not found"
            status = 400
            print(f"Exception occured as {e}")
    else:
        message = "You are only entitled for POST request!"
        status = 404
    
    return JsonResponse({
        "Data": data,
        "Message": message,
        "Status": status
    })