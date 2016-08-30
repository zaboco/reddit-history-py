FROM python:2.7.12

COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt
COPY . /opt/app

EXPOSE 5000

WORKDIR /opt/app
CMD ["python", "-u", "history_api.py"]
