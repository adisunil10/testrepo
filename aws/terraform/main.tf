# Terraform configuration for AWS deployment
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# ECR Repository
resource "aws_ecr_repository" "llm_support" {
  name                 = "llm-support-agent"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "llm_support" {
  name = "llm-support-cluster"
}

# ECS Task Definition
resource "aws_ecs_task_definition" "llm_support" {
  family                   = "llm-support-agent"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "2048"
  memory                   = "4096"

  container_definitions = jsonencode([
    {
      name  = "api"
      image = "${aws_ecr_repository.llm_support.repository_url}:latest"
      portMappings = [
        {
          containerPort = 8000
          protocol      = "tcp"
        }
      ]
      environment = [
        {
          name  = "MLFLOW_TRACKING_URI"
          value = "http://mlflow:5000"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/llm-support"
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "ecs"
        }
      }
    }
  ])
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "llm_support" {
  name              = "/ecs/llm-support"
  retention_in_days = 7
}

# Variables
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

# Outputs
output "ecr_repository_url" {
  value = aws_ecr_repository.llm_support.repository_url
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.llm_support.name
}

