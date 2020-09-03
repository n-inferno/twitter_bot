FROM python:3.7

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/
RUN pip3 install -r requirements.txt
ENV TZ=Europe/Moscow

CMD ["python", "bot.py"]