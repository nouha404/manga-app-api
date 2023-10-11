#!/bin/bash

# Activez le service Cron
service cron start

# Exécuter scrapper chaque semaine (le dimanche à minuit)
echo "0 0 * * 0 /usr/bin/python /app/scrapper.py" >> /etc/crontabs/root

# Démarrez le serveur Django
python manage.py runserver 0.0.0.0:8000
