FROM python:3-alpine
WORKDIR /app
RUN apk add --no-cache socat
#COPY ./requirements.txt ./
#RUN pip3 install -r requirements.txt
COPY ./ ./
CMD socat -T 60 -d -d tcp-l:10081,reuseaddr,fork exec:"python3 vuln_manager.py"