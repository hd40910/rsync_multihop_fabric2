# rsync_multihop_fabric2


## Introduction
Fabric2 + Patchwork based script to perform parallel copy to defined target hosts.
Milti hop is supported based on facric2 funtionalities

## Requirments
1. Python >=3.6 
2. pip3.6 install patchwork == 1.0.1


## Target Definition
```
[{
    "machine_name": "ilgss0254",
    "reload_command": "",
    "port": "22",
    "shell_type": "",
    "steps_to_auth": [
        {
            "username": "test",
            "order": 1,
            "host": "test",
            "password": "test",
            "type": "SSH",
            "port": "22"
        }
    ],
    "username": "test",
    "host": "test",
    "password": "test"
}]
```

## Usage
```
curl --location --request POST 'http://localhost:1012/copy' \
--header 'Content-Type: application/json' \
--data-raw '{
    "copy_from":"/source/test",
    "copy_to":"/target/test",
    "machine_list":["ilgss0254"]
}'
```
## Response
```
{
    "result": "success",
    "machine_list": [
        {
            "machine_name": "ilgss0254",
            "result": "success",
            "result_message": "<Copied files list>"
        }
    ]
}
```
