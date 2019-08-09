import os
import boto3


def main():

    try:

        session = boto3.session.Session(aws_access_key_id=os.environ['AWSKEY'],
                                        aws_secret_access_key=os.environ['AWSSECRET'])

        iam = session.client("iam")

        result = iam.list_users(PathPrefix='/')

        for user in result['Users']:

            print(user['UserName'])

    except Exception as e:

        print("Error: ", str(e))


if __name__ == '__main__':

    main()
