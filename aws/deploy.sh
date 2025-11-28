#!/bin/bash
# AWS Deployment Script for LLM Customer Support Agent

set -e

echo "🚀 Starting AWS deployment..."

# Configuration
REGION="us-east-1"
ECR_REPOSITORY="llm-support-agent"
ECS_CLUSTER="llm-support-cluster"
ECS_SERVICE="llm-support-service"
IMAGE_TAG="latest"

# Check AWS CLI
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Please install it first."
    exit 1
fi

# Login to ECR
echo "📦 Logging into ECR..."
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $(aws sts get-caller-identity --query Account --output text).dkr.ecr.$REGION.amazonaws.com

# Create ECR repository if it doesn't exist
echo "📦 Creating ECR repository if needed..."
aws ecr describe-repositories --repository-names $ECR_REPOSITORY --region $REGION || \
aws ecr create-repository --repository-name $ECR_REPOSITORY --region $REGION

# Build and push Docker image
echo "🔨 Building Docker image..."
docker build -t $ECR_REPOSITORY:$IMAGE_TAG .

ECR_URI=$(aws sts get-caller-identity --query Account --output text).dkr.ecr.$REGION.amazonaws.com/$ECR_REPOSITORY:$IMAGE_TAG

echo "📤 Tagging and pushing to ECR..."
docker tag $ECR_REPOSITORY:$IMAGE_TAG $ECR_URI
docker push $ECR_URI

# Update ECS service (if it exists)
echo "🔄 Updating ECS service..."
if aws ecs describe-services --cluster $ECS_CLUSTER --services $ECS_SERVICE --region $REGION --query 'services[0].status' --output text | grep -q "ACTIVE"; then
    aws ecs update-service \
        --cluster $ECS_CLUSTER \
        --service $ECS_SERVICE \
        --force-new-deployment \
        --region $REGION
    echo "✅ ECS service updated!"
else
    echo "⚠️  ECS service not found. Please create it first using terraform or AWS console."
fi

echo "✅ Deployment complete!"

