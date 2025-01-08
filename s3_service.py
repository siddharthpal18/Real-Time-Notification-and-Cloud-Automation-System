import boto3
import json
from botocore.exceptions import ClientError

def create_s3_bucket():
    try:
        print("\n=== Configure S3 Bucket ===")
        bucket_name = input("Enter a unique S3 Bucket Name: ")
        access_types = ["private", "public-read"]

        print("Choose access type:")
        for idx, access in enumerate(access_types, 1):
            print(f"{idx}. {access}")
        access_type = access_types[int(input("Enter choice (1-2): ")) - 1]

        # Initialize session and determine region
        session = boto3.Session()
        region = session.region_name
        s3 = session.client('s3')

        # Handle bucket creation based on region
        if region != 'us-east-1':
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        else:
            s3.create_bucket(Bucket=bucket_name)

        # Apply public access settings if "public-read" is selected
        if access_type == "public-read":
            # Disable Block Public Access
            s3.put_public_access_block(
                Bucket=bucket_name,
                PublicAccessBlockConfiguration={
                    'BlockPublicAcls': False,
                    'IgnorePublicAcls': False,
                    'BlockPublicPolicy': False,
                    'RestrictPublicBuckets': False
                }
            )

            # Apply bucket policy to grant public-read access
            bucket_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": "s3:GetObject",
                        "Resource": f"arn:aws:s3:::{bucket_name}/*"
                    }
                ]
            }
            s3.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(bucket_policy))
            print(f"Public access granted using bucket policy for '{bucket_name}'")
        else:
            # Do nothing for private buckets (default behavior)
            print(f"Bucket '{bucket_name}' created successfully with private access.")

        return f"S3 Bucket Created: {bucket_name} with {access_type} access"

    except ClientError as e:
        return f"ClientError: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"
