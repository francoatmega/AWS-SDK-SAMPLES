import os
import boto3


def main():

    """
    INFORMATION

    Moving a file or folder in AWS S3 is not possible, you need to copy the object to
    new location and delete the old file after that
    """

    try:

        session = boto3.session.Session(aws_access_key_id=os.environ['AWSKEY'],
                                        aws_secret_access_key=os.environ['AWSSECRET'])

        s3 = session.client("s3")

        copy_source = {

            'Bucket': 'my-new-bucket-name-123',
            'Key': "old_file_location"
        }

        s3.copy(Bucket="my-new-bucket-name-123", CopySource=copy_source,
                Key="new_file_location")

        s3.delete_object(Bucket="my-new-bucket-name-123", Key="old_file_location")

    except Exception as e:

        print("Error: ", str(e))


if __name__ == '__main__':

    main()
