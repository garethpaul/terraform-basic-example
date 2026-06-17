# ---------------------------------------------------------------------------------------------------------------------
# ENVIRONMENT VARIABLES
# Define these secrets as environment variables
# ---------------------------------------------------------------------------------------------------------------------

# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY

# ---------------------------------------------------------------------------------------------------------------------
# OPTIONAL PARAMETERS
# ---------------------------------------------------------------------------------------------------------------------

variable "aws_region" {
  description = "AWS region where the example resources will be created"
  type        = string
  default     = "us-east-2"

  validation {
    condition     = can(regex("^[a-z]{2}-[a-z]+-[0-9]+$", var.aws_region))
    error_message = "aws_region must look like a valid AWS region, such as us-east-2."
  }
}

variable "ami_id" {
  description = "Optional AMI ID override; null selects the latest regional Amazon Linux 2023 x86_64 image"
  type        = string
  default     = null
  nullable    = true

  validation {
    condition     = var.ami_id == null || can(regex("^ami-([0-9a-f]{8}|[0-9a-f]{17})$", var.ami_id))
    error_message = "ami_id must use an 8- or 17-character lowercase hexadecimal AWS AMI ID."
  }
}

variable "instance_type" {
  description = "EC2 instance type for the example web server"
  type        = string
  default     = "t2.micro"

  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9-]*[.][a-z0-9]+$", var.instance_type))
    error_message = "instance_type must look like an EC2 instance type, such as t2.micro."
  }
}

variable "server_port" {
  description = "The port the server will use for HTTP requests"
  type        = number
  default     = 8080

  validation {
    condition = (
      var.server_port > 0 &&
      var.server_port < 65536 &&
      var.server_port == floor(var.server_port)
    )
    error_message = "server_port must be a whole number between 1 and 65535."
  }
}

variable "allowed_cidr_blocks" {
  description = "IPv4 CIDR blocks allowed to reach the example web server; leave empty to disable inbound HTTP"
  type        = list(string)
  default     = []

  validation {
    condition = alltrue([
      for cidr in var.allowed_cidr_blocks :
      can(cidrnetmask(cidr)) &&
      cidr == try(cidrsubnet(cidr, 0, 0), "")
    ])
    error_message = "allowed_cidr_blocks must contain only canonical IPv4 CIDR blocks."
  }
}

variable "resource_tags" {
  description = "Common tags applied to example resources for ownership and cleanup"
  type        = map(string)
  default = {
    ManagedBy = "terraform"
    Project   = "terraform-basic-example"
  }

  validation {
    condition = (
      length(var.resource_tags) > 0 &&
      alltrue([
        for key, value in var.resource_tags :
        length(trimspace(key)) > 0 &&
        length(trimspace(value)) > 0 &&
        length(key) <= 128 &&
        length(value) <= 256 &&
        !startswith(lower(key), "aws:")
      ]) &&
      length(setunion(toset(keys(var.resource_tags)), toset(["Name"]))) <= 50
    )
    error_message = "resource_tags must produce at most 50 final tags including Name, contain non-empty keys up to 128 characters and values up to 256 characters, and not use the reserved aws: prefix."
  }
}
