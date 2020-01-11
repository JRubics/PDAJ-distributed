from datetime import datetime
import os
import socket
import subprocess
import time
import csv

from celery import chain, chord
from celery.exceptions import Reject
import numpy as np

from ..app import app
from .worker import simulate_pendulum


def gen_simulation_model_params(theta_resolution):
    search_space = np.linspace(0, 2*np.pi, theta_resolution)
    for theta1_init in search_space:
        for theta2_init in search_space:
            yield theta1_init, theta2_init

def store_results(filename, results):
    with open(filename, 'w+') as f:
        writer = csv.writer(f)

        writer.writerow(['theta1_init', 'theta2_init', 'theta1', 'theta2'])
        for r in results:
          writer.writerow(r)

@app.task
def save_result(result):
    store_results(os.path.join(app.conf.RESULTS_DIR, "result.csv"), sorted(result))
    return result

@app.task
def seed_computations(theta_resolution, dt, tmax, L1, L2, m1, m2):
    return chord(
        (
            simulate_pendulum.s(theta1_init, theta2_init, dt, tmax, L1, L2, m1, m2)
            for theta1_init, theta2_init
            in gen_simulation_model_params(theta_resolution)
        ),
        save_result.s(),
    ).delay()

