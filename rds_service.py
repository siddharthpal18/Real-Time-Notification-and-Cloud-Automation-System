import boto3
from botocore.exceptions import ClientError

def create_rds_instance():
    try:
        print("\n=== Configure RDS Instance ===")

        # Initialize RDS client
        rds = boto3.client('rds')
        region = boto3.session.Session().region_name

        # Fetch available MySQL versions in the current region
        print("\nFetching available MySQL versions...")
        response = rds.describe_db_engine_versions(
            Engine='mysql',
            DefaultOnly=False,
            Filters=[{'Name': 'status', 'Values': ['available']}]
        )
        available_versions = [v['EngineVersion'] for v in response['DBEngineVersions']]

        if not available_versions:
            return "No MySQL versions are available in this region."

        # Display available MySQL versions
        print("\nAvailable MySQL Versions:")
        for idx, version in enumerate(available_versions, start=1):
            print(f"{idx}. {version}")

        # User-friendly prompts
        db_identifier = input("Enter DB Identifier (default: mydbinstance): ") or "mydbinstance"
        db_name = input("Enter Database Name (default: MyDatabase): ") or "MyDatabase"
        master_username = input("Enter Master Username (default: admin): ") or "admin"
        master_password = input("Enter Master Password (default: admin12345): ") or "admin12345"

        # Instance class selection
        instance_classes = ["db.t3.micro", "db.t2.micro", "db.m6g.large", "db.t3.medium"]
        print("\nSelect DB Instance Class:")
        for idx, cls in enumerate(instance_classes, start=1):
            print(f"{idx}. {cls}")
        instance_class_choice = int(input("Enter choice (1-4): "))
        instance_class = instance_classes[instance_class_choice - 1]

        # Engine version selection
        print("\nSelect MySQL Engine Version:")
        for idx, version in enumerate(available_versions, start=1):
            print(f"{idx}. {version}")
        engine_version_choice = int(input(f"Enter choice (1-{len(available_versions)}): "))
        engine_version = available_versions[engine_version_choice - 1]

        # Create RDS instance
        print("\nCreating RDS instance. Please wait...")
        response = rds.create_db_instance(
            DBInstanceIdentifier=db_identifier,
            AllocatedStorage=20,
            DBName=db_name,
            Engine='mysql',
            MasterUsername=master_username,
            MasterUserPassword=master_password,
            DBInstanceClass=instance_class,
            EngineVersion=engine_version,
            LicenseModel='general-public-license',
            StorageType='gp2',
            PubliclyAccessible=True,
            BackupRetentionPeriod=7
        )

        return f"RDS Instance '{db_identifier}' created successfully! Details: {response}"

    except ClientError as e:
        error_message = e.response['Error']['Message']
        return f"ClientError: {error_message}"
    except ValueError:
        return "Invalid input. Please enter valid numbers for selection."
    except Exception as e:
        return f"An unexpected error occurred: {e}"
