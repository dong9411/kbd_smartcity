FROM tensorflow/tensorflow
WORKDIR /root

ARG CACHE=""
ENV PIP_INDEX_URL http://${CACHE}:3141/root/pypi/+simple/
ENV PIP_TRUSTED_HOST ${CACHE}
RUN [ ! -z ${CACHE} ] && printf "Acquire::HTTP::Proxy \"http://${CACHE}:3142\";\nAcquire::HTTPS::Proxy \"false\";" >> /etc/apt/apt.conf.d/01proxy

RUN apt update -y && apt install -y libgl1-mesa-glx libglib2.0-0 && rm -rf /var/lib/apt/lists/*
RUN pip3 --no-cache-dir install imageai opencv-python keras requests boto3

#RUN curl https://kbdlab.hwangsehyun.com/nas/detection_model-ex-33--loss-4.97.h5 > detection_model-ex-33--loss-4.97.h5 
RUN curl kbdlab-nas.local:8000/detection_model-ex-33--loss-4.97.h5 > detection_model-ex-33--loss-4.97.h5
#ADD https://github.com/OlafenwaMoses/FireNET/releases/download/v1.0/detection_model-ex-33--loss-4.97.h5 detection_model-ex-33--loss-4.97.h5

COPY . .
CMD ["bash", "source.sh", "python3", "aws.py"]