# Real-Time Notification and Cloud Automation System

## Description
The **Real-Time Notification and Cloud Automation System** is a Python-based project designed to simplify the management of AWS services such as EC2, S3, RDS, and Lambda. It enables users to:

- Create, manage, and terminate AWS resources efficiently.
- Automate notifications via email upon completion of actions.
- Ensure streamlined workflows for cloud resource management.

---

## Features

### 1. EC2 Instance Management
- Launch new EC2 instances.
- Select AMI and instance types dynamically.
- Terminate running EC2 instances.

### 2. S3 Bucket Management
- Create S3 buckets with public or private access settings.
- Apply bucket policies for `public-read` access.
- Delete existing S3 buckets, including their contents.

### 3. RDS Instance Management
- Create MySQL-based RDS instances.
- Customize configurations like engine version, instance class, and credentials.
- Delete RDS instances.

### 4. Lambda Function Management
- Create new Lambda functions using uploaded ZIP files.
- Assign IAM roles for Lambda execution.
- Delete Lambda functions.

### 5. Notification System
- Sends email notifications after every operation using the Gmail SMTP service.

---

## File Structure

```
Real-Time-Notification-and-Cloud-Automation-System/
├── main.py                  # Entry point for the application.
├── ec2_service.py           # Manages EC2 instance operations.
├── s3_service.py            # Handles S3 bucket operations.
├── rds_service.py           # Manages RDS instances.
├── lambda_service.py        # Handles Lambda functions.
├── terminate_services.py    # Deletes EC2, S3, RDS, and Lambda resources.
├── email_service.py         # Sends email notifications.
├── __pycache__/             # Compiled Python files.
├── .gitignore               # Excludes unnecessary files from Git.
└── README.md                # Project documentation.
```

---

## Requirements

### Python Libraries:
- `boto3`: AWS SDK for Python.
- `smtplib`: To send emails.

### Environment:
- Python 3.9 or later.
- AWS credentials configured using the AWS CLI or environment variables.

---

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/siddharthpal18/Real-Time-Notification-and-Cloud-Automation-System.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Real-Time-Notification-and-Cloud-Automation-System
   ```

3. Install required dependencies:
   ```bash
   pip install boto3
   ```

4. Configure AWS credentials:
   ```bash
   aws configure
   ```

5. Run the application:
   ```bash
   python main.py
   ```

---

## Usage
Follow the on-screen prompts in `main.py` to manage AWS resources. Notifications will be sent to the configured email address upon task completion.

---

## Contributing
Feel free to submit issues or pull requests for improvements and bug fixes. Contributions are always welcome.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Author
**Siddharth Pal**

For inquiries or feedback, contact via [email](mailto:siddharthpal90990@gmail.com).
