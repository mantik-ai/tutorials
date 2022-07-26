# Create Apptainer images from Docker

**NOTE:** This tutorial is also valid for [Singularity](https://sylabs.io/singularity/). For more information on the transition from Singularity to Apptainer [see here](https://www.linuxfoundation.org/press-release/new-linux-foundation-project-accelerates-collaboration-on-container-systems-between-enterprise-and-high-performance-computing-environments/).

Apptainer and Docker are both container runtime platforms that implement the OCI standard.

While Docker is the most used platform, Apptainer (formerly known as Singularity) has been developed explicitly for HPC usage.

It is more likely to find suitable Docker images, e.g. on [dockerhub](https://hub.docker.com/) or Dockerfiles in example projects than it is to find corresponding Apptainer images.
In this tutorial we show how Apptainer images can be built from Docker images.

## Option 1: Build from local Docker image

In case you have a Docker image available locally, or you executed

```bash
sudo docker pull <image>:<tag>
```

Apptainer images can be built from images that can be accessed via your Docker daemon:

```bash
sudo apptainer build <image_name.sif> docker-daemon://<docker-image-name:image-tag>
```

This option is especially useful if you develop your own Docker images.

## Option 2: Build from remote Docker image

It is also possible to build apptainer images directly from remote Docker images:

```bash
sudo apptainer build <image_name.sif> docker://<docker-image-name:image-tag>
```

## Option 3: Build from definition file

The most flexible option to build Apptainer images is to write [definition files](https://apptainer.org/docs/user/main/definition_files.html) (also called _recipes_).

As recipes are well-documented already, we will only cover the bare necessities for building from Docker images.

### Headers and sections

Apptainer recipes are text files, commonly named `recipe.def`. They contain a header, i.e. the first lines of the file that are not part of any section, and sections.

### Header

The two relevant entries in the header for us are:

 - `Bootstrap`: Defines from which platform the base images are pulled. Interesting options are 
   1. `docker`: pull from dockerhub
   2. `docker-daemon`: use a local Docker image
 - `From`: Defines the base image to extend.

An example header could look like this:

```
Bootstrap: docker
From: python:3.7
```

### Sections

Here, only the two most frequently used sections are described briefly. For detailed documentation, [see here](https://apptainer.org/user-docs/master/definition_files.html#sections).

#### `%files`

The `files` section is used to copy files into the image. Paths are relative to the path from which `apptainer build` is executed. 

**Tip:** Do not copy to user paths. When running the image, the user directories are automatically mounted. It can lead to confusion between mounted and copied files. Good places to copy your files to are `/opt`, `/app` or `/project`.


#### `%post`

The `post` section contains steps to execute during the build. It is useful for installing additional software.

#### Example

An example recipe is given below:

```
Bootstrap: docker
From: python:3.7

%files
  README.md /opt/

%post
  pip install mantik
``` 

### Known problems

Some options from Docker can not be mapped to the Apptainer logic. For a detailed explanation [see here](https://apptainer.org/user-docs/master/singularity_and_docker.html#differences-and-limitations-vs-docker).
