# IOMETE SDK

This is the IOMETE SDK for Python. 
It provides convenient access to the IOMETE API from applications written in the Python language.

## Installation

Install the package with:

```bash
pip install iomete-sdk
```

## Usage

### Spark Job API

Import and initialize the client:
```python
from iomete_sdk.spark import SparkJobApiClient
from iomete_sdk.api_utils import ClientError

HOST = "<YOUR_DATAPLANE_HOST>" # https://dataplane-endpoint.example.com
API_KEY = "<YOU_IOMETE_API_KEY>"

job_client = SparkJobApiClient(
    host=HOST,
    api_key=API_KEY,
)
```

Create a new job:
```python
response = job_client.create_job(payload={
        "name": "job-name",
        "template": {
            "main_application_file": "local:///opt/spark/examples/jars/spark-examples_2.12-3.2.1-iomete.jar",
            "main_class": "org.apache.spark.examples.SparkPi",
            "arguments": ["10"]
        }
    })

job_id = response["id"]
```

Get jobs:
```python
response = job_client.get_jobs()
```

Get job:
```python
response = job_client.get_job(job_id=job_id)
```

Update job:
```python
response = job_client.update_job(job_id=job_id, payload={
        "template": {
            "main_application_file": "local:///opt/spark/examples/jars/spark-examples_2.12-3.2.1-iomete.jar",
            "main_class": "org.apache.spark.examples.SparkPi",
            "arguments": ["10"]
        }
    })
```

Delete job:
```python
response = job_client.delete_job(job_id=job_id)
```


Submit job run:
```python
response = job_client.submit_job_run(job_id=job_id, payload={})
```

Cancel job run:
```python
response = job_client.cancel_job_run(job_id=job_id, run_id=run_id)
```

Get Job Runs:
```python
response = job_client.get_job_runs(job_id=job_id)
```

Get Job Run:
```python
response = job_client.get_job_run(job_id=job_id, run_id=run_id)
```

Get Job Run Logs:
```python
response = job_client.get_job_run_logs(job_id=job_id, run_id=run_id)
```

Get Job Run Metrics:
```python
response = job_client.get_job_run_metrics(job_id=job_id, run_id=run_id)
```



