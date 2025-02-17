## AWS Lambda function deployment 

- Save lambda in file, eg lambda_function.py
- AWS Lambda requires the function code to be packaged in a ZIP file. Create a ZIP file containing the lambda_function.py file:
  ```bash
  zip lambda_function.zip lambda_function.py
  ```
- AWS Lambda needs an IAM role to execute. Create a role with the AWSLambdaBasicExecutionRole policy attached.(trust-policy.json)
  ```bash
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Service": "lambda.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  }
  ```
- Create the IAM role:
  ```bash
  aws iam create-role --role-name lambda-greet-user-role --assume-role-policy-document file://trust-policy.json
  ```
- Attach the AWSLambdaBasicExecutionRole policy
  ```bash
  aws iam attach-role-policy --role-name lambda-greet-user-role --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
  ```
- Get the role ARN:
  ```bash
  aws iam get-role --role-name lambda-greet-user-role --query 'Role.Arn' --output text
  ```
  Save the ARN for the next step.
- Use the AWS CLI to create the Lambda function:
  ```bash
  aws lambda create-function \
    --function-name greet-user \
    --zip-file fileb://lambda_function.zip \
    --handler lambda_function.greet_user \
    --runtime python3.9 \
    --role <ROLE_ARN> \
    --timeout 10 \
    --memory-size 128
  ```
  Replace <ROLE_ARN> with the ARN of the IAM role you created earlier.
- Make sure both cli user and lambda role have lambda access

  <img width="1628" alt="Image" src="https://github.com/user-attachments/assets/10b1aa81-722d-4270-a3b5-ac5ff3aaf872" />

  <img width="1628" alt="Image" src="https://github.com/user-attachments/assets/ea2fec4c-d20c-45a7-94b5-e0310dae6dcb" />

- Invoke the Lambda function using the AWS CLI:
  ```bash
  aws lambda invoke \
    --function-name greet-user \
    --payload '{"name": "John"}' \
    --cli-binary-format raw-in-base64-out \
    output.txt
  ```

## S3 bucket setup and permissions 

- Navigate to S3 dashboard

  <img width="1628" alt="Image" src="https://github.com/user-attachments/assets/fc231880-9613-4aab-a378-d06707083d82" />

- Proceed to create bucket

  <img width="1628" alt="Image" src="https://github.com/user-attachments/assets/6fefdd01-5bf3-49de-9def-b4aa6706afad" />

- Configure permissions
  
  <img width="1628" alt="Image" src="https://github.com/user-attachments/assets/2b50bde1-61fa-4542-aee2-2801c593b91f" />

  <img width="1628" alt="Image" src="https://github.com/user-attachments/assets/85565f7d-ef97-4bde-82bb-c9020653237e" />


## RDS database instance configuration 
- Navigate to VPC dashboard
- On the left menu navigate to security groups and create new security group

  <img width="1628" alt="Image" src="https://github.com/user-attachments/assets/0b79c734-ac72-4306-b6e9-fae3c8341809" />

- Configure inbound rules for both IPV4 and IPV6

  <img width="1628" alt="Image" src="https://github.com/user-attachments/assets/c81a34bc-024f-477c-95a3-f37d1e30c985" />

- Navigate to RDS dashboard
- Proceed to create database

  <img width="1628" alt="Image" src="https://github.com/user-attachments/assets/017a8eb2-c4a6-47bc-ac5d-06cc2cd7db98" />

  <img width="1628" alt="Image" src="https://github.com/user-attachments/assets/28e101af-1578-4f69-b0a8-fa72a9166552" />

- Set db instance password
- On storage disable auto-scaling
- Enable public access and give access to the VPC security group previously created
  
  <img width="1628" alt="Image" src="https://github.com/user-attachments/assets/9379ec2c-d732-4148-b5b9-bbf838f40c5c" />

  <img width="1628" alt="Image" src="https://github.com/user-attachments/assets/1660d8f7-c41e-4960-a008-9c3e760a3471" />


##  IAM role and policy settings

- From your dashboard navigate to IAM
- Navigate to users on the left menu
- Create new user

<img width="1628" alt="Image" src="https://github.com/user-attachments/assets/30d38d70-36de-4307-98a5-850685fce132" />

- Continue to create user

<img width="1628" alt="Image" src="https://github.com/user-attachments/assets/3829761f-c185-4622-ad86-d77c47a32127" />

- Then create user

<img width="1628" alt="Image" src="https://github.com/user-attachments/assets/33e0c403-475a-4147-a841-f780bcf21e6f" />

- Once user is created, login details are provided

<img width="1628" alt="Image" src="https://github.com/user-attachments/assets/bb852a20-1e2c-458a-b7b3-e8a4b2bf40d7" />

- Navigate to user groups, create new group and link users

<img width="1628" alt="Image" src="https://github.com/user-attachments/assets/619d05d7-112b-4eba-a7e4-79718b7cdfbf" />

- Create access key for AWS CLI

<img width="1628" alt="Image" src="https://github.com/user-attachments/assets/adabbe77-5301-433d-b062-2a9e13d19070" />

<img width="1628" alt="Image" src="https://github.com/user-attachments/assets/95972e4f-e657-44c4-b580-12bdc4a53b2b" />
