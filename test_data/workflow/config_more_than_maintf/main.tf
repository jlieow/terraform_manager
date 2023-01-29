provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      hashicorp-learn = "resource-targeting"
    }
  }
}

resource "ri-1" "extra" {
  length    = 3
  separator = "-"
  prefix    = "learning"
}

resource "ri-1" "try" {
  length    = 3
  separator = "-"
  prefix    = "learning"
}

module "mi-1" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "3.3.0"

  bucket = random_pet.bucket_name.id
  acl    = "private"
}

module "mi-2" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "3.3.0"

  bucket = random_pet.bucket_name.id
  acl    = "private"
}

resource "ri-2" "extra" {
  count = 4

  length    = 5
  separator = "_"
  prefix    = "learning"
}

module "mi-24" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "3.3.0"

  bucket = random_pet.bucket_name.id
  acl    = "private"
}