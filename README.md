# Postgres Pilot

Postgres Pilot is a simple controller written in Python that manages the creation and deletion of PostgreSQL databases based on Kubernetes resources named `PostgresqlDatabase`. This project aims to simplify the management of PostgreSQL databases in a Kubernetes environment.

## Features

- Automatically creates a PostgreSQL database when a `PostgresqlDatabase` resource is created in the Kubernetes cluster.
- Automatically deletes the corresponding PostgreSQL database when the `PostgresqlDatabase` resource is deleted.

## Prerequisites

- Kubernetes cluster (v1.19 or later recommended)
- Python 3.7 or later
- `kubectl` command-line tool
- PostgreSQL server
- Access to the Kubernetes API

## Installation in kubernetes cluster

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ninoamine/PostgresPilot.git
   cd PostgresPilot
   ```
2. **Configure Postgresql server connection:**

   ```bash
    cd manifests
    vim deployment.yaml
   ```
3. **Install PostgresPilot:**

   ```bash
    cd ..
    kubectl apply -f manifests

## Usage

**Creating a PostgreSQL Database:**

To create a PostgreSQL database, define a PostgresqlDatabase resource and apply it to your Kubernetes cluster.

   ```yaml
    apiVersion: postgrespilot.io/v1alpha1
    kind: PostgresqlDatabase
    metadata:
      name: toto
    spec:
      databaseName: toto
  ```

## RoadMap

- Management of postgresqlDatabase ressource status
- Devloppement of webhook the stop updating existing databases
- Adding unit test to the code