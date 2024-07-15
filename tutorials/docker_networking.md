# The Bridge network driver

The Bridge network driver is the default network driver for Docker containers.
It creates a private internal network on your host system, allowing containers to communicate with each other while isolating them from external networks. 

1. Create a custom Bridge Network

```bash
docker network create mynet
```

2. Run Containers on the Bridge Network

```bash
docker run -d --name nginx1 --network mynet nginx
docker run -d --name nginx2 --network mynet nginx
```

3. Test Communication Between Containers

```bash
docker exec -it nginx1 /bin/bash
```

Inside the container, use `ping` to test the connection (install `ping` if needed):

```bash
ping nginx2
```

4. Inspect the Bridge Network

```bash
docker network inspect mynet
```

> [!NOTE]
> Networking in Docker is a broad topic out of our bootcamp scope. 
> Docker uses the Container Networking Model (CNM) to manage networking across its [various drivers](https://docs.docker.com/network).

# Exercises

### :pencil2: Nginx, NetflixFrontend, NetflixMovieCatalog

Your goal is to run the following architecture (locally):

![][docker_nginx_frontend_catalog]

- The Nginx and NetflixFrontend should be connected to a custom bridge network called `public-net-1` network.
- In addition, the NetflixFrontend app the NetflixMovieCatalog should be connected to a custom bridge network called `private-net-1` network.
- The Nginx should talk with NetflixFrontend using the `netflix-frontend` hostname.
- The NetflixFrontend app should talk to the NetflixMovieCatalog using the `netflix-catalog` hostname.


[docker_sandbox]: https://exit-zero-academy.github.io/DevOpsTheHardWayAssets/img/docker_sandbox.png
[docker_cache]: https://exit-zero-academy.github.io/DevOpsTheHardWayAssets/img/docker_cache.png
[docker_nginx_frontend_catalog]: https://exit-zero-academy.github.io/DevOpsTheHardWayAssets/img/docker_nginx_frontend_catalog.png