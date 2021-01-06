import boto3
import cfnresponse
def handler(event, context):
    response_data = {}
    s3 = boto3.client('s3')
    the_bucket = event['ResourceProperties']['the_bucket']
    new = event['ResourceProperties']['dirs_to_create']
    the_event = event['RequestType']
    response = s3.list_objects_v2(Bucket=the_bucket)
    #check if objects exist in the bucket
    existing = []
    print(response)
    if 'Contents' in response:
        for i in response['Contents']:
            existing.append(i['Key'])
    else:
        pass
    #create and or delete objects to ensure the bucket reflects the state of dirs_to_create
    try:
        if the_event in ('Create', 'Update'):
            print("event is: ", the_event)
            dirs_to_create = []
            dirs_to_delete = []
            #if contents already exist in the bucket, create the difference first, then delete what is not defined in dirs_to_create
            if existing:
                for index, i in enumerate(new):
                    if i not in existing:
                        dirs_to_create.append(i)
                        #create_dirs(i)
                for index, i in enumerate(existing):
                    if i not in new:
                        dirs_to_delete.append(i)
                for create in dirs_to_create:
                    print("Creating:", str(create))
                    s3.put_object(Bucket=the_bucket, Key=create)
                for delete in dirs_to_delete:
                    print("Deleting:", str(delete))
                    s3.delete_object(Bucket=the_bucket, Key=delete)
            #if bucket is empty, create objects in dirs_to_create
            if not existing:
                for create in new:
                    print("Creating:", str(create))
                    s3.put_object(Bucket=the_bucket, Key=create)
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
