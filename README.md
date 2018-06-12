LineBot using Django
=================

This repository was intentionally created for FUKI ITForce 2017 Internships Training

Supporting files: https://drive.google.com/drive/folders/0B2H2u3aQBNoYUUpOUmNFOXVpODg

Reference:
- https://github.com/Lee-W/line_echobot
- https://developers.line.me/en/docs/messaging-api/reference/

Contents
-----------
- [Required Knowledge](#required-knowledge)
- [Pre-Requisite](#pre-requisite)
- [Integration with Git](#integration-with-git)
- [Create Django Project](#create-django-project)
- [Create Django App](#create-django-app)
- [Deploy to server](#deploy-to-server)
- [Integration with Line Developer Channel](#integration-with-line-developer-channel)
- [Handle Messaging API Request](#handle-messaging-api-request)
- [Have Fun!](#have-fun)

Required Knowledge
---------------------
Only need **basic python** (including OOP) and **basic git** skills. You can learn the other things while you're doing this tutorial, or even after it.

Pre-Requisite
------------------
In this tutorial, you will deploy your bot webhook to heroku server and use GitLab CI/CD to automate the deployment process. You can use other server or deployment process if you want to

So basically you have to:
- Create [GitLab](https://gitlab.com) account
- Create [LINE Developers](https://developers.line.me) channel
- Create [Heroku](https://dashboard.heroku.com) app

Integration with Git
-------------------------
- Create project (online repository) on GitLab
- Clone the repository to your local computer
```
git clone https://gitlab.com/<user_name>/<repository_name>.git
cd <repository_name>
touch README.md // or create new file on windows
                  // copy `.gitignore` to your folder
git add README.md .gitignore
git commit -m "init repo"
git push -u origin master
```
> this will make a folder with same name as your repository name

Create Django Project
------------------------------

- Go inside the folder mentioned above
- Create python virtual environment `python -m venv env`
- Activate virtual environment
  > use this command first whenever you want to develop your code

  - Windows `env\Scripts\activate.bat`
  - Linux `source env/bin/activate`
- Copy **requirements\.txt** and install the requirements `pip install -r requirements.txt`
- Create django project on current folder `django-admin startproject <project_name> .`
- Try the project by run `python manage.py runserver` and access it on **http://localhost:8000/**
  > you should see an error

Create Django App
-------------------------
- Create empty django app `python manage.py startapp <app_name>`

- Add the app name to INSTALLED_APPS array in settings\.py to register your app
```
# <project_name>/settings.py
...
INSTALLED_APPS = [
    ...
    '<app_name>',
]
```

- Add empty implementation of index function in views\.py
```
# <app_name>/views.py
...
from django.http import HttpResponse
...
def index(request):
	return HttpResponse("Hello World!")
```

- Create **urls\.py** in your app folder
```
# <app_name>/urls.py
...
from django.conf.urls import url
from .views import index
...
urlpatterns = [
	url(r'^$', index, name='index'),
]
```

- Register your app's urls\.py to project's urls\.py
```
# <project_name>/urls.py
...
from django.conf.urls import url, include
from django.contrib import admin
...
import <app_name>.urls as <app_name>
...
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^<app_name>/', include(<app_name>, namespace='<app_name>')),
]
```

- Run it again and access **http://localhost:8000/<app_name>**
  > you should see "Hello World!" in your browser


Deploy to server
----------------------
- Go to your Gitlab repository's **Settings > CI / CD > Secret variables** and add these variables:
  - SECRET_KEY
      Django secret key. You can generate it with https://www.miniwebtool.com/django-secret-key-generator/
  - HEROKU_APIKEY
      Your heroku account api key. **Account settings > API Key**
      Click on Reveal to see the API Key
  - HEROKU_APPNAME
      Your heroku app name
      To see your herouku apps list go to https://dashboard.heroku.com/apps
  - HEROKU_APP_HOST
      The url of your heroku app. By default is [https://<heroku_app_name>.herokuapp.com/](#)

- Change SECRET KEY initialization in **<app_name>/settings\.py**
```
# <project_name>/settings.py
...
SECRET_KEY = '<django_secret_key>'
...
```
  to the code below
```
# <project_name>/settings.py
...
from django.core.exceptions import ImproperlyConfigured
...
def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = 'Set the {} environment variable'.format(var_name)
        raise ImproperlyConfigured(error_msg)
...
try:
    SECRET_KEY = get_env_variable('SECRET_KEY')
except ImproperlyConfigured:
    SECRET_KEY = '<django_secret_key>'
...
```
  > this will set the SECRET_KEY with $SECRET_KEY environment variable (if exist), if not exist it will use the <django_secret_key>

- Set DEBUG variable to false in **<project_name>/settings\.py** and set the ALLOWED_HOST as below
```
...
ALLOWED_HOST = [
    '<heroku_app_name>.herokuapp.com',
]
...
```
  > set DEBUG to true when developing it in your local pc, but **don't forget** to set it to false when deploying it

- Add the following code to your **<project_name>/settings\.py**
```
import os
import dj_database_url
...
BASE_DIR = ...
PRODUCTION = os.environ.get('DATABASE_URL') != None
...
DATABASES = {
    ...
}
if PRODUCTION:
    DATABASES['default'] = dj_database_url.config()
```
  > this will set the database to use heroku configuration setting in deployment

- Add the following code to your **<project_name>/settings\.py**
```
...
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
...
STATIC_URL = '/static/'
...
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
```
  > this will set the static folder for static files collected by `python manage.py collectstatic --noinput`

- Add supporting files (**.gitlab-ci\.yml**, **deployment\.sh**, **Procfile**) to your project
  > the same folder where manage\.py lived

- edit **Procfile** to use your django project name
```
migrate: bash deployment.sh
web: gunicorn <project_name>.wsgi --log-file -
```

- Save all of the code, commit it, and push it to remote repository
```
git add .
git commit -m "add deployment configuration"
git push
```

- Check in your gitlab repository's pipeline. When the process is done, try to access it via [https://<heroku_app_name>.herokuapp.com/](#)
 > What you'll see must be the same as your http://localhost:8000 but without error message if something goes wrong
- To check the error message, you can access your application log by going to your heroku app dashboard, click **More** *(next to Open App in the upper right corner)*, and click **View logs**



Integration with Line Developer Channel
------------------------------------------------------
- Add another secret variables in your gitlab repository
  - LINE_CHANNEL_SECRET
      Your line developer channel secret key
      **Channel settings > Basic information > Channel Secret**
  - LINE_CHANNEL_ACCESS_TOKEN
      Your line channel access token
      **Channel settings > Messaging settings > Channel access token (long-lived)**

- Edit **.gitlab-ci\.yml** to pass the secret variable from gitlab to be heroku environment variable on deployment
```
Deployment:
    ...
    script:
        ...
        - heroku config:set --app $HEROKU_APPNAME SECRET_KEY=$SECRET_KEY
        - heroku config:set --app $HEROKU_APPNAME LINE_CHANNEL_SECRET=$LINE_CHANNEL_SECRET
        - heroku config:set --app $HEROKU_APPNAME LINE_CHANNEL_ACCESS_TOKEN=$LINE_CHANNEL_ACCESS_TOKEN
    ...
```

- Edit **<project_name>/settings\.py** below the initialization of SECRET_KEY
```
...
try:
    SECRET_KEY = get_env_variable('SECRET_KEY')
    LINE_CHANNEL_SECRET = get_env_variable('LINE_CHANNEL_SECRET')
    LINE_CHANNEL_ACCESS_TOKEN = get_env_variable('LINE_CHANNEL_ACCESS_TOKEN')
except ImproperlyConfigured:
    SECRET_KEY = '<django_secret_key>'
    LINE_CHANNEL_SECRET = 'dummy-line-channel-secret'
    LINE_CHANNEL_ACCESS_TOKEN = 'dummy-line-channel-access-token'
...
```

- Push your work `git push origin master`

- Set the webhook settings **Channel settings > Messaging settings > Webhook URL** to use your deployed django app url that handle the bot request ([https://<heroku_app_name>.herokuapp.com/<django_app_name>]())
  > if you click verify, this will give you error because the app hasn't handle the messaging api request yet


Handle Messaging API Request
-------------------------------------------
- Edit your **<app_name>/views\.py**
```
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
...
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
...
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
...
...
@csrf_exempt
def index(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
...
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
...
        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    try:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=event.message.text)
                        )
                    except LineBotApiError as e:
                        print(e.status_code)
                        print(e.error.message)
                        print(e.error.details)
...
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
```
  > your bot will just reply as the same as what user chat to your bot


Have Fun!
--------------
Just edit the **<app_name>/views\.py** to modify the behavior of your bot
