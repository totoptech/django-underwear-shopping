from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from portal import views

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(views.portal_scrape, 'interval', minutes=1440)
    scheduler.start()