from datetime import datetime, timedelta
from celery import Celery
from flask_mail import Message
from app import app, mail
from models import User



# Schedule a task to run every 10 minutes
# Celery Configuration

app = Celery(
    'tasks',
    broker = 'redis://localhost:6379/0',
    backend = 'redis://localhost:6379/0'
   
)
app.conf.redis_backend_protocol = 2
app.conf.broker_connection_retry_on_startup = True
# Scheduling tasks to run every 10 minutes

@app.task
def mail_students():
    now = datetime.now()
    ten_minutes_after = now + timedelta(minutes=10)

    
  
    students = User.query.filter_by(role='student').all()
    emails = [s.email for s in students if s.email]
    
    mail.send(Message(
        subject='Placement Drive Alert',
        recipients=emails,
        sender=app.config['MAIL_DEFAULT_SENDER']
    ))