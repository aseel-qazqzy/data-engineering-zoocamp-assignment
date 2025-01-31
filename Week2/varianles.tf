variable "credentias" {
    description = "The path to the service account key file"
    type = string
    default = "~/.google/credentials/google_credentials.json"
}

variable "location" {
    description = "The location of the GCP resources"
    type = string
    default = "europe-west1"
  
}

variable "project_id" {
    description = "The GCP project ID"
    type = string
    default = "pivotal-surfer-449302"
  
}

variable "region" {
    description = "The region of the GCP resources"
    type = string
    default = "europe-west1"
  
}

variable "gcd_bucket_name" {
    description = "The name of the GCS bucket"
    type = string
    default = "tf-state-bucket"
  
}

variable "storage_calass" {
    description = "The storage class of the GCS bucket"
    type = string
    default = "STANDARD"
}