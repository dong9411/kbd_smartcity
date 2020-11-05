FROM ubuntu:latest
RUN apt update -y
RUN apt install -y libgl1-mesa-glx libglib2.0-0
RUN apt install -y python3-pip
RUN pip3 install imageai tensorflow opencv-python keras
COPY ./fire ./fire_detection
WORKDIR /fire_detection
ENTRYPOINT ["python3", "fire_net.py"]
