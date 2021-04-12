FROM python:3.8.3
LABEL jenkins_stock https://github.com/houdini91/jenkins_stock.git

WORKDIR /usr/src/stock

RUN mkdir -p /usr/src/stock
COPY . /usr/src/stock
RUN pip install --no-cache-dir -r requirements.txt

# CMD ["python", "./simple.py"]
