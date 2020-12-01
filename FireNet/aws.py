import boto3
import requests
import traceback, sys 
import json

from firenet import detect_from_image

BUCKET = 'kbdlab-smartcity'
s3 = boto3.resource('s3')
s3_client = boto3.client('s3')
sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='SmartCity-CCTV')
try:
	queue.purge()
except Exception as error:
	print(error)

def loop():
	for message in queue.receive_messages():
		try:
			print(message.body)
			key = json.loads(message.body)['Records'][0]['s3']['object']['key']
			if '.tmp.' in key:
				continue

			object = s3.Object(BUCKET, key)
			img = object.get()['Body'].read()

			url = s3_client.generate_presigned_url(
				ClientMethod='get_object', 
				Params={
					'Bucket': BUCKET,
					'Key': key
				},
				ExpiresIn=300
			)
			data = {
				"image": url,
				"labels": {}
			}

			data["labels"]["fire"] = detect_from_image(img)
		except Exception as error:
			print(error)
			raise error
			data = ''.join(traceback.format_exception(*sys.exc_info()))

		message.delete()
		try:
			requests.post('https://proxy.hwangsehyun.com/smartcity/123', json=data)
		except Exception as error:
			print(error)

if __name__ == '__main__':
	s3_client.upload_file('1.jpg', BUCKET, '1.jpg')
	while 1:
		loop()
