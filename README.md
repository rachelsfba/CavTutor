Project Description
===
CavTutor is a web application for [CS 4501: Internet Scale Applications](https://github.com/thomaspinckney3/cs4501) meant to
illustrate concepts of scalability and best-practice full stack development for
Internet-based applications. Our application will provide basic functionality to
connect tutors with tutees for courses at any arbitrary institution.

Authors
===
Richard Shaw \<rcs8vq@virginia.edu\>

Matthew Schaeffer \<mbs5mz@virginia.edu\>

Daniel Saha \<drs5ma@virginia.edu\>

Networks
===
We use two docker networks, a user-facing network which contains front-end
docker containers, and a back-end network, which is meant to be inaccessible
to users.

 - `cavtutor_frontend` -- contains `www`, `ux`
 - `cavtutor_backend` -- contains `ux`, `api_v2`, `api_static`, and `mysql` (see next section)

Note that the user experience layer is the "middle man" between the two
networks, being the only docker container on both.

Important Note for `mysql` Docker
---
Please note that your external `mysql` docker container must be on the same
docker network as ours. To connect `mysql` to the network, run

    $ docker network connect cavtutor_backend mysql

If you get an error, you may need to try a different network. To list all active
networks, run

    $ docker network ls

Description of Docker Containers
===
There are currently 4 docker containers created by running `docker-compose up`
on our project, in addition to the pre-requisite MariaDB docker instance named
`mysql`; these are

0. `mysql` -- the low-level docker image container for our MariaDB database
1. `api` -- our secondary-level services API that talks to our database directly
   (port `8003`)
1. `api_static` -- serves static files for API admin page and REST web API (port
   `8002`)
2. `ux` -- an abstract tertiary-level user experience layer that communicates
   between our client-facing µ-services (`www`, `ios`, `android`, etc.) (port
   `8001`)
3. `www` -- a client-facing docker image that serves HTML-based content for
   human consumption; aimed at desktop web browsers (port `8000`)

User Stories
====
Refer to [doc/user_stories.md](doc/user_stories.md) for documented user stories.

Unit and Integration Tests
====
Currently, some unit tests are bundled which are aimed at the API-layer of our
application. In the future, integration testing will focus on the user
experience layer (it is difficult to do this because a separate API instance is
necessary for test isolation from the UX layer). For now, you may only run tests by
attaching to the `api` docker container, i.e.

    $ docker exec -it api bash

and then running `python app/manage.py test app` inside the docker container.

Dockerfiles
====
We currently use two customized `Dockerfiles`:

 - `build/Dockerfile-nginx-reverse-proxy`: used on the `api_handler` docker
   container (not yet functional)
 - `build/Dockerfile-restful-proxy`: used on main Django containers (`www`,
   `ux`, `api_v2`)

Fixtures
===
We use Django fixtures to prepopulate the given database instance with our test
data. A Django superuser is created, with username `root` and password `root`.

Project Instantiation
===
To run a development instance of this project, spin up your own MySQL/MariaDB container
and call it `mysql`.

Then, clone this repository and start up our docker containers with

    $ docker-compose up

To use the site, simply point your browser (or CLI tool, such as `curl`) to
[localhost:8000](http://localhost:8000/).
