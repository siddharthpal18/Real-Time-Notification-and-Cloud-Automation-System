from ec2_service import create_ec2_instance
from s3_service import create_s3_bucket
from rds_service import create_rds_instance
from lambda_service import create_lambda_function
from terminate_services import terminate_ec2_instance, delete_s3_bucket, delete_rds_instance, delete_lambda_function
from email_service import send_email

def main():
    while True:
        print("\n=== Welcome to AWS Service Manager ===")
        print("1. Create EC2 Instance")
        print("2. Create S3 Bucket")
        print("3. Create RDS Instance")
        print("4. Create Lambda Function")
        print("5. Terminate EC2 Instance")
        print("6. Delete S3 Bucket")
        print("7. Delete RDS Instance")
        print("8. Delete Lambda Function")
        print("9. Exit")

        try:
            choice = int(input("Enter your choice (1-9): "))
            if choice == 9:
                print("Exiting... Goodbye!")
                break

            result = ""
            if choice == 1:
                result = create_ec2_instance()
            elif choice == 2:
                result = create_s3_bucket()
            elif choice == 3:
                result = create_rds_instance()
            elif choice == 4:
                result = create_lambda_function()
            elif choice == 5:
                result = terminate_ec2_instance()
            elif choice == 6:
                result = delete_s3_bucket()
            elif choice == 7:
                result = delete_rds_instance()
            elif choice == 8:
                result = delete_lambda_function()
            else:
                print("Invalid choice!")
                continue

            print(result)
            send_email("AWS Service Notification", result)
            print("Notification sent!")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 9.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
