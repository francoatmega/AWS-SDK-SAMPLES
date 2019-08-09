import os
import boto3


def main():

    try:

        session = boto3.session.Session(aws_access_key_id=os.environ['AWSKEY'],
                                        aws_secret_access_key=os.environ['AWSSECRET'])

        s3 = session.client("s3")

        s3.create_bucket(Bucket="my-new-bucket-name-123")

    except Exception as e:

        print("Error: ", str(e))


if __name__ == '__main__':

    main()
