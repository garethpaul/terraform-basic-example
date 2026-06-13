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
  description = "AMI ID to launch for the example web server"
  type        = string
  default     = "ami-0c55b159cbfafe1f0"

  validation {
    condition     = can(regex("^ami-[0-9a-f]+$", var.ami_id))
    error_message = "ami_id must look like an AWS AMI ID, such as ami-0c55b159cbfafe1f0."
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
        !startswith(lower(key), "aws:")
      ])
    )
    error_message = "resource_tags must contain non-empty keys and values and must not use the reserved aws: prefix."
  }
}
