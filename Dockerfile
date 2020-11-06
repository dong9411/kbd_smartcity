FROM tensorflow/tensorflow

WORKDIR /root
CMD ["python3", "fire_net.py"]

#ADD https://github.com/OlafenwaMoses/FireNET/releases/download/v1.0/detection_model-ex-33--loss-4.97.h5 detection_model-ex-33--loss-4.97.h5
ADD https://kbdlab.hwangsehyun.com/nas/detection_model-ex-33--loss-4.97.h5 detection_model-ex-33--loss-4.97.h5

RUN apt update -y && apt install -y libgl1-mesa-glx libglib2.0-0 && rm -rf /var/lib/apt/lists/*
RUN pip3 --no-cache-dir install imageai opencv-python keras

COPY FireNet .
