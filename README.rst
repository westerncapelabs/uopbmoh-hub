uopboh-hub
=======================================

University of Pennsylvania / MOH Botswana Partnership - TB Training Monitoring & Evaluation system

A central data hub accessible from modern desktop and mobile web browsers that provides:

* Clinician registration (self-driven and administrator driven)
* Quiz entry management (simple text driven)
* Broadcast quiz capability (to drive clinicians to quizzes)
* Response reporting (metric dashboards and tabular results display)


Pre-reqs:

* [postgresql](http://www.postgresql.org)


Setup and test:

```sh
$ git clone git@github.com:westerncapelabs/uopboh-hub.git
$ cd uopboh-hub
$ psql postgres -c "CREATE DATABASE uopboh_hub"
$ pyenv virtualenv 3.4.2 uopboh-hub
$ pyenv shell uopboh-hub
(uopboh-hub) $ pip install -r requirements.txt
(uopboh-hub) $ pip install -r requirements-dev.txt
(uopboh-hub) $ ./manage.py migrate
```

Run
```sh
(uopboh-hub) $ export DEBUG=True
(uopboh-hub) $ ./manage.py createsuperuser
(uopboh-hub) $ ./manage.py runserver  
```
