import os
import boto3

sended = 0
total = 0


def main():

    try:

        global total

        session = boto3.session.Session(aws_access_key_id=os.environ['AWSKEY'],
                                        aws_secret_access_key=os.environ['AWSSECRET'])

        s3 = session.client("s3")

        total = s3.get_object(Bucket="my-new-bucket-name-123", Key="my_remote_file")['ContentLength']

        s3.download_file("my-new-bucket-name-123", "my_remote_file", "my_local_file", Callback=progress)

    except Exception as e:

        print("Error: ", str(e))


def progress(bytes):

    global sended
    global total

    sended += bytes

    temp = sended * 100
    percent = (temp / total) * 1

    print("{}% Downloaded(s)".format(int(percent)))


if __name__ == '__main__':

    main()
