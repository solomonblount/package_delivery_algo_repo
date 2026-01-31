# author: Solomon Blount
# student ID: 011906683

import csv
import datetime

#opening spreadsheet data
with open("./CSV\addresses.csv") as addressesCSV:
    addresses = csv.DictReader(addressesCSV)
    addresses = list(addresses)
with open("./CSV\distances.csv") as distancesCSV:
    distances = csv.DictReader(distancesCSV)
    distances = list(distances)

#creating hash table
#source: https://www.youtube.com/watch?v=9HFbhPscPU0 (this video is in course tips for C950)
class chainedHashTable:
    def __init__(self, starting_size = 40):
        self.hashTable = []
        for i in range(starting_size):
            self.hashTable.append([])

#inserts items into table
#source: C950 - Webinar-1 - Let's Go Hashing.pdf
def insert(self, key, item):
    bucket = hash(key) % len(self.table)
    bucket_list = self.table[bucket]

#updates existing items
#source: C950 - Webinar-1 - Let's Go Hashing.pdf
    for kv in bucket_list:
            #print (key_value)
            if kv[0] == key:
                kv[1] = item
                return True

#apppend nonexistent items to end of bucket list
#source: C950 - Webinar-1 - Let's Go Hashing.pdf
    key_value = [key, item]
    bucket_list.append(key_value)
    return True

#removes an item with matching key from the hash table
#source: C950 - Webinar-1 - Let's Go Hashing.pdf

def remove(self, key):
    bucket = hash(key) % len(self.table)
    bucket_list = self.table[bucket]
    #removes the item if it is present
    if key in bucket_list:
        bucket_list.remove(key)

#lookup functions that finds an item using a provided key
#will return the item if found, or None if not found
#source: C950 - Webinar-1 - Let's Go Hashing.pdf
def lookup(self, key):
    bucket = hash(key) % len(self.table)
    bucket_list = self.table[bucket]
    # print(bucket_list)
    # search key in bucket
    for kv in bucket_list:
        # print(key_value)
        if kv[0] == key:
            return kv[1]  # value
    return None

#class for packages
class Packages:
    def __init__(self, ID, address, deadline, city, zip, weight, status, notes, departure_time, delivery_time):
        self.ID = ID
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zip = zip
        self.weight = weight
        self.status = status #remember to make an additional status (delayed)
        self.notes = notes
        self.departure_time = None
        self.delivery_time = None

    def __str__(self):
        return "ID: %s, %-20s, %s, %s,%s, Deadline: %s,%s,%s,Departure Time: %s,Delivery Time: %s" % (self.ID,
                                                                                                      self.address,
                                                                                                      self.deadline,
                                                                                                      self.city,
                                                                                                      self.zip,
                                                                                                      self.weight,
                                                                                                      self.status,
                                                                                                      self.departure_time,
                                                                                                      self.delivery_time)

    def update_status(self, changed_time):
        # Using a fixed delay threshold (e.g., 30 minutes past expected departure)
        expected_departure = self.departureTime - datetime.timedelta(minutes=30)

        if changed_time > expected_departure and self.departureTime > changed_time:
            self.status = "Delayed"
        elif self.deliveryTime < changed_time:
            self.status = "Delivered"
        elif self.departureTime > changed_time:
            self.status = "En route"
        else:
            self.status = "At Hub"

        if self.ID == 9:  # will change the address for package 9 to the correct address once it's been received
            if changed_time > datetime.timedelta(hours=10, minutes=20): #after 10:20, change the address
                self.address = "410 S. State St"
                self.zip = "84111"
            else:
                self.address = "300 State St"
                self.zip = "84103"

#creating package objects from and loading them into hash table
def load_packages(filename, package_hash):
    with open(filename) as package_info:
        package_data = csv.reader(package_info)
        for package in package_data:
            pID = int(package[0])
            pAddress = package[1]
            pDeadline = package[2]
            pCity = package[3]
            pZipcode = package[4]
            pWeight = package[5]
            pStatus = "At Hub"
            pDepartureTime = None
            pDeliveryTime = None

            #package object
            p = Packages(pID, pAddress, pDeadline, pCity, pZipcode, pWeight, pStatus, pDepartureTime, pDeliveryTime)

            #insert data into hash table
            package_hash.insert(pID, p)

