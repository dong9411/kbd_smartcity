HOST=kbdlab.hwangsehyun.com
docker build --network network -t $HOST/efficient-det .
docker push $HOST/efficient-det