# local-llm-zmq

## Minicoda

// install minicoda for python enviroments before

conda create --name local-llm--zmq python=3.8
conda activate local-llm--zmq

## Install requirements

pip install -r requirements.txt

## Export exe

pyinstaller --onefile main.py
