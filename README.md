# Gutefrage API
### An unofficial [gutefrage.net](https://gutefrage.net) API made for Python.
## Features
* get question by name/url/id
* get newest questions 
* like questions 
* TODO: reply questions 
* TODO: post questions 
* TODO: reply replies
## Get started
An short explenation of the basic features. You can find the full documentation [here]("")
### Installation
Gutefrage API can be installed like every other python package: `pip install gutefrage`
### Basic usage
In this example we are going to mark a question from gutefrage.net as liked.
First we have to create a new client with username and password:
```python 
import gutefrage as gf

gfclient = gf.gutefrage("username", "password")
```
To interact with an specific question we need its **id**. To get the id we need the **last part** of its url. e.g.:

The Url: `https://www.gutefrage.net/frage/wie-berechnet-man-die-quadratwurzel-aus-625`

last part of it: `wie-berechnet-man-die-quadratwurzel-aus-625`

