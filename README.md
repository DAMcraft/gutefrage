![Logo](https://raw.githubusercontent.com/DAMcraft/gutefrage/main/gf-api-logo-new.png)

[![PyPI](https://img.shields.io/pypi/v/gutefrage?color=g&logo=python&logoColor=white)](https://pypi.org/project/gutefrage/)
[![PyPI - License](https://img.shields.io/pypi/l/gutefrage)]()
[![YouTube](https://img.shields.io/badge/DAMcraft-subscribe-red?logo=youtube&logoColor=white)](https://www.youtube.com/c/DAMcraft)
### An unofficial [gutefrage.net](https://gutefrage.net) API made for Python.
## Features
* get question by name/url/id
* get newest questions 
* like questions 
* reply to questions 
* post questions 
* TODO: reply replies
## Get started
An short explenation of the basic features. You can find the full documentation [here](https://github.com/DAMcraft/gutefrage/wiki#documentation)
### Installation
Gutefrage API can be installed like every other python package: `pip install gutefrage`
### Basic usage
In this example we are going to mark a question from gutefrage.net as liked.
First we have to create a new client with username and password:
```python 
import gutefrage as gf

gfclient = gf.gutefrage("username", "password")
```
To interact with an specific question we need its **id**. To get the id we need its **stripped_title**. The stripped_title can be found in the last part of its url called like this:

The Url: `https://www.gutefrage.net/frage/wie-berechnet-man-die-quadratwurzel-aus-625`

stripped_title: `wie-berechnet-man-die-quadratwurzel-aus-625`

To get the questions id we can use `.convert_to_id(string)`:
```python 
title = "wie-berechnet-man-die-quadratwurzel-aus-625"

id = gfclient.convert_to_id(title)
print(id)
```
What now is printed in the console is the question's id! For this question it's `57753709`.
Now we have the id we can get the question by id:
```python 
id = 57753709 
question = gf.question(id)
```
Now we've got the question, we can get lot of information about it:
```python 
information = question.info()
```
And we can finally give it a like!
```python 
question.like
```
## Documentation
You can find the full documentation [here](https://github.com/DAMcraft/gutefrage/wiki#documentation)
