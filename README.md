# Burgers!
Restaurant order management system created in Python

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
This project is a simple application for collecting orders from customers.
<br>Digging into Tkinter, SQLite and creating a complexed set of features in Python was the main motivation to undertake the task.

## Technologies
Project is created with:
* Python version: 3.7.1
* Tkinter version: 8.6
* SQLite version: 3.21.0

## Layout
![layout](/images/layout.jpg)
<br>Application stores bookings with generating unique ID number for each order.
<br>Orders are sorted by the receipt time, while maintaining a certain limit of ordered meals.

## User manual
![sections](/images/sections.jpg)
<br>Interface consists of four segments.

#####1. Selection window
Gathers fields representing ordered amounts of burgers, which names are loaded from the database.
<br>The application allows setting amount with a mouse click or by typing from keyboard.

#####2. Summary window
Selected burgers are conveyed as a list to the summary window in order to review before sending it to the database.

#####3. Order information window
Restaurant staff inserts customer's phone number for orders made via phone call.

#####4.Search section


## Setup
To run this project, install it locally using npm:

```
$ cd ../lorem
$ npm install
$ npm start
```
