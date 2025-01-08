import boto3

AWS_REGION = "us-east-1"  # Change as needed

# Terminate EC2 Instance
def terminate_ec2_instance():
    ec2 = boto3.client('ec2', region_name=AWS_REGION)
    instances = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    instance_ids = [inst['InstanceId'] for res in instances['Reservations'] for inst in res['Instances']]

    if not instance_ids:
        return "No running EC2 instances found."

    print("\nRunning EC2 Instances:")
    for idx, instance_id in enumerate(instance_ids, 1):
        print(f"{idx}. {instance_id}")

    choice = int(input("Enter the number of the instance to terminate: "))
    instance_id = instance_ids[choice - 1]

    ec2.terminate_instances(InstanceIds=[instance_id])
    return f"EC2 Instance {instance_id} terminated."

# Delete S3 Bucket
def delete_s3_bucket():
    s3 = boto3.client('s3', region_name=AWS_REGION)
    buckets = s3.list_buckets()['Buckets']
    if not buckets:
        return "No S3 buckets found."

    print("\nAvailable S3 Buckets:")
    for idx, bucket in enumerate(buckets, 1):
        print(f"{idx}. {bucket['Name']}")

    choice = int(input("Enter the number of the bucket to delete: "))
    bucket_name = buckets[choice - 1]['Name']

    # Delete objects in the bucket before deleting it
    bucket = boto3.resource('s3', region_name=AWS_REGION).Bucket(bucket_name)
    bucket.objects.all().delete()
    bucket.delete()
    return f"S3 Bucket {bucket_name} deleted."

import boto3
from botocore.exceptions import ClientError

def delete_rds_instance():
    try:
        print("\n=== Delete RDS Instance ===")

        # Fetch all AWS regions
        ec2 = boto3.client('ec2')
        regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]

        # Display all regions
        print("\nAvailable AWS Regions:")
        for idx, region in enumerate(regions, start=1):
            print(f"{idx}. {region}")
        
        # Prompt user to select a region
        region_choice = int(input(f"\nEnter the number of the region to search for RDS instances (1-{len(regions)}): "))
        selected_region = regions[region_choice - 1]
        
        # Initialize RDS client for the selected region
        rds = boto3.client('rds', region_name=selected_region)

        # Fetch all RDS instances in the selected region
        response = rds.describe_db_instances()
        instances = response.get('DBInstances', [])

        if not instances:
            return f"No RDS instances found in region '{selected_region}'."

        # Display all instances in the selected region
        print(f"\nAvailable RDS Instances in '{selected_region}':")
        for idx, instance in enumerate(instances, start=1):
            print(f"{idx}. Identifier: {instance['DBInstanceIdentifier']}, Status: {instance['DBInstanceStatus']}, Engine: {instance['Engine']}")

        # Prompt user to select an instance for deletion
        choice = int(input(f"\nEnter the number of the instance to delete (1-{len(instances)}): "))
        selected_instance = instances[choice - 1]
        db_identifier = selected_instance['DBInstanceIdentifier']

        # Confirm deletion
        confirm = input(f"Are you sure you want to delete the RDS instance '{db_identifier}' in region '{selected_region}'? (yes/no): ").strip().lower()
        if confirm != "yes":
            return "Deletion cancelled by user."

        # Delete the selected RDS instance
        print(f"\nDeleting RDS instance '{db_identifier}' in region '{selected_region}'...")
        response = rds.delete_db_instance(
            DBInstanceIdentifier=db_identifier,
            SkipFinalSnapshot=True
        )

        return f"RDS instance '{db_identifier}' is being deleted in region '{selected_region}'. Details: {response}"

    except ClientError as e:
        error_message = e.response['Error']['Message']
        return f"ClientError: {error_message}"
    except ValueError:
        return "Invalid input. Please enter a valid number."
    except Exception as e:
        return f"An unexpected error occurred: {e}"



# Delete Lambda Function
def delete_lambda_function():
    lambda_client = boto3.client('lambda', region_name=AWS_REGION)
    functions = lambda_client.list_functions()['Functions']
    if not functions:
        return "No Lambda functions found."

    print("\nAvailable Lambda Functions:")
    for idx, func in enumerate(functions, 1):
        print(f"{idx}. {func['FunctionName']}")

    choice = int(input("Enter the number of the Lambda function to delete: "))
    function_name = functions[choice - 1]['FunctionName']

    lambda_client.delete_function(FunctionName=function_name)
    return f"Lambda Function {function_name} deleted."
