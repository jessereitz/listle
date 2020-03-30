# Listle

An easy back-end for collecting arbitrary information for an email list or campaign.

## Quick Start Using Cloud Run

The easiest way to deploy Listle is on Google Cloud Platform's [Cloud Run](https://cloud.google.com/run). To deploy Listle on GCP using the Firestore Connector:

1. Install the [`gcloud`](https://cloud.google.com/sdk/install) utility,
2. Log in using
```bash
$ gcloud auth login
```

3. Set your desired project
```
$ gcloud config set project <PROJECT_ID>
```

4. Enable Firestore (if not already enabled)
    1. Go to Firestore in your GCP Console
    2. Choose `Select Native Mode`

5. Deploy the Listle service on Cloud Run
```bash
$ gcloud run deploy --image gcr.io/rereitz-listle/listle --platform=managed --set-env-vars=ENABLED_CONNECTORS=firestore
```

6. Make sure Listle is up and running
```bash
$ curl https://<cloud_run_service_url>/health
# healthy
```

## Concepts

### Records

When a `POST` request is sent to Listle, a Record is generated. A Record contains the entire JSON body of the request as well as some additional meta-data about the request.

For example:
```json
{
    "id": "uuid identifier",
    "meta": {
        "charset": "utf-8",
        "url": "https://listle.url/",
        "datetime": "2020-03-30T02:54:25.723903+00:00",
        "headers": {"Host": "listle.url"},
        "user_agent": {
            "browser": "Chrome",
            "language": "en-us",
            "platform": null,
            "string": null,
            "version": null
        }
    },
    "fields": {
        "json_field_1": "value 1",
        "json_field_2": "value 2"
    }
}
```

### Connectors

Connectors are what actually process generated Records. A Record will be given to the Connector for dispatch and processing.

Enable Connectors using the `ENABLED_CONNECTORS` environment variable setting its value to a comma-separated list containing your desired connectors. For example:
```
export ENABLED_CONNECTORS=email,firestore
```

#### Email

`ENABLED_CONNECTORS=email`

Send an email each time a Record is generated. The Connector sends email via SMTP and requires some configuration. Set the following environment variables when running Listle:

##### Required Environment Variables
| Var Name | Description |
| -------- | ----------- |
| `FROM_EMAIL` | The address from which the email will be sent |
| `TO_EMAIL` | The address to which the email will be sent |
| `EMAIL_HOST` | The hostname of your SMTP server |
| `EMAIL_PORT` | The port of your SMTP server (eg. `465`) |
| `EMAIL_USER` | The username of your SMTP credentials |
| `EMAIL_PASSWORD` | The password of your SMTP credentials |


#### Firestore

`ENABLED_CONNECTORS=firestore`

Create a Firestore document for each Record created. Each Record document will be stored in a collection named `records`.


## Endpoints

### POST `/`

Create a Record. All fields in the JSON body will be saved to the Record's `fields` attribute.


### GET `/health`

A very simple health check. This merely returns `healthy` if the server is up and running. It doesn't do any status checks for any enabled Connectors.
