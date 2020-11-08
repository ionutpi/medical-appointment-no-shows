FROM python:3.7-slim

ADD no-show-web no-show-web

RUN pip install pandas==1.0.3
RUN pip install scikit-learn==0.22.2.post1
RUN pip install Flask==1.1.1
RUN pip install Flask-Cors==3.0.8
RUN pip install gunicorn==20.0.4

CMD cd no-show-web && gunicorn --bind 0.0.0.0:8080 no-show-app:app