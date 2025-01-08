import boto3
import json

AWS_REGION = "us-east-1"  # Change this as needed

def create_iam_role_for_lambda(iam_client):
    """
    Creates an IAM role for Lambda if no suitable roles are found.
    """
    print("\nNo suitable IAM roles found. Creating a new IAM role for Lambda...")
    role_name = "LambdaExecutionRole"
    assume_role_policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "lambda.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }
        ]
    }

    try:
        response = iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(assume_role_policy_document),
            Description="Role for Lambda execution"
        )
        print(f"IAM Role Created: {response['Role']['Arn']}")
        return response['Role']['Arn']
    except iam_client.exceptions.EntityAlreadyExistsException:
        print("IAM Role already exists.")
        role = iam_client.get_role(RoleName=role_name)
        return role['Role']['Arn']
    except Exception as e:
        raise Exception(f"Failed to create IAM role: {e}")

def create_lambda_function():
    try:
        print("\n=== Configure Lambda Function ===")

        # Get the Lambda client
        # Interacts with the Lambda service to 
        # create, update, or manage Lambda functions.
        lambda_client = boto3.client('lambda', region_name=AWS_REGION)

        # Get the IAM client to fetch roles

        iam_client = boto3.client('iam', region_name=AWS_REGION)

        # Fetch available IAM roles
        roles_response = iam_client.list_roles()
        roles = [
            role['Arn'] for role in roles_response['Roles']
            if 'lambda.amazonaws.com' in role['AssumeRolePolicyDocument']['Statement'][0]['Principal'].get('Service', [])
        ]

        if not roles:
            # Create a new role if none exist
            selected_role_arn = create_iam_role_for_lambda(iam_client)
        else:
            # Display IAM roles for user selection
            print("\nAvailable IAM Roles:")
            for idx, role_arn in enumerate(roles, start=1):
                print(f"{idx}. {role_arn}")

            # Prompt user to select a role
            role_choice = int(input(f"\nEnter the number of the IAM role to use (1-{len(roles)}): "))
            selected_role_arn = roles[role_choice - 1]

        # Prompt for other function details
        function_name = input("Enter Lambda Function Name: ")
        zip_file_path = input("Enter Path to ZIP File: ")

        # Read the ZIP file
        with open(zip_file_path, 'rb') as f:
            code = f.read()

        # Create the Lambda function
        print("\nCreating Lambda function. Please wait...")
        response = lambda_client.create_function(
            FunctionName=function_name,
            Runtime='python3.9',
            Role=selected_role_arn,
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': code}
        )

        return f"Lambda Function Created Successfully: {response['FunctionName']}"

    except FileNotFoundError:
        return "Error: ZIP file not found. Please check the file path."
    except KeyError as e:
        return f"Error: Missing key {str(e)} in the IAM role response."
    except ValueError:
        return "Invalid input. Please enter a valid number for role selection."
    except Exception as e:
        return f"An unexpected error occurred: {e}"
