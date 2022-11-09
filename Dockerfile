FROM python:slim

COPY app.py /app/app.py
COPY requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip install -r requirements.txt
RUN chmod 755 app.py
EXPOSE 5000
ENTRYPOINT ["./app.py"]
