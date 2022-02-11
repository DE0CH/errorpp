FROM python:3.6
COPY setup.cfg setup.cfg
COPY setup.py setup.py 
RUN pip3 install . 
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD pwd