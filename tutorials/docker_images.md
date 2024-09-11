# Docker Images

## Docker registry

Where do the images we've run in the previous module come from?

The images used in Docker, including the ones you've run in the previous module, typically come from **Docker registries**.
A Docker registry is a centralized repository for storing and distributing container images.
It serves as a hub where you can find pre-built container images created by others or upload and share your own images.

By default, Docker pulls images from the [DockerHub registry](https://hub.docker.com/), which is a public registry provided by Docker. 
Docker Hub hosts a vast collection of official and community-contributed images for a wide range of applications and operating systems.
It is a popular source for finding and sharing container images.

However, Docker also allows you to work with **private registries**. Organizations often set up private registries to store proprietary or sensitive container images.
Private registries offer control over image distribution, access control, and integration with other deployment pipelines or processes.

## Image tags 

In Docker, **image tags** are labels attached to container images that help identify specific versions, variations, or configurations of an image.
They allow users to differentiate and reference different image versions or variations based on the tags assigned to them.

By default, when pulling an image without specifying a tag, Docker assumes the `latest` tag.
This tag represents the most recent version of the image available in the repository.

```console
$ docker pull python
Using default tag: latest
latest: Pulling from library/python
4eedd9c5abf7: Pull complete 
9cdadd40055f: Pull complete 
2a12d0031f3f: Pull complete 
24685c45a066: Pull complete 
6ba57ec00f34: Pull complete 
71bcc9787aa7: Pull complete 
Digest: sha256:30f9c5b85d6a9866dd6307d24f4688174f7237bc3293b9293d590b1e59c68fc7
Status: Downloaded newer image for python:latest
docker.io/library/python:latest
```

The above command pulls the latest version of the `python` docker image. 

We can also notice the image SHA digest, and the full URI address:

- **Image SHA digest** is a unique identifier calculated from the contents of a Docker image. It represents the specific version and content of the image, providing a reliable reference for ensuring image integrity, version control, and reproducibility.
- The image full **URI address** is `docker.io/library/python:latest`.

It's important to note that relying solely on the `latest` tag may lead to unexpected behavior or compatibility issues, as it may change over time as new versions are released.
Alternatively, you want to explicitly specify a version tag:

```console
$ docker pull python:3.9.16
3.9.16: Pulling from library/python
918547b94326: Already exists 
5d79063a01c5: Already exists 
4eedd9c5abf7: Already exists 
9cdadd40055f: Already exists 
2a12d0031f3f: Already exists 
cea461a97d87: Pull complete 
a48c72dfa8c4: Pull complete 
c343b921680a: Pull complete 
Digest: sha256:6ea9dafc96d7914c5c1d199f1f0195c4e05cf017b10666ca84cb7ce8e2699d51
Status: Downloaded newer image for python:3.9.16
docker.io/library/python:3.9.16
```

## Semantic version for image tags 

While the image creator can decide the way she tags her images, many organizations (including the above `python` image you've pulled) follow specific tagging method called [**semantic version**](https://semver.org/), or **SemVer**. 

Take a look on the `python` image version: `3.9.16`. Each component has a specific meaning, given a version number `MAJOR.MINOR.PATCH`:

1. Increment the `MAJOR` version when you make **incompatible** API changes.
2. Increment the `MINOR` version when you **add functionality** in a backward compatible manner.
3. Increment the `PATCH` version when you make backward compatible **bug fixes**.

#### 🧐 Test yourself

Assume you have an app exposing an API for your clients. For each of the following changes, decide the increment:

Given version `1.14.0`:

1. What is the next version after a variable name refactor?
2. What is the next version after adding a new endpoint to the api?
3.  What is the next version after changing the api endpoint from `/uploading` to `/upload`.


## Image manipulations 

You can manage docker images is a similar way you've managed containers. 
List available images with `docker images`, pulling images from a registry using `docker pull`, pushing images to a registry with `docker push`, removing images using `docker image rm`, and inspecting image details with `docker inspect`, among others.

## Build images 

It's time to learn how to build your own images.
In the below example, we will build the [NetflixMovieCatalog][NetflixMovieCatalog] app. 

A **Dockerfile** is a text document in which you tell docker how to containerize an application.

Assume you start with a clean version of Ubuntu and want to run a Flask application.
The natural approach might involve manual installation steps such as using `apt-get` to update the system, installing Python, install app dependencies using `pip`, setting up the application environment, and configuring runtime settings.

A Dockerfile provides a declarative and automated way to define all these steps as instructions for docker to build. 
The final result after building an image according to a Dockerfile is a self-contained and portable artifact that encapsulates the application code, its dependencies, and the runtime environment. 
This image can be run as a container on any system that has Docker installed, ensuring consistent behavior and eliminating the need for manual setup and configuration.

Here's the Dockerfile you'll use as the starting point in order to pack our app into an image:

```dockerfile
FROM python:3.8.12-slim-buster
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["python3", "app.py"]
```

In your NetflixMovieCatalog repo, create a file called `Dockerfile` (note the capital `D`) and copy the above content. We will explain each line soon.
For now, let's build an image out of it.

Open up a terminal where the current working directory root dir of the repo. Then build the image using the `docker build` command:

```bash
docker build -t netflix_movie_catalog:0.0.1 .
```

The working directory from which the image is built is called the **Build context**.
In the above case, the `.` at the end of the command specifying to docker that the "current working directory", is the build context. 
The docker daemon looks by default for a file called `Dockerfile` and builds the image according to the instructions specified in the Dockerfile. 

Run a container based on your built image, the image name is `netflix_movie_catalog:0.0.1`.
The app listens to port `8080`, publish this port to the host machine, so you can visit the app from your web browser. 

## The Dockerfile

A Docker build consists of a series of ordered build instructions.

### Base image - the `FROM` instruction

All Docker images start with a **base image**, and as changes are made and new content is added to the image, new layers are added on top of the base image.
The [`FROM` instruction](https://docs.docker.com/engine/reference/builder/#from) uses the official [`python:3.8.12-slim-buster`](https://hub.docker.com/layers/library/python/3.8.12-slim-buster/images/sha256-a5a7a63d6493977b0f13b1cb3a3764dba713a49baf6b87d3a53d547c41f90b2c?context=explore) image as the base image upon which our image will be built.
This base image is a docker image itself (based on the [`debian`](https://hub.docker.com/_/debian) image), which provides a lightweight and minimalistic version of the Python runtime environment, allowing developers to build and run Python applications without the need to install Python in the image from scratch.

So, our image is based on a Python base image, which in turn based on a Debian base image. 
What is the Debian image based on?

Based on [Hindu mythology](https://en.wikiquote.org/wiki/Turtles_all_the_way_down), the Debian image rest on the back of an elephant which rested in turn on the back of a turtle,
what did the turtle rest on? Another turtle. And that turtle? 'Ah, Sahib, after that it is turtles all the way down.'.

Back to the Docker world... all images are based on the [`scratch`](https://hub.docker.com/_/scratch) "image". 
The `FROM scratch` is a special instruction used in a Dockerfile to indicate that you are starting the image from scratch, without using any existing base image.
When `FROM scratch` is specified, it means you are creating the image from the bare minimum, without including any pre-built operating system or runtime environment.

### Working dir - the `WORKDIR` instruction

The [`WORKDIR` instruction](https://docs.docker.com/engine/reference/builder/#workdir) in a Dockerfile is used to set the working directory for any subsequent instructions within the Dockerfile. 
It allows you to define the directory where commands such as `RUN`, `CMD`, `COPY`, and `ADD` will be executed.

In our example, we set the working directory inside the container to `/app`.

By setting the working directory, you avoid having to specify the full path for subsequent instructions, making the Dockerfile more readable and maintainable.

### Copying files from the build machine into the image - the `COPY` instruction

The `COPY <src> <dst>` instruction copies new files or directories from the `<src>` path in the host machine, and adds them to the filesystem of the image at the path `<dst>`.

In our example, we copy the file under the `.` path, which is the current working directory **relative to the build context**, into the image's filesystem working directory, which is `/app` according to what specified in `WORKDIR`.

### The `.dockerignore` 

The `.dockerignore` file is used to specify which files and directories should be excluded from the Docker build context when building an image.
It works similarly to `.gitignore`, where you can list patterns to match files and directories that should be ignored.

### Execute commands in the image - the `RUN` instruction

The [`RUN` instruction](https://docs.docker.com/engine/reference/builder/#run) in a Dockerfile is used to execute commands during the image build process. 
It allows you to run any valid command or script inside the image that is being created.

Naturally, after you've copied the application files, you need to install the Python dependencies specified in the `requirements.txt` file. 
The `RUN pip install -r requirements.txt` instruction does so. 

Note that `pip` is already available for you as part of the Python base image. 

### Define the command to run a container - the `CMD` instruction

The [`CMD` instruction](https://docs.docker.com/engine/reference/builder/#cmd) in a Dockerfile is used to specify the default command to run when a container based on the image is started. 
It defines the primary executable or process that should be executed within the container.

In our example, we specify the command to run when the container starts, which is `python3 app.py`.

# Exercises

### :pencil2: Push the `netflix_movie_catalog` image to DockerHub

[Create a free account](https://docs.docker.com/docker-id/) in DockerHub.

Push the built `netflix_movie_catalog:0.0.1` image to your registry.

### :pencil2: Build the availability agent

Build the availability agent app located in `availability_agent` (this app used in an exercise in Containers tutorial).

The `Dockerfile` is already written. Push the image to DockerHub. 


### :pencil2: Build the Netflix Frontend app

1. Build a Docker image of the following app: https://github.com/exit-zero-academy/NetflixFrontend. 

   This is a Node.js app. In the README you'll find instructions to build and run the app. 
   Use it as a baseline for you Dockerfile instructions. 

2. Push the image to container registry (either DockerHub or ECR). 
3. Deploy your image in a fresh new `*.nano` Ubuntu EC2 instance (pull the image and run it). 
4. In your Nginx instance, create a new `server` which routes traffic to your Netflix Frontend app. The app should be accessible from your domain, e.g.: http://netflix.devops-days-upes.com.



[NetflixMovieCatalog]: https://github.com/exit-zero-academy/NetflixMovieCatalog
[docker_layers]: https://exit-zero-academy.github.io/DevOpsTheHardWayAssets/img/docker_layers.png
[docker_cache]: https://exit-zero-academy.github.io/DevOpsTheHardWayAssets/img/docker_cache.png

