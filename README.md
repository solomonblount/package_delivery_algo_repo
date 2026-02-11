# WESTERN GOVERNORS UNIVERSITY 
## C950 – JAVA FRAMEWORKS

ASSUMPTIONS

•  Each truck can carry a maximum of 16 packages, and the ID number of each package is unique.
•  The trucks travel at an average speed of 18 miles per hour and have an infinite amount of gas with no need to stop.
•  There are no collisions.
•  Three trucks and two drivers are available for deliveries. Each driver stays with the same truck as long as that truck is in service.
•  Drivers leave the hub no earlier than 8:00 a.m., with the truck loaded, and can return to the hub for packages if needed.
•  The delivery and loading times are instantaneous (i.e., no time passes while at a delivery or when moving packages to a truck at the hub). This time is factored into the calculation of the average speed of the trucks.
•  There is up to one special note associated with a package.
•  The delivery address for package #9, Third District Juvenile Court, is wrong and will be corrected at 10:20 a.m. WGUPS is aware that the address is incorrect and will be updated at 10:20 a.m. However, WGUPS does not know the correct address (410 S. State St., Salt Lake City, UT 84111) until 10:20 a.m.
•  The distances provided in the “WGUPS Distance Table” are equal regardless of the direction traveled.
•  The day ends when all 40 packages have been delivered.

A.  Develop a hash table, without using any additional libraries or classes, that has an insertion function that takes the package ID as input and inserts each of the following data components into the hash table:

•   delivery address
•   delivery deadline
•   delivery city
•   delivery zip code
•   package weight
•   delivery status (i.e., at the hub, en route, or delivered), including the delivery time

1. main.py, lines 9-14: added code that opens provided spreadsheets as csv files
2. main.py, lines 15-21: added function that creates an empty hash table with 40 buckets
3. main.py, lines 23-52: added functions that inserts, updates, and removes spreadsheet data in or from the hash table

B.  Develop a look-up function that takes the package ID as input and returns each of the following corresponding data components:

•   delivery address
•   delivery deadline
•   delivery city
•   delivery zip code
•   package weight
•   delivery status (i.e., at the hub, en route, or delivered), including the delivery time

4. main.py, lines 53-65: added function that takes a provided package ID and finds corresponding data 

C.  Write an original program that will deliver all packages and meet all requirements using the attached supporting documents “Salt Lake City Downtown Map,” “WGUPS Distance Table,” and “WGUPS Package File.”

•  Create an identifying comment within the first line of a file named “main.py” that includes your student ID.
•  Include comments in your code to explain both the process and the flow of the program.

5. main.py, lines 67-111: added a package class to store package data and a nested function to update a package's status
6. main.py, lines 113-132: added function for inserting package data into the hash table 
7. main.py, lines 134-148: added a truck class to store truck data for when they are created later
8. main.py, lines 150-161: added functions for calculating the minimum distance needed to travel to the next address and the distance between two addresses
9. main.py, lines 163-172: added code to create the hash table, load packages into them, and load packages into trucks
10. main.py, lines 175-270: added function that uses the nearest neighbor algorithm to deliver the packages


D.  Provide an intuitive interface for the user to view the delivery status (including the delivery time) of any package at any time and the total mileage traveled by all trucks. (The delivery status should report the package as at the hub, en route, or delivered. Delivery status must include the time.)

•  Provide screenshots to show the status of all packages loaded onto each truck at a time between 8:35 a.m. and 9:25 a.m.
•  Provide screenshots to show the status of all packages loaded onto each truck at a time between 9:35 a.m. and 10:25 a.m.
•  Provide screenshots to show the status of all packages loaded onto each truck at a time between 12:03 p.m. and 1:12 p.m.

11. main.py: modified previously written code to be more readable and more consistent (capitalization, formatting, & variable names)
12. main.py: lines 276-322: added a main interface to allow user input and communicate inportant information with the user, such as package status
