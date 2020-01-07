# Burgers!
Restaurant order management system created in Python

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Layout](#layout)
* [User Manual](#user-manual)

## General info
This project is a simple application for collecting orders from customers. Digging into Tkinter, SQLite with creating a complexed set of features in Python was the main motivation to undertake this task.

## Technologies
Project is built with:
* Python version: 3.7.1
* Tkinter version: 8.6
* SQLite version: 3.21.0

## Layout
![layout](/images/layout.jpg)
<br>Application stores bookings with generating unique ID number for each order.
<br>Orders are sorted by the receipt time, while maintaining a certain limit of ordered meals.

## User Manual
Interface consists of four segments.
<br>
<br>![sections](/images/sections.jpg)

#### 1. Selection
This section gathers fields representing ordered amounts of burgers, which names are loaded from the database.
<br>The application allows setting amount with a mouse click or by typing from keyboard.
<br>
<br>![selection](/images/selection.jpg)

#### 2. Summary
Selected burgers are conveyed as a list to the summary window in order to review before sending it to the database.
<br>
<br>![summary](/images/summary.jpg)

#### 3. Order information
As mentioned before, each order number is generated.
<br>Select preferential, available receipt time and insert customer's phone number for orders made via phone call.
<br>With chosen "OB" (OverBooking) checkbox, user avoids ordering limit with information about selected products over established amount.
<br>
<br>![set time](/images/order_info_1.jpg)
<br>
* Press "Add New" to save order in the database. For stored reservations, the cost of all selected products is printed in the Summary Section.
* Press "Update Order" to make changes in the saved purchase, which you can access with Search Section.
* Press "Clear All" to simply deselect all chosen products and clear inscribed data.
* Press "Delete Order" to remove selected order from the database.

<br>![add order](/images/order_info_2.jpg)

#### 4.Search
To filter stored orders single out receipt time from drop-down list.
<br>Then, select order number to view details of the particular order.
<br>
<br>![view order](/images/search.jpg)
