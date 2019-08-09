import os
import boto3


def main():

    try:

        session = boto3.session.Session(aws_access_key_id=os.environ['AWSKEY'],
                                        aws_secret_access_key=os.environ['AWSSECRET'])

        iam = session.client("iam")

        key = iam.create_access_key(UserName="NEW_USER_NAME")

        print("Access Key: ", key['AccessKey']['AccessKeyId'])
        print("Secret Key: ", key['AccessKey']['SecretAccessKey'])

    except Exception as e:

        print("Error: ", str(e))


if __name__ == '__main__':

    main()
