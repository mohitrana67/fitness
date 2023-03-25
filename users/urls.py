from django.urls import path
from users.views import (createUser as cu, listUsers as lu, deleteUser as du, login as lg, getUser as gu)

urlpatterns = [
    path('create_user/',cu, name="createUser"),
    path('list_users/',lu, name="listUsers"),
    path('delete_user/<str:email_id>/',du, name="listUsers"),
    path('login/',lg,name="login"),
    path('get_user/',gu,name="getUser"),
]