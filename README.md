# OpenAI-Realtime-API-Chat / API Client for Python

## Run local: Virtual environment using uv
- Install: curl -LsSf https://astral.sh/uv/install.sh | sh
- Create a virtual environment in current dir in folder .venv.
	- `uv venv`
- Activate environment
	- `source .venv/bin/activate`
- Deactivate environment
	- `deactivate`

## Run in Gitpod
https://gitpod.io/#https://github.com/aknip/OpenAI-Realtime-API-Chat
Set API keys here: https://gitpod.io/user/variables
General help and infos: https://www.gitpod.io/guides/gitpodify

## Install dependencies
uv pip install -r requirements.txt

# Set key for OpenAI
export OPENAI_API_KEY=

## Run
python ./examples/streaming_cli.py
or
python ./examples/manual_cli.py


## Source
https://github.com/run-llama/openai_realtime_client



# OpenAI Realtime API Client for Python

This is an experimental OpenAI Realtime API client for Python and LlamaIndex. It integrates with LlamaIndex's tools, allowing you to quickly build custom voice assistants.

Include two examples that run directly in the terminal -- using both manual and Server VAD mode (i.e. allowing you to interrupt the chatbot).

## Installation

Install system deps:

```bash
brew install ffmpeg
```

Install python deps:

```bash
pip install openai-realtime-client

# Optional: clone the repo and run the examples locally
git clone https://github.com/run-llama/openai_realtime_client.git
cd openai_realtime_client
```

Set your openai key:

```bash
export OPENAI_API_KEY="sk-..."
```

## Usage

Assuming you installed and cloned the repo (or copy-pasted the examples), you can immediately run the examples.

Run the interactive CLI with manual VAD (try asking for your phone number to see function calling in action):

```bash
python ./examples/manual_cli.py
```

Or to use streaming mode (which allows you to interrupt the chatbot):

```bash
python ./examples/streaming_cli.py
```

**NOTE:** Streaming mode can be a little janky, best to use headphones in a quiet environment.

Take a look at the examples, add your own tools, and build something amazing!