#class for trucks
class Trucks:
    def __init__(self, capacity, speed, miles, load, packages, address, depart_time):
        self.capacity = capacity
        self.speed = speed
        self.miles = miles
        self.load = load
        self.packages = packages
        self.address = address
        self.depart_time = depart_time
        self.time = depart_time

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % (self.capacity, self.speed, self.load, self.packages, self.miles,
                                               self.address, self.depart_time)

#finding the minimum distance to the next address
def next_address(self, address):
    for row in addressesCSV:
        if address in row[2]:
            return int(row[0])

#finding distance between two addresses
def distance_between(self, address1, address2):
    distance = distancesCSV[address1][address2]
    if distance == '':
        distance = distancesCSV[address2][address1]
    return float(distance)

#creating hash table
package_hash = chainedHashTable()

#loading packages into table
load_packages("./CSV/packages.csv", package_hash)

#loading trucks and giving them a departure time
truck1 = Trucks(16, 18, 0.0, [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40], None, "4001 South 700 East", datetime.timedelta(hours=8))
truck2 = Trucks(16, 18, 0.0, [3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39], None, "4001 South 700 East", datetime.timedelta(hours=11))
truck3 = Trucks(16, 18, 0.0, [2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33], None, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5))


#delivering packages using Nearest Neighbor Algorithm
#calculating distance traveled and sorting packages for efficient delivery
def optimize_routes(truck):
    #creating list of packages to be delivered
    pending_deliveries = []
    #adding packages to delivery list
    for package_id in truck.packages:
        package = package_hash.lookup(package_id)
        pending_deliveries.append(package)

    #clearing truck's package list to rebuild in optimized order
    truck.packages.clear()
    #tracking current position - start from hub
    current_location = "HUB"

    # Continue until all packages are routed
    while len(pending_deliveries)>0:
        nearest_distance = float('inf')  # Use infinity for initial comparison
        nearest_package = None
        nearest_package_index = -1

        #finding the closest package from current location
        for index, package in enumerate(pending_deliveries):
            distance = distance_between(
                next_address(current_location),
                next_address(package.address)
            )

            if distance < nearest_distance:
                nearest_distance = distance
                nearest_package = package
                nearest_package_index = index

        #updating truck with this delivery
        truck.packages.append(nearest_package.ID)

        #removing from pending list efficiently using index
        pending_deliveries.pop(nearest_package_index)

        #updating truck metrics
        truck.mileage += nearest_distance
        current_location = nearest_package.address
        truck.address = current_location

        #calculating travel time (assuming 18 mph average speed)
        travel_time_hours = nearest_distance / 18
        truck.time += datetime.timedelta(hours=travel_time_hours)

        #updating package delivery information
        nearest_package.delivery_time = truck.time
        nearest_package.departure_time = truck.depart_time

        #update package status based on current time
        nearest_package.update_status(truck.time)

    #after completing route, return to hub and add return distance
    return_to_hub_distance = distance_between(
        next_address(current_location),
        next_address("HUB")  # because HUB is the starting location
    )
    truck.miles += return_to_hub_distance
    travel_time_hours = return_to_hub_distance / 18
    truck.time += datetime.timedelta(hours=travel_time_hours)

# Execute delivery optimization for all trucks
def deliver_packages():
    #Commence delivery operations for all trucks in sequence.

    print("Starting delivery route optimization...")

    # Optimize and dispatch first two trucks
    print("Optimizing routes for Truck 1...")
    optimize_routes(truck1)

    print("Optimizing routes for Truck 2...")
    optimize_routes(truck2)

    # Truck 3 waits for first available return from Truck 1 or Truck 2
    print("Scheduling Truck 3 departure...")
    truck3.depart_time = min(truck1.time, truck2.time)

    print("Optimizing routes for Truck 3...")
    optimize_routes(truck3)

    # Calculate and display summary statistics
    print("\n=== Delivery Operation Summary ===")
    print(f"Truck 1: {len(truck1.packages)} packages, {truck1.miles:.2f} miles, "
          f"completed at {truck1.time}")
    print(f"Truck 2: {len(truck2.packages)} packages, {truck2.miles:.2f} miles, "
          f"completed at {truck2.time}")
    print(f"Truck 3: {len(truck3.packages)} packages, {truck3.miles:.2f} miles, "
          f"completed at {truck3.time}")

    total_miles= truck1.miles + truck2.miles + truck3.miles
    print(f"\nTotal distance traveled: {total_miles:.2f} miles")


