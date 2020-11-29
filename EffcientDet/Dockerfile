FROM pytorch/pytorch:1.4-cuda10.1-cudnn7-runtime
WORKDIR /root
ENV PIP_INDEX_URL=http://apt.network:3141/root/pypi/+simple/
ENV PIP_TRUSTED_HOST=apt.network


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt #-t /usr/lib/python3/dist-packages

RUN printf 'Acquire::HTTP::Proxy "http://apt.network:3142";\nAcquire::HTTPS::Proxy "false";' >> /etc/apt/apt.conf.d/01proxy
RUN apt update
RUN apt install -y libgtk2.0-dev

COPY . .

CMD python efficientdet_test.py