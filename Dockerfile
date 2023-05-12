FROM python

RUN mkdir /app
WORKDIR /app

COPY ./intermediary.py /app/intermediary.py

EXPOSE 1028
EXPOSE 1536-2048

CMD ["python", "/app/intermediary.py"]
