# LangchainStudy
My Langchain study

# Troubleshooting
## AWS Layer environment variables 
In Lambda page > Configuration > Environment variables
```
LINE_CHANNEL_ACCESS_TOKEN
LINE_CHANNEL_SECRET
OPENAI_API_KEY
SERPAPI_API_KEY
```

## How to create layer?
0. If use Mac M1 chip, need to use docker to build layer in arm64 environment
```
docker pull arm64v8/ubuntu
docker run -it arm64v8/ubuntu

# in docker
root@3e836bc53a63:/# lsb_release -a
No LSB modules are available.
Distributor ID:	Ubuntu
Description:	Ubuntu 22.04.3 LTS
Release:	22.04
Codename:	jammy
root@3e836bc53a63:/# uname -a
Linux 3e836bc53a63 5.10.76-linuxkit #1 SMP PREEMPT Mon Nov 8 11:22:26 UTC 2021 aarch64 aarch64 aarch64 GNU/Linux
```

1. Install requirements
```
python -m venv aws-lambda
source aws-lambda/bin/activate
pip install -r requirements.txt

deactivate
```
If `pip install multidict` show this error in python3.12 arm64 env
```
Building wheels for collected packages: PyYAML, multidict

...

ERROR: Could not build wheels for multidict, which is required to install pyproject.toml-based projects
```

Try
```
sudo apt-get install python3.12-dev
```

2. Wrap in to zip
File path should be `python/lib/python3.12/site-packages/{install_here}`
```
zip -r my-layer.zip python
```

3. Copy out zip and upload to AWS sebsite
```
docker cp 3e836bc53a63:{path_of_my-layer.zip} {local_path}
```