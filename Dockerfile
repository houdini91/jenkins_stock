FROM python:3.8.3
LABEL stock_analyzer https://github.com/houdini91/jenkins_stock/stock_analyzer.git

WORKDIR /usr/src/stock

RUN mkdir -p /usr/src/stock
COPY . /usr/src/stock
RUN pip install --no-cache-dir -r requirements.txt

# CMD ["python", "./simple.py"]
