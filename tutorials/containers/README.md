# Create apptainer images from docker

**NOTE:** This tutorial is also valid for [singularity](https://sylabs.io/singularity/). For more information on the transition from singularity to apptainer, [see here](https://www.linuxfoundation.org/press-release/new-linux-foundation-project-accelerates-collaboration-on-container-systems-between-enterprise-and-high-performance-computing-environments/).

Apptainer and Docker are both container runtime platforms that implement the OCI standard.

While Docker is the most used platform, apptainer (formerly known as singularity) has been developed explicitly for HPC usage.

It is much more likely to find suitable docker images, e.g. on [dockerhub](https://hub.docker.com/) or Dockerfiles in example projects than it is to find corresponding apptainer images.
In this tutorial we show how apptainer images can be built from Docker images.

## Option 1: Build from local Docker image

In case you have a docker image available locally, or you executed

```bash
sudo docker pull <image>:<tag>
```

apptainer images can be built from images that can be accessed via your docker daemon:

```bash
sudo apptainer build <image_name.sif> docker-daemon://<docker-image-name:image-tag>
```

This option is especially usefull if you develop your own Docker images.

## Option 2: Build from remote Docker image

It is also possible to build apptainer images directly from remote docker images:

```bash
sudo apptainer build <image_name.sif> docker://<docker-image-name:image-tag>
```

## Option 3: Build from recipe

The most felxible option to build apptainer images is to define [recipes]().

As recipes are well-documented already, we will only cover the bare necessities for building from Docker images.

### Headers and sections

Apptainer recipes are text files, commonly named `recipe.def`. They contain a header, i.e. the first lines of the file that are not part of any section, and sections.

### Header

The two relevant entries in the header for us are:

 - `Bootstrap`: Defines from which platform the base images are pulled. Interesting options are `docker` (pull from dockerjub) and `docker-daemon` (use a local docker image).
 - `From`: Defines the base image to extend.

An example header could look like this:

```
Bootstrap: docker
From: python:3.7
```

### Sections

Here, only the two most frequently used sections are described briefly. For detailed documentation, [see here](https://apptainer.org/user-docs/master/definition_files.html#sections).

#### `%files`

The `files` section is used to copy files into the image. Paths are relative to path from which `apptainer build` is executed. 

Tip: do not copy to user paths, as when running the image, the user directories are automatically mounted. It can lead to confusion between mounted and copied files. A good place to copy your files to is `/opt` or `/project`.


#### `%post`

The `post` section contains steps to execute after files have been copied. It is useful for installing additional software.

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

Some options from Docker can not be mapped to the apptainer logic. For a detailed explanation, [see here](https://apptainer.org/user-docs/master/singularity_and_docker.html#differences-and-limitations-vs-docker).
