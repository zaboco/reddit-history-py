FROM python:2.7.12

COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt
COPY . /opt/app

WORKDIR /opt/app
CMD ["python", "main.py"]
