# Infrastructure as Code with Terraform

**HashiCorp Terraform** is an Infrastructure as Code (IaC) tool that lets you define cloud resources in human-readable configuration files that you can version, reuse, and share.

![terraform_providers][terraform_providers]

## Motivation

Want to create exactly the same EC2 instance in 3 environments (dev, test, prod), or in 15 different regions? You can't really do it manually using the web console...
Using Terraform, it's as simple as configure the below code in a `.tf` file: 

```terraform
resource "aws_instance" "app_server" {
  ami           = "ami-0123456789abcdef0"
  instance_type = "t2.micro"

  tags = {
    Name = "some-instance"
    Terraform = "true"
  }
}
```

And perform the `terraform apply` command to provision the infrastructure in AWS. 

### IaC Benefits

- **Automated Provisioning**: Automates the creation and configuration of infrastructure, less human errors.
- **Consistent Environments**: Ensures uniformity across development, testing, and production environments.
- **Repeatable Process**: Allows for the replication of infrastructure setups, or reproduced infrastructure in a case of Disaster Recovery (RD).
- **Versioned and Documented**: IaC scripts are version-controlled, enabling teams to track changes over time and roll back to previous states if needed. 


## Install Terraform

https://learn.hashicorp.com/tutorials/terraform/install-cli?in=terraform/aws-get-started

## Talk with AWS using CLI

Before we start, let's see how to interact with the AWS API from your local machine using the AWS CLI (Command Line Interface).
This will allow you to manage AWS resources and services programmatically, in addition to using the AWS Management Console.

1. Follow AWS's official docs to [install AWS cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) on your Ubuntu machine.
2. Once installed, verify your installation by `aws --version`, and **make sure `aws-cli` version `2.*` was installed**!
3. You will then need to create credentials in the **IAM service** and configure them on your local machine before running CLI commands to interact with AWS services.
    1. Use your AWS account ID or account alias, your IAM username, and your password to sign in to the [IAM console](https://console.aws.amazon.com/iam)\.
    2. In the navigation bar on the upper right, choose your username, and then choose **Security credentials**\.
    3. In the **Access keys** section, choose **Create access key**\. If you already have two access keys, this button is deactivated and you must delete an access key before you can create a new one\.
    4. On the **Access key best practices & alternatives** page, choose your use case to learn about additional options which can help you avoid creating a long\-term access key\. If you determine that your use case still requires an access key, choose **Other** and then choose **Next**\.
    5. Set a description tag value for the access key\. This adds a tag key\-value pair to your IAM user\. This can help you identify and rotate access keys later\. The tag key is set to the access key id\. The tag value is set to the access key description that you specify\. When you are finished, choose **Create access key**\.
    6. On the **Retrieve access keys** page, choose either **Show** to reveal the value of your user's secret access key, or **Download \.csv file**\. This is your only opportunity to save your secret access key\. After you've saved your secret access key in a secure location, choose **Done**\.

4. Open a new terminal session on your local machine, and type `aws configure`. Enter the access key id and the access secret key. You can also provide the default region you are working on, and the default output format (`json`).
5. Test your credentials by executing `aws sts get-caller-identity`. This command returns details about your AWS user, which indicats a successful communication with API cli.


## Working with Terraform in AWS

> [!NOTE]
> It's recommended to create a dedicated GitHub repo for this module. 

Terraform creates and manages resources on cloud platforms through their APIs.

**Providers** are plugins that allow Terraform to interact with different platforms. 
Providers enable Terraform to create, read, update, and delete infrastructure resources in the platform you work with.
You can find all publicly available providers that Terraform can work with on the [Terraform Registry](https://registry.terraform.io/browse/providers), including AWS, Azure, GCP, Kubernetes, Helm, GitHub, Splunk, DataDog, and many more.


### Deploy a single EC2 instance

The set of files used to describe infrastructure in Terraform is known as a **Terraform configuration files** (`.tf`).

Let's provision a single AWS EC2 instance:

```terraform
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">=5.55"
    }
  }

  required_version = ">= 1.7.0"
}

provider "aws" {
  region  = "<aws-region>"
  profile = "default"  # change in case you want to work with another AWS account profile
}

resource "aws_instance" "netflix_app" {
  ami           = "<ec2-ami>"
  instance_type = "t2.micro"

  tags = {
    Name = "<instance-name>"
  }
}

```

- The `terraform` block contains Terraform settings, including the required providers used to provision infrastructure.
  In this example, the aws provider's source is defined as `hashicorp/aws`.
- The `provider` block configures the specified provider, in this case `aws`.
- The `resource` blocks to define a physical or a virtual component in your infrastructure.
  In this example, the block declares a resource of type `aws_instance` (EC2 instance) with a local name `netflix_app`.
  The resource local name is used internally by Terraform, but has no meaning in AWS. 


1. In your repo, create a file called `main.tf`, copy the above code and change it as follows:
   1. `<aws-region-code>` is the region in which you want to deploy your infrastructure.
   2. `<ec2-ami>` is the AMI you want to provision (choose an Ubuntu AMI according to your region).
   3. `<instance-name>` is the name of you EC2 instance.

2. The directory containing your `.tf` file is known as **Terraform workspace dir**.
   When first working with your TF workspace, you have to initialize it by: `terraform init`. 

   Initializing a configuration directory downloads and installs the providers defined in the configuration, which in this case is the `aws` provider.
3. Run the `terraform plan` to create an execution plan, which lets you preview the changes that Terraform plans to make to your infrastructure.
4. Apply the configuration now with the `terraform apply` command.

When you applied your configuration, Terraform wrote data into a file called `terraform.tfstate`.
Terraform stores the IDs and properties of the resources it manages in this file, so that it can update or destroy those resources going forward.
The Terraform state file is **the only way** Terraform can track which resources it manages, and often **contains sensitive information**, so you must store your state file securely, outside your version control.


> [!NOTE]
> - You can make sure your configuration is syntactically valid and internally consistent by using the `terraform validate` command.
> - Inspect the current state using `terraform show`.
> - To list all resources in the state file, perform `terraform state list`.


### Destroy infrastructure

The `terraform destroy` command terminates resources managed by your Terraform project.

You can destroy specific resource by `terraform destroy -target RESOURCE_TYPE.NAME`.

# Exercises 

### :pencil2: Change the deployed infrastructure

1. Add another tag to the `aws_instance.netflix_app` resource. Plan and apply. Can you see the updated EC2 in the AWS web console? What does **in-place** update mean? 
2. Change the instance type (e.g. from `t2.micro` to `t2.nano`). Plan and apply. Is terraform destroying your instance in order to perform the update?  
3. Update the `ami` of your instance. How many resources are going to be added or destroyed? Why?

### :pencil2: Deploy the Netflix app within your EC2 instance

Use the [`user_data`](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance#user_data) argument to configure a bash script to be executed when the instance is launching. 

```diff
resource "aws_instance" "netflix_app" {
  ...
+ user_data = file("./deploy.sh")
  ...
}
```

Create a bash script named `deploy.sh`. 
The bash script should install Docker on the machine, and run the Netflix stack in the background. 

Make sure you are able to visit the app after applying your configurations. 

**Note:** Updates to the `user_data` argument for an existing instance will trigger a stop/start of the instance by default. 


[terraform_providers]: https://exit-zero-academy.github.io/DevOpsTheHardWayAssets/img/terraform_providers.png