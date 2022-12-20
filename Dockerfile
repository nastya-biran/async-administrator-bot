FROM ubuntu

RUN apt-get update
RUN apt-get install -y python3 python3-pip

RUN pip install --upgrade pip

COPY . async_bot
WORKDIR async_bot
RUN yes | pip install -r /async_bot/requirements.txt

CMD ["python3", "main.py"]
