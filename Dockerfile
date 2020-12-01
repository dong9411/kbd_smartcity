FROM tensorflow/tensorflow
WORKDIR /root

RUN apt update -y && apt install -y libgl1-mesa-glx libglib2.0-0 && rm -rf /var/lib/apt/lists/*
RUN pip3 --no-cache-dir install imageai opencv-python keras requests boto3

#RUN curl https://kbdlab.hwangsehyun.com/nas/detection_model-ex-33--loss-4.97.h5 > detection_model-ex-33--loss-4.97.h5 
RUN curl kbdlab-nas.local:8000/detection_model-ex-33--loss-4.97.h5 > detection_model-ex-33--loss-4.97.h5
#ADD https://github.com/OlafenwaMoses/FireNET/releases/download/v1.0/detection_model-ex-33--loss-4.97.h5 detection_model-ex-33--loss-4.97.h5

COPY FireNet .
CMD ["bash", "source.sh", "python3", "aws.py"]