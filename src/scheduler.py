import schedule
import time
import logging
from datetime import datetime

class LocalScheduler:
    def __init__(self, app, run_time="06:00"):
        self.app = app
        self.run_time = run_time
        self.logger = logging.getLogger(__name__)
        
    def setup_schedule(self):
        schedule.every().day.at(self.run_time).do(self.run_job)
        self.logger.info(f"Scheduled daily job at {self.run_time}")
        
    def run_job(self):
        self.logger.info(f"Running scheduled job at {datetime.now()}")
        try:
            self.app.run()
            self.logger.info("Job completed successfully")
        except Exception as e:
            self.logger.error(f"Job failed: {str(e)}")
            
    def start(self):
        self.setup_schedule()
        self.logger.info("Scheduler started")
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
