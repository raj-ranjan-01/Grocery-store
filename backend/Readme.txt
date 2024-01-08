# At first install all the requiremnts
# Then run flask bakcend using python main.py and frontend using npm run serve
# then run celery and celery beats using below command 
    celery -A main.celery worker -l info -P threads
    celery -A main.celery beat -l info
# Run redis using redis-server 