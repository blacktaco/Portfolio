import boto3
import cfnresponse

def get_existing_dirs():
	if 'Contents' in response:
		dirs = []
		for i in response['Contents']:
			dirs.append(i['Key'])
		return dirs
	else:
		pass

def create_dirs(dirs_to_create):
	for dirs in dirs_to_create:
		print("Creating:", str(dirs_to_create))
		s3.put_object(Bucket=the_bucket, Key=dirs_to_create)

def delete_dirs(dirs_to_delete):
	for dirs in dirs_to_delete:
		print("Deleting:", str(dirs_to_delete))
		s3.delete_object(Bucket=the_bucket, Key=dirs_to_delete)

def handler(event, context):

	the_bucket = event['ResourceProperties']['the_bucket']
	new = event['ResourceProperties']['dirs_to_create']
	the_event = event['RequestType']
	response_data = {}
	existing = get_existing_dirs()

	try:
		if the_event in ('Create', 'Update'):
			print("event is: ", the_event)
			dirs_to_create = []
			dirs_to_delete = []
			#set dirs to create and dirs to delete
			if existing:
				for index, i in enumerate(new):
					if i not in existing:
						dirs_to_create.append(i)
						#create_dirs(i)
				for index, i in enumerate(existing):
					if i not in new:
						dirs_to_delete.append(i)
			for i in dirs_to_create:
				create_dirs(i)
			for i in dirs_to_delete:
				delete_dirs(i)
			# if bucket is new, create new folders, and skip deletion
			if not existing:
				for index, i in enumerate(new):
					dirs_to_create.append(i)
					create_dirs(i)
			else:
				print("No changes have been detected")
		
		#if event is delete, the bucket objects will get deleted
		elif the_event == 'Delete':
			print("Deleting S3 content...")
			b_operator = boto3.resource('s3')
			b_operator.Bucket(str(the_bucket)).objects.all().delete()
		print("Execution succesfull!")
		cfnresponse.send(event,
		                 context,
		                 cfnresponse.SUCCESS,
		                 response_data)
	
	except Exception as e:
	    print("Execution failed...")
	    print(str(e))
	    response_data['Data'] = str(e)
	    cfnresponse.send(event,
	                     context,
	                     cfnresponse.FAILED,
	                     response_data)	