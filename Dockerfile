# This is designed to be run as a K8s CronJob, with the environment variables
# INFLUXDB_TOKEN, INFLUXDB_URL, and INFLUXDB_ORG set.
FROM library/python:3-alpine
COPY requirements.txt restartmapper /
RUN pip install -r /requirements.txt
USER guest
CMD ["/restartmapper"]
