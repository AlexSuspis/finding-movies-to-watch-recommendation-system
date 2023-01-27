FROM python:3.8.12

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

#Install dependencies
COPY requirements.txt ./
RUN apt-get update \
    && apt-get install -y pip \ 
    && pip install --upgrade pip==21.2.4 \
    && pip install -r requirements.txt

COPY . .

EXPOSE 3000

CMD ["python","index.py"]
