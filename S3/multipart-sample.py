import os
import time
import boto3


class MultipartUpload:

    s3 = None
    mpuid = None
    try_count = 0
    SPLIT_PART_MAX = 1024**2 * 10 #10 megabytes

    def __init__(self, mpuid=None):

        self.session = boto3.session.Session(aws_access_key_id=os.environ['AWSKEY'],
                                        aws_secret_access_key=os.environ['AWSSECRET'])

        self.s3 = self.session.client("s3")

        self.mpuid = mpuid

    def CreateMultipartUpload(self, bucket, key):

        try:

            self.mpuid = self.s3.create_multipart_upload(Bucket=bucket, Key=key)

            print("MPUID created with success")

            return self.mpuid

        except Exception as e:

            print(str(e))

    def UploadMultipartUpload(self, bucket, key, file):

        try:

            self.try_count += 1

            if self.try_count <= 5:

                time.sleep(30)  #ESPERA 10 MINUTOS

            else:

                print("Mais do que 5 tentativas, adicionando de envio, informações"
                      "\nbucket: " + bucket +
                      "\nkey: " + key +
                      "\nfile: " + file +
                      "\nmpuid: " + self.mpuid["UploadId"])

            mpu = self.mpuid["UploadId"]

            partes = self.s3.list_parts(Bucket=bucket,
                                   Key=key,
                                   UploadId=mpu)

            if not "Parts" in partes:

                parte = 1

            else:

                parte = partes["Parts"]

            with open(file, "rb") as f:

                uploaded_bytes = 0
                part_number = parte

                if part_number == 1:

                    f.seek(0)

                else:

                    f.seek((self.SPLIT_PART_MAX * (part_number - 1)))

                while True:

                    data = f.read(self.SPLIT_PART_MAX)

                    if not len(data):

                        break

                    part = self.s3.upload_part(Body=data,
                                          Bucket=bucket,
                                          Key=key,
                                          UploadId=mpu,
                                          PartNumber=part_number)

                    uploaded_bytes += len(data)

                    print(str(part_number) + " parts sended")

                    print(str(uploaded_bytes // 1024 // 1024) + " MB sended from total of " +
                          str(os.path.getsize(file) // 1024 // 1024) + " MB")

                    part_number += 1

        except Exception as e:

            print(str(e))

    def CompleteMultipartUpload(self, bucket, key):

        try:

            partes = self.s3.list_parts(Bucket=bucket,
                                        Key=key,
                                        UploadId=self.mpuid["UploadId"])

            if "Parts" in partes:

                parts = []

                for parte in partes["Parts"]:

                    parts.append({"PartNumber": parte["PartNumber"], "ETag": parte["ETag"]})

            self.s3.complete_multipart_upload(Bucket=bucket,
                                              Key=key,
                                              UploadId=self.mpuid["UploadId"],
                                              MultipartUpload={"Parts": parts})

            return True, "Ok"

        except Exception as e:

            return False, str(e)


def main():

    bucket = "wst-test-jardel"
    key = "jardel.zip"
    file = "E:/jardel.zip"
    mpu = None

    s = MultipartUpload(mpuid=mpu)

    mpu = s.CreateMultipartUpload(bucket, key)

    s.UploadMultipartUpload(bucket, key, file)

    ret, val = s.CompleteMultipartUpload(bucket, key)

    if not ret:

        print(val)

    else:

        print("Upload with success!")


if __name__ == "__main__":

    main()
