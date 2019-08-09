import os
import boto3


def main():

    try:

        session = boto3.session.Session(aws_access_key_id=os.environ['AWSKEY'],
                                        aws_secret_access_key=os.environ['AWSSECRET'])

        iam = session.client("iam")

        iam.create_user(Path="/", UserName="NEW_USER_NAME")

        print("User created...")

    except Exception as e:

        print("Error: ", str(e))


if __name__ == '__main__':

    main()
