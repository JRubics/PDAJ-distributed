from celery import Celery
from celery.signals import worker_ready
from datetime import timedelta

app = Celery('pdaj')
app.config_from_object('pdaj.celeryconfig')


if app.conf.AM_I_SERVER:
    @worker_ready.connect
    def bootstrap(**kwargs):
        from .tasks.server import seed_computations

        # delay_time = timedelta(seconds=10) # seconds
        delay_time = 10
        print(f"Getting ready to automatically seed computations in 10 seconds...")

        params = {
            'theta_resolution': app.conf.PDAJ_THETA_RES,
            'dt': app.conf.PDAJ_DT,
            'tmax': app.conf.PDAJ_TMAX,
            'L1': app.conf.PDAJ_L1,
            'L2': app.conf.PDAJ_L2,
            'm1': app.conf.PDAJ_M1,
            'm2': app.conf.PDAJ_M2,
        }
        print(params)
        seed_computations.apply_async(kwargs=params, countdown=delay_time)


if __name__ == '__main__':
    app.start()
