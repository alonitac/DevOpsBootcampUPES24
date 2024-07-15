# GitHub Actions and the simple CI/CD pipeline 

CI/CD (Continuous integration and continuous deployment) is a methodology which automates the deployment process of software project.
You'll spend fairly amount of time in your studies to discuss this topic. But for now we want to achieve a simple outcome:

**When you make changes to your code locally, commit, and push them, a new automated pipeline connects to an EC2 instance, and deploys the new version of the app.**

No need to manually connect to your EC2, no need manually install dependencies, stop the running server, pulls the new code version, and launch the server - everything from code changes to deployment is seamlessly done by an automatic process.
This is why it is called **Continuous Deployment**, because on every code change, a new version of the app is being deployed automatically.

To achieve that, we will use a platform which is part of GitHub, called **GitHub Actions**.

1. First, **get yourself familiar** with how GitHub Actions works: https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions. 
2. The GitHub Actions **Workflow** skeleton is already written for you and available under `.github/workflows/service-deploy.yaml` in the [NetflixMovieCatalog][NetflixMovieCatalog] repo. Carefully review it, and feel free to customize it according to your specific requirements.

   Note that in order to automate the deployment process of the app, the workflow should have an SSH private key that authorized to connect to your instance. Since we **NEVER** store secrets in a git repo, you should configure a **Secret** in GitHub Actions and provide it to the workflow as an environment variable, as follows:
   - Go to your project repository on GitHub, navigate to **Settings** > **Secrets and variables** > **Actions**.
   - Click on **New repository secret**.
   - Define a secret named `SSH_PRIVATE_KEY` with the private key value to connect to your EC2.
   - Take a look how this secret is being used in the workflow `service-deploy.yaml` YAML.
4. Make some changes to your app, then commit and push it. Notice how the **Netflix Movie Catalog Service Deployment** workflow automatically kicked in. Once the workflow completes successfully, your new application version should be automatically deployed in your EC2 instance. Make sure the service is working properly and reflects the code changes you've made. 

**Note:** Your EC2 instances should be running while the workflow is running. **Don't forget to turn off the machines when you're done**.



[git_gitflow]: https://exit-zero-academy.github.io/DevOpsTheHardWayAssets/img/git_gitflow.png
[NetflixMovieCatalog]: https://github.com/exit-zero-academy/NetflixMovieCatalog.git

# Exercises

### :pencil2: CI/CD for the Nginx configuration files

In this exercise, you will set up a CI/CD pipeline to automate the deployment of Nginx configuration files to your EC2 instance.
The goal is to automatically update and reload Nginx whenever you make changes to its configuration files and push them to your repository.

- Create a new GitHub repo named **NetflixInfra** and clone it locally. 
  In your repository, create a folder named `nginx-config` and place your Nginx configuration files (`default.conf`, etc.) inside it.

- Create a new workflow file under `.github/workflows/nginx-deploy.yaml` in your repository. 
  
  In the `nginx-deploy.yaml` file, write a GitHub Actions workflow that:
     - Uses the SSH private key to connect to your EC2 instance.
     - Transfers the updated Nginx configuration files from the `nginx-config` folder to the appropriate directory on your EC2 instance.
     - Restarts the Nginx service on your EC2 instance to apply the changes.

- Test the CI/CD Pipeline by making a small change to your Nginx configuration files, commit and push the changes to your repository.
  Observe the GitHub Actions workflow being triggered and completing the deployment process.
