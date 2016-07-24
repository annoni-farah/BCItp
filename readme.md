# BCI Training Platform #
--------------------------------

## A brain computer interface training platform ##

## Installation (Linux) ##


### General Linux Dependencies ###

```shell

sudo apt-get install sox

```

### Python Modules (Dependencies) ###

```shell
# add daily updated kivy repository
sudo add-apt-repository ppa:kivy-team/kivy-daily
sudo apt-get update
sudo apt-get install python-numpy python-scipy python-kivy python-biosig

```

### Install Kivy Garden (Dependencies) ###

```shell
sudo apt-get install python-pip
sudo pip install kivy-garden
garden install graph
garden install bar

```

### Clone this repository ###

```shell 

git clone https://github.com/rafaelmendes/bci_training_platform
cd bci_training_platform
git submodule update --init

```

### Open the GUI ###

```shell 

cd bci_training_platform
python main.py

```












