import schedule

from src.tasks import outbox_events_task

schedule.every(5).seconds.do(outbox_events_task)
