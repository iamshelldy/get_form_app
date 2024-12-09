# GetForm App

## Description
A web application for defining a form template.

A form template is a structure that is defined by a unique set of fields, indicating their types. For example,
```
{
    "name": "Form template name",
    "field_name_1": "email",
    "field_name_2": "phone"
}
```

This application is developed based on FastAPI and connects to MongoDB. MongoDB can be run both on the host machine and in a Docker container.

The application supports setting up a connection to MongoDB via environment variables.

## Tech Stack

- FastAPI
- Uvicorn
- Pydantic
- Motor (asynchronous engine for MongoDB)

## Installation

### Prerequisites

- [Python 3.10 or higher](https://www.python.org/downloads/)
- [MongoDB](https://www.mongodb.com/docs/manual/installation/)
- [Docker (optional, for containerized deployment)](https://docs.docker.com/engine/install/)

### Clone the Repository

```bash
git clone https://github.com/iamshelldy/get_form_app.git
cd get_form_app
```

If you have installed MongoDB on your machine, open /etc/mongod.conf and add IP address of Docker Bridge Network:
```yaml
net:
  bindIp: localhost, 172.17.0.1
  port: 27017
```
and restart MongoDB:
* on Linux:
```sh
sudo systemctl restart mongod  # or
sudo service mongod restart
```
* on Windows:
  - Open the Run dialog (press Windows key + R).
  - Type services.msc and press Enter. The Services window will open.
  - Locate the service named "MongoDB".
  - Right-click on the service and select "Restart".

Next u have two options:
* [Use Python Virtual Environment](#local-setup)
* [Use Docker](#docker-deployment)

### Local Setup

#### Create a Virtual Environment:
```bash
python3 -m venv venv  
source venv/bin/activate  # On Windows: venv\Scripts\activate  
```

#### Install Dependencies:
```bash
pip install -r requirements.txt
```

#### Run the Application:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

#### Troubleshooting
If u see error like this.
```sh
pymongo.errors.ServerSelectionTimeoutError: localhost:27017: [Errno -2]
Name orservice not known (configured timeouts: socketTimeoutMS: 5000.0ms,
connectTimeoutMS: 5000.0ms), Timeout: 30s, Topology Description:
<TopologyDescription id: 67573be4febf7ec8f018b2a4, topology_type: Unknown,
servers: [<ServerDescription ('1722.17.0.1', 27017) server_type: Unknown,
rtt: None, error=AutoReconnect('1722.17.0.1:27017: [Errno -2] Name or service
not known (configured timeouts: socketTimeoutMS: 5000.0ms, connectTimeoutMS:
5000.0ms)')>]>
```
try to set environment variable MONGO_URI:
```sh
env MONGO_URI="mongodb://172.17.0.1:27017"  # Linux
SET MONGO_URI="mongodb://host.docker.internal:27017"  # Windows
```
and then retry to [run application](#run-the-application).

### Docker Deployment

#### Build the Docker Image:
```sh
docker build -t get_form_app .
```

#### Run the Docker Container:
```sh
docker run -p 8000:8000 get_form_app
```

#### Troubleshooting
If u see error like this.
```sh
pymongo.errors.ServerSelectionTimeoutError: localhost:27017: [Errno -2]
Name orservice not known (configured timeouts: socketTimeoutMS: 5000.0ms,
connectTimeoutMS: 5000.0ms), Timeout: 30s, Topology Description:
<TopologyDescription id: 67573be4febf7ec8f018b2a4, topology_type: Unknown,
servers: [<ServerDescription ('1722.17.0.1', 27017) server_type: Unknown,
rtt: None, error=AutoReconnect('1722.17.0.1:27017: [Errno -2] Name or service
not known (configured timeouts: socketTimeoutMS: 5000.0ms, connectTimeoutMS:
5000.0ms)')>]>
```
try to set environment variable MONGO_URI when starting Docker container:
```sh
docker run -e MONGO_URI="172.17.0.1/27017" -p 8000:8000 get_form_app # Linux
docker run -e MONGO_URI="host.docker.internal/27017" -p 8000:8000 get_form_app # Windows
```

### Run tests
```sh
python -m unittest discover tests
```
