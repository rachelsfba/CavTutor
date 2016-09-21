Project Goal
===
CavTutor tutoring marketplace web application for U.Va. CS 4501: Internet Scale Applications that is meant to illustrate concepts of scalability and best-practice full stack development for Internet-based applications. Our application will provide basic functionality to connect tutors with tutees for courses at any arbitrary instituion.

Authors
===
Richard Shaw \<rcs8vq@virginia.edu\>

Matthew Schaeffer \<mbs5mz@virginia.edu\>

Daniel Saha \<drs5ma@virginia.edu\>

API Usage
===
Currently, an API services layer is partially committed for some models.

`Institutions` and `Users` both provide a mechanism for creating new objects and
looking up existing ones.

User Model
---
To create a new `User` object, `POST` to:

    http://localhost:80/api/v1/users/create

To retrieve an existing `User` object, visit

    http://localhost:80/api/v1/users/<user_id>

where `<user_id>` is the id of a `User`.

Institution Model
---
To create a new `Institution` object, `POST` to:

    http://localhost:80/api/v1/institutions/create

To retrieve an existing `Institution` object, visit

    http://localhost:80/api/v1/institutions/<inst_id>

where `<inst_id>` is the id of a `Institution`.


Instantiation
===
To run a development instance of this project, spin up your own mysql container
and name it `db`.

Then, clone this repository and start up our docker containers with

    $ docker-compose up

To use the site, simply point your browser (or CLI tool, such as `curl`) to [localhost](http://localhost:80/).
