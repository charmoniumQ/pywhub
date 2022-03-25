# Contributing to this repository

pywhub is open-source software distributed under the MIT license. Contributions are welcome.


## Setting up the WorkflowHub Docker image

The GitHub Actions workflow runs tests against a local WorkflowHub instance brought up via the `fairdom/seek:workflow` Docker image. Since the `workflow` tag is periodically overwritten in the upstream image, we tag the image as `crs4/seek:workflow-pywhub` and use that instead, so we can control its updates.

The WorkflowHub image needs some configuration before it can be used for testing. A snapshot of the relevant directories after configuration is available in `crs4/seek:workflow-pywhub-data`. To get a preconfigured WorkflowHub instance, do the following:

```
docker run -v /seek/filestore -v /seek/sqlite3-db --name hubdata crs4/seek:workflow-pywhub-data bash
docker run -d -p 3000:3000 --volumes-from hubdata --name hub crs4/seek:workflow-pywhub
```

The configuration stored in `crs4/seek:workflow-pywhub-data` includes:

* workflows enabled
* `admin` user with password `0123456789`
* `pywhub` user with password `0123456789` and API key `gsBPTvcPk9EruYb41jY18DMr3ATfzSEaOoqvVutF`

A simple tool to wait until the server is ready is available under `tools`:

```
python tools/wait_for_hub.py -u http://localhost:3000
```

Now you can run the unit tests:

```
export WHUB_URL=http://localhost:3000
export WHUB_API_KEY=gsBPTvcPk9EruYb41jY18DMr3ATfzSEaOoqvVutF
pytest tests
```

## Regenerating the Docker images

From time to time, the Docker images might need regenerating, for instance if there's a change in the WorkflowHub API. Get the latest upstream image and run it:

```
docker pull fairdom/seek:workflow
docker tag fairdom/seek:workflow crs4/seek:workflow-pywhub
docker run -d -p 3000:3000 --name hub crs4/seek:workflow-pywhub
python tools/wait_for_hub.py -u http://localhost:3000
```

Open your browser at `http://localhost:3000` and configure WorkflowHub:

* Fill in the form to create the `admin` user
* Enable workflows: click on the drop-down menu at the top right and select "Server admin"; click on "Enable/disable features"; tick "Workflows enabled" under "Resource Types"
* Use the "Create" menu at the top to create an institution, then create a project called "Testing" (you can set the associated institution to the one just created)
* In a new private window, open `http://localhost:3000` and register as `pywhub`; click on the top right menu and select My profile > Actions > API tokens; generate an API token and use it to replace the current value in this guide and in the GitHub Actions workflow
* Back in the previous window, add `pywhub` to the "Testing" project: Browse > Projects > Testing > Actions > Administer project members, then fill in the form on the right

Now build the image containing the snapshots of the volumes and push everything to Docker Hub:

```
docker run --user $(id -u):$(id -g) --rm --volumes-from hub -v /tmp:/tmp ubuntu bash -c 'for d in filestore sqlite3-db; do tar -C / -cvf /tmp/${d}.tar seek/${d}; done'
docker run -d -v /tmp:/tmp --name hubdata ubuntu bash -c 'for d in filestore sqlite3-db; do tar -C / -xvf /tmp/${d}.tar; done'
docker commit hubdata crs4/seek:workflow-pywhub-data
docker rm hubdata
docker push crs4/seek:workflow-pywhub
docker push crs4/seek:workflow-pywhub-data
```
