# BCI Training Platform #
--------------------------------

[![Build Status](https://travis-ci.org/rafaelmendes/BCItp.svg?branch=master)](https://travis-ci.org/rafaelmendes/BCItp)

## A brain computer interface training platform ##

* for more detailed information see http://bcitp.readthedocs.io/ 

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
sudo apt-get install python-numpy python-scipy python-kivy python-pip
sudo pip install -U sklearn

```

### Install Kivy Garden (Dependencies) ###

```shell
sudo pip install kivy-garden
garden install graph
garden install bar

```

### Clone this repository ###

```shell 

git clone https://github.com/rafaelmendes/bcitp

```

### Open the GUI ###

```shell 

python bcitp

```












