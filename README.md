# Server Cultural Events Management System

_API REST in Python with FastAPI, PostgreSQL, TortoiseORM, as the server in the cultural services Management application_

## Getting Started 🚀

_These instructions will get you a copy of the project up and running on your local machine for development and testing purposes._

### Prerequisites 📋

_Docker is needed_

_Docker_:

On Ubuntu:

https://www.hostinger.co/tutoriales/como-instalar-y-usar-docker-en-ubuntu/

On Windows and Mac:

https://platzi.com/tutoriales/2066-docker/1779-como-instalar-docker-en-windows-y-mac/

_PostgreSQL_:

On Ubuntu:

https://www.digitalocean.com/community/tutorials/como-instalar-y-utilizar-postgresql-en-ubuntu-18-04-es

On Windows:

https://www.solvetic.com/tutoriales/article/7676-como-instalar-postgresql-en-windows-10/

On Mac:

https://programadorwebvalencia.com/instalar-postgresql-en-osx/

### Installation 🔧

_Once Docker and PostgreSQL are installed, open a terminal within the project path and execute the following command_

- On Ubuntu:

first, create the network:

```sh
sudo docker network create aplicativo
```

then the volume:

```sh
sudo docker volume create aplicativo-db
```

build the Docker image:

```sh
sudo docker-compose -f docker/Docker-compose.dev.yml build
```

then run the container:

```sh
sudo docker-compose -f docker/Docker-compose.dev.yml up

```

- On Windows (With administrator permissions):

first, create the network:

```sh
 docker network create aplicativo
```

then the volume:

```sh
docker volume create aplicativo-db
```

build the Docker image:

```sh
docker-compose -f docker/Docker-compose.dev.yml build
```

then run the container:

```sh
docker-compose -f docker/Docker-compose.dev.yml up
```

Once both commands are executed, the API will be running on port 8007 by default and ready to receive requests.

- To access the API: localhost:8007

- To access the interactive documentation: localhost:8007/docs

## Build With 🛠️

- [FastAPI](https://fastapi.tiangolo.com/es/) - The web framework used
- [Docker](https://www.docker.com) - Deployment

## License 📄

This project is licensed under the MIT License - see the LICENSE.md [LICENSE.md](LICENSE) file for details.
