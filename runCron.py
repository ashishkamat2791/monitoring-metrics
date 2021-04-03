from crontab import CronTab
 
my_cron = CronTab(user='askamat')
job = my_cron.new(command='python3 getData.py')
job.minute.every(5)
 
my_cron.write()