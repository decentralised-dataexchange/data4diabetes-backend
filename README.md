# Data4Diabetes Backend

## Development

## Setup environment

This project uses Pipenv for package management.

Run the following command to setup the virtual environment.

```bash
pipenv shell
```

Run the following command to install the dependencies to current virtual environment.

```bash
pipenv sync
```

Create `.env` file with following content:

```bash
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_FROM_MOBILE_NUMBER=
```

## Docker

Run the following command to run the project using docker-compose.

```bash
docker-compose up
```