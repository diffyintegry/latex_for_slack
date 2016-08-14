FROM python:2.7-slim
ADD . /src
WORKDIR /src
RUN pip install -r requirements.txt
CMD ["sh", "-c", "python ./bot/app.py& python ./bot/flask_server.py"]
