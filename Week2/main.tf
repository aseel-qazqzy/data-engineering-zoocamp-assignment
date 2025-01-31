terraform {
   required_providers {
    google = {
        source = "hashicorp/google"
        version = "6.17.0"
    }
   }
}

provider "google"{
    project = var.project_id
    region = var.region
    credentials = file(var.credentias)
    
}