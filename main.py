from src.db.deps import init_db, get_db_session_context
from src.deps import create_service1, create_service2, create_tasks_scheduler
from src.scheduler import TasksScheduler
from src.services import Service1, Service2


def run_event_loop(scheduler: TasksScheduler, svc1: Service1, svc2: Service2):
    while True:
        cmd = input('Enter command: ')

        if cmd == 'stop':
            scheduler.stop()
            break

        if cmd == 'ev1':
            svc1.do_smth()

        if cmd == 'ev2':
            svc2.do_smth()


def main():
    init_db()

    scheduler = create_tasks_scheduler()
    scheduler.run()

    with get_db_session_context() as db_session:
        svc1 = create_service1(db_session)
        svc2 = create_service2(db_session)

        try:
            run_event_loop(scheduler, svc1, svc2)
        except KeyboardInterrupt:
            scheduler.stop()


if __name__ == '__main__':
    main()
