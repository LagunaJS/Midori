Getting Started:

```
pip install virtualenv
virtualenv mysiteenv
source mysiteenv/bin/activate
pip install Django==1.8.1
django-admin.py startproject --template=https://github.com/pinax/pinax-project-account/zipball/master mysite
cd mysite
chmod +x manage.py
pip install -r requirements.txt
./manage.py migrate
./manage.py loaddata sites
./manage.py runserver
```
