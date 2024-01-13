# LangchainStudy
My Langchain study


## Overview
### langchain v0.1.0
```
$ python src/langchain_assistant.py
```
```
Type 'quit' to quit chat
Question >>> hello


> Entering new AgentExecutor chain...
Hello! How can I assist you today?

> Finished chain.
{'input': 'hello', 'output': 'Hello! How can I assist you today?'}
Answer >>>  Hello! How can I assist you today?
-----------------

Question >>> 台北天氣如何


> Entering new AgentExecutor chain...

Invoking: `Google_Search` with `台北天氣`


{'type': 'weather_result', 'temperature': '22', 'unit': 'Celsius', 'precipitation': '0%', 'humidity': '51%', 'wind': '23 公里/時', 'location': '台北市', 'date': '星期六 下午5:00', 'weather': '大致晴朗'}根據最新資訊，台北市目前的天氣狀況是大致晴朗，溫度約為攝氏22度，降雨機率為0%，相對濕度為51%，風速為每小時23公里。請注意天氣可能會有變化，建議您隨時留意天氣預報。

> Finished chain.
{'input': '台北天氣如何', 'output': '根據最新資訊，台北市目前的天氣狀況是大致晴朗，溫度約為攝氏22度，降雨機率為0%，相對濕度為51%，風速為每小時23公里。請注意天氣可能會有變化，建議您隨時留意天氣預報。'}
Answer >>>  根據最新資訊，台北市目前的天氣狀況是大致晴朗，溫度約為攝氏22度，降雨機率為0%，相對濕度為51%，風速為每小時23公里。請注意天氣可能會有變化，建議您隨時留意天氣預報。
-----------------

Question >>> quit
Quit chat...
```

### OpenAI Assistants API Beta
```
$python src/assistant.py 
```
```
Assistant id:  {assistant_id}
Thread id:  {thread}
Type 'quit' to quit chat
Question >>> hi, who are you
Run status: queued
Run status: in_progress
Run status: in_progress
Run status: completed
Answer >>>  Hello! I'm an AI developed by OpenAI, designed to assist with a wide range of tasks and questions you might have. How can I help you today?
-----------------

Question >>> how is the weather in Taipei                    
Run status: queued
Run status: in_progress
Run status: requires_action
Google search query: current weather in Taipei
Get result: {'type': 'weather_result', 'temperature': '21', 'unit': 'Celsius', 'precipitation': '0%', 'humidity': '55%', 'wind': '19 公里/時', 'location': '台北市', 'date': '星期六 下午5:00', 'weather': '晴'}
google_search:  {'type': 'weather_result', 'temperature': '21', 'unit': 'Celsius', 'precipitation': '0%', 'humidity': '55%', 'wind': '19 公里/時', 'location': '台北市', 'date': '星期六 下午5:00', 'weather': '晴'}
Run status: queued
Run status: in_progress
Run status: in_progress
Run status: completed
Answer >>>  The current weather in Taipei is clear with a temperature of 21 degrees Celsius. There is no precipitation with a humidity level at 55%, and the wind is blowing at 19 kilometers per hour. It's a nice day! If you need more details or a forecast, let me know.
-----------------

Question >>> quit
Quit chat...
```
## Troubleshooting
### AWS Layer environment variables 
In Lambda page > Configuration > Environment variables
```
LINE_CHANNEL_ACCESS_TOKEN
LINE_CHANNEL_SECRET
OPENAI_API_KEY
SERPAPI_API_KEY
```

### How to create layer?
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