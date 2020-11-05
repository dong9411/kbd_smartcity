curl -L https://github.com/OlafenwaMoses/FireNET/releases/download/v1.0/detection_model-ex-33--loss-4.97.h5 \
| gzip -9 - \
| aws s3 cp --content-encoding gzip - s3://hwangsehyun/FireNet.h5