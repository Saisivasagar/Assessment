# Assessment
Course and Program Assessment

This code is from Rivier University COMP-699 Professional Seminar student projects from Spring 2025.



## Executing the Code


```sh
~/Assessment/src/ACAT$ uv run python run_acat.py
```



## Recommended Installation

Use a github codespace


## 

## Local Windows

### Install WSL and Ubuntu24.04

https://learn.microsoft.com/en-us/windows/wsl/install

open PowerShell in admin mode (right click on program)
`wsl --install -d Ubuntu-24.04`

To see all the available Linux distributions

`wsl --list --online`

reboot your machine



### Install Docker Desktop

https://docs.docker.com/desktop/setup/install/windows-install/

reboot 

start Docker desktop and configure it to start on Windows boot (Settings->General)



### Open Ubuntu in WSL

In Windows search, type Ubuntu and select Ubuntu-24.04

create your userid

create a password  <---- DON'T FORGET IT



### Follow the Install Linux Software Instructions

From here, the directions for Linux and Windows running Linux are the same except where noted.



# Install Linux Software (in Ubuntu or WSL Ubuntu)

`sudo apt update && sudo apt install -y \
    software-properties-common \
    curl \
    zip \
    unzip \
    tar \
    ca-certificates \
    git \
    wget \
    build-essential \
    vim \
    jq \
    firefox \  
    wslu \
    && sudo apt clean`



### Install uv and venv

https://docs.astral.sh/uv/#installation

`curl -LsSf https://astral.sh/uv/install.sh | sh`



### Install Microsoft Visual Studio Code

https://code.visualstudio.com/sha/download



### Clone the Repository

`git clone https://github.com/Rivier-Computer-Science/Assessment.git`

cd into Assessment and initialize a venv environment

`uv venv --python 3.12`

Activate the environment

`source .venv/bin/activate`



### Install Python requirements.txt

`uv pip install -r requirements.txt`



### Set up the Default Browser for Windows Display

Note: Linux users should not need to perform this step.

If your Windows browser does not open automatically:

Option 1: All http requests use the Windows browser:
`sudo apt install wslu
echo 'export BROWSER=wsluview' >> ~/.bashrc`

Option 2: Only this project uses the Windows browser:

`sudo apt install wslu`

echo 'export BOKEH_BROWSER=wsluview' >> ~/.bashrc`

Option 3: Run the browser from within Ubuntu: :
`echo 'export BOKEH_BROWSER=firefox' >> ~/.bashrc`



## Set Environment Variables

Sign up to get an [OpenAI Key](https://platform.openai.com/docs/overview)

```sh
export OPENAI_API_KEY=sk-     # available form platform.openai.com
```

Note: for Windows use *set* instead of *export*

