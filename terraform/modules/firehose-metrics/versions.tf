terraform {
  required_version = ">= 1.3"

  required_providers {

    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0.0"
    }

    newrelic = {
      source  = "newrelic/newrelic"
      version = ">= 3.0.0"
    }
  }
}