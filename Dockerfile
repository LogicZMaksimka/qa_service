FROM python:3.7.13

WORKDIR /qa_service

ENV FLASK_APP=app.py

ENV FLASK_RUN_HOST=0.0.0.0

COPY . .

RUN git clone -b feat/generative_qa https://github.com/LogicZMaksimka/DeepPavlov-1.git

RUN git clone https://github.com/studio-ousia/bpr.git

RUN python3.7 -m pip install ./bpr

RUN python3.7 -m pip install ./DeepPavlov-1

RUN python3.7 -m pip install -r requirements.txt

EXPOSE 5000

CMD ["python3.7", "app.py"]