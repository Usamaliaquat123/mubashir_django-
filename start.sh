#/bin/bash
cd /var/www
cd venv
source bin/activate 
cd ..
cd go_to_america
python3 manage.py runserver 0.0.0.0:8080 > /dev/null 2>&1
# /var/www/go_to_america