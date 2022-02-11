FROM python:3.6
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD python tests/test.py