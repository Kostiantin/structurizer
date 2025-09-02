# Deployment script for AWS
# Using free-tier services to keep costs at $0

# Upload React frontend to S3
aws s3 sync frontend/build/ s3://demo-ai-saas --region us-east-1

# Package and deploy Lambda function
cd api
zip -r function.zip .
aws lambda update-function-code --function-name demo-ai --zip-file fileb://function.zip

# Create DynamoDB table for caching
aws dynamodb create-table \
    --table-name DemoCache \
    --attribute-definitions AttributeName=ID,AttributeType=S \
    --key-schema AttributeName=ID,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --region us-east-1