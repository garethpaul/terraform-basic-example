# ---------------------------------------------------------------------------------------------------------------------
# ENVIRONMENT VARIABLES
# Define these secrets as environment variables
# ---------------------------------------------------------------------------------------------------------------------

# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY

# ---------------------------------------------------------------------------------------------------------------------
# OPTIONAL PARAMETERS
# ---------------------------------------------------------------------------------------------------------------------

variable "server_port" {
  description = "The port the server will use for HTTP requests"
  type        = number
  default     = 8080

  validation {
    condition     = var.server_port > 0 && var.server_port < 65536
    error_message = "server_port must be between 1 and 65535."
  }
}

variable "allowed_cidr_blocks" {
  description = "CIDR blocks allowed to reach the example web server"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}
