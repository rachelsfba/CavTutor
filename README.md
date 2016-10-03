Project Description
===
CavTutor is a web application for CS 4501: Internet Scale Application meant to illustrate concepts of scalability and best-practice full stack development for Internet-based applications. Our application will provide basic functionality to connect tutors with tutees for courses at any arbitrary instituion.

Authors
===
Richard Shaw \<rcs8vq@virginia.edu\>

Matthew Schaeffer \<mbs5mz@virginia.edu\>

Daniel Saha \<drs5ma@virginia.edu\>

Description of Docker Containers
===
There are currently 3 docker containers created by running `docker-compose up` on our project, in addition to the pre-requisite MariaDB docker instance named `mysql`; these are

0. `mysql` -- the low-level docker image container for our MariaDB database
1. `api` -- our secondary-level services API that talks to our database directly
2. `ux` -- an abstract tertiary-level user experience layer that communicates
   between our client-facing µ-services (`www`, `ios`, `android`, etc.)
3. `www` -- a client-facing docker image that serves HTML-based content for
   human consumption; aimed at desktop web browsers

User Stories
====
Refer to [doc/user_stories.md](doc/user_stories.md) for documented user stories.


API Usage
===
Currently, an API services layer is partially implemented for some models.

`Institution`s and `User`s both provide a mechanism for creating new objects,
updating and deleting old objects, and looking up existing ones. In future
patches, this API should extend to all of our remaining models.

User Model
---
To create a new `User` object, `POST` to

    http://localhost:8003/api/v1/users/create

To retrieve an existing `User` object, visit

    http://localhost:8003/api/v1/users/<user_id>

where `<user_id>` is the id of the `User` you wish to look up.

To update an existing `User` object, `POST` to

    http://localhost:8003/api/v1/users/update/<user_id>

where `<user_id>` is the id of the `User` record you wish to update.

Finally, to delete a `User` object, visit

    http://localhost:8003/api/v1/users/delete/<user_id>

where `<user_id>` is the id of the `User` record you wish to delete.

Institution Model
---
To create a new `Institution` object, `POST` to

    http://localhost:8003/api/v1/institutions/create

To retrieve an existing `Institution` object, visit

    http://localhost:8003/api/v1/institutions/<inst_id>

where `<inst_id>` is the id of the `Institution` you wish to look up.

To update an existing `Institution` object, `POST` to

    http://localhost:8003/api/v1/institutions/update/<inst_id>

where `<inst_id>` is the id of the `Institution` record you wish to update.

Finally, to delete a `Institution` object, visit

    http://localhost:8003/api/v1/institutions/delete/<inst_id>

where `<inst_id>` is the id of the `Institution` record you wish to delete.

Project Instantiation
===
To run a development instance of this project, spin up your own MySQL/MariaDB container
and call it `mysql`.

Then, clone this repository and start up our docker containers with

    $ docker-compose up

To use the site, simply point your browser (or CLI tool, such as `curl`) to [localhost:8000](http://localhost:8000/).
