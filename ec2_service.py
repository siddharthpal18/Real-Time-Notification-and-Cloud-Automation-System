import boto3

AWS_REGION = "us-east-1"  # Change as needed

def create_ec2_instance():
    print("\n=== Configure EC2 Instance ===")
    instance_types = ["t2.micro", "t2.small", "t2.medium"]
    images = {
    "Amazon Linux 2": "ami-0c02fb55956c7d316",  # Valid for us-east-1
    "Ubuntu 22.04": "ami-09d95fab7fff3776c"     # Replace with correct AMI for us-east-1
}


    print("Choose an instance type:")
    for idx, instance in enumerate(instance_types, 1):
        print(f"{idx}. {instance}")
    instance_type = instance_types[int(input("Enter choice (1-3): ")) - 1]

    print("Choose an AMI:")
    for idx, (name, ami) in enumerate(images.items(), 1):
        print(f"{idx}. {name}")
    ami_id = list(images.values())[int(input("Enter choice (1-2): ")) - 1]

    ec2 = boto3.resource('ec2', region_name=AWS_REGION)
    instance = ec2.create_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        MinCount=1,
        MaxCount=1
    )
    return f"EC2 Instance Created: {instance[0].id} with type {instance_type}"
