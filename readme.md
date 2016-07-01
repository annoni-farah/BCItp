# BCI Training Platform #
--------------------------------

## A brain computer interface training platform ##

## Installation (Linux) ##

### Python Modules (Dependencies) ###

```shell

sudo apt-get install python-numpy python-scipy python-kivy python-biosig

```

### General Linux Dependencies ###

```shell

sudo apt-get install sox

```

### Install Kivy Garden (Dependencies) ###

```shell
sudo apt-get install python-pip
sudo pip install kivy-garden

```

### Garden Modules: ###

* Graph

```shell

garden install graph

```

* Bar

```shell

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












