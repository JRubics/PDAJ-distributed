FROM python:3.8-slim

# Install the required Python packages
# Celery has to be installed via pip, as Ubuntu distributes an older version which has a critical bug involving chords
# (see http://celery.readthedocs.org/en/latest/changelog.html for details)
RUN pip install "celery[librabbitmq,redis]" scipy

# Parameterize this Dockerfile, by storing the configuration within environment variables 
ENV MAX_CPU_CORES 1
ENV SERVER_NAME server
ENV WORKER_LIST worker

# Deploy the app
COPY pdaj /code/pdaj/
ENV PYTHONPATH=/code \
    PYTHONUNBUFFERED="1" \
    C_FORCE_ROOT="1"

CMD ["celery", "worker", "--app", "pdaj.app", "-E", "-Ofair", "--loglevel=WARN"]