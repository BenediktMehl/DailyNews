provider "aws" {
  region = "eu-central-1"
}

resource "aws_s3_bucket" "my_bucket" {
  bucket  = "my-daily-news-bucket"
  tags    = {
    Name          = "MyS3Bucket"
    Environment    = "Production"
  }
}

resource "aws_s3_object" "lambda_zip" {
  bucket = aws_s3_bucket.my_bucket.bucket
  key    = "lambda/my_python_app.zip"
  source = "lambda.zip"
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda_execution_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_policy_attachment" "lambda_policy" {
  name       = "lambda_policy_attachment"
  roles      = [aws_iam_role.lambda_role.name]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "my_lambda" {
  function_name = "my_python_app"
  role          = aws_iam_role.lambda_role.arn
  handler       = "app.lambda_handler"
  runtime       = "python3.9"
  s3_bucket     = aws_s3_bucket.my_bucket.bucket
  s3_key        = aws_s3_object.lambda_zip.key
  source_code_hash = filebase64sha256("../lambda.zip")
}
