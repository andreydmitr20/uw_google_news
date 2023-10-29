# uw_google_news

<h2>Test local</h2>

<p> edit .env file: 
selenium_host=localhost
db_host=localhost
redis_host=localhost
</p>
<p>docker compose -f local.yml up --build</p>
<p>cd back</p>
<p>celery -A back  worker -P threads --loglevel=info --beat</p>
<p>uwsgi --ini uwsgi.ini</p>
<p>or</p>
<p>python3 m runserver</p>
<p>http://127.0.0.1:8000/api/admin</p>
<p>http://127.0.0.1:8000/api/docs</p>
<p>http://127.0.0.1:8000/news</p>

<h2>Test local as on the server</h2>

<p> edit .env file: 
selenium_host=selenium
db_host=db
redis_host=redis
</p>

<p>docker compose -f server.yml up --build</p>

<h2>.env example</h2>

<p>
selenium_host=localhost
db_host=localhost
redis_host=localhost

#selenium_host=selenium
#db_host=db
#redis_host=redis

openai_api_key = ...

selenium_prefix=http://
selenium_postfix=/wd/hub
selenium_port=4444

db_user=pguser
db_pass=...
db_port=5432
db_echo=True
db_log_statement=all
#db_log_statement=none
db_proto=postgresql://
db_name=pguser

django_secret_key=...

redis_port=6379

</p>
