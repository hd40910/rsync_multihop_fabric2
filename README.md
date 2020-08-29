# rsync_multihop_fabric2


## Introduction
1. Fabric2 + Patchwork based script to perform parallel copy to defined target hosts.
2. Source has to be a local file or directory.The copy is based of rsync
2. Multi hop is supported based on facric2 funtionalities.
3. Additonal parameter supported by rsync can be passed as defined by https://fabric-patchwork.readthedocs.io/en/latest/.
4. Just additonal keys into the the payload and it will get passed to Patchwork. Example : "delete : true " will enable the delete functinality of rsync

## Requirments
1. Python >=3.6 
2. pip3.6 install patchwork == 1.0.1
3. pip3.6 install Flask==0.12.4
4. pip3.6 install futures==3.1.1


## Target Definition
```
#vi targets.json

[{
    "machine_name": "ilgss0254", --> Unique name
    "reload_command": "",
    "port": "22",
    "shell_type": "",
    "steps_to_auth": [ --> Multi Hop details
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
python3.6 main.py
```

```
Basic:

curl --location --request POST 'http://localhost:1012/copy' \
--header 'Content-Type: application/json' \
--data-raw '{
    "copy_from":"/source/test",
    "copy_to":"/target/test",
    "machine_list":["ilgss0254"]
}'

With keyargs:

curl --location --request POST 'http://localhost:1012/copy' \
--header 'Content-Type: application/json' \
--data-raw '{
    "copy_from":"/source/test",
    "copy_to":"/target/test",
    "machine_list":["ilgss0254"]
    "delete":"true",
    "ssh_opts": "--rsh"
}'
```


```
CLI based:

import rsync_multihop_fabric2.main

result = main.copy({
    "copy_from":"/source/test",
    "copy_to":"/target/test",
    "machine_list":["ilgss0254"]
});

print(result)
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
