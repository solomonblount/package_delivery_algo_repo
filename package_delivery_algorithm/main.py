# author: Solomon Blount
# student ID: 011906683

import csv
import datetime

#opening spreadsheet data
with open("./CSV/addresses.csv") as addressesCSV:
    addresses = csv.reader(addressesCSV)
    addresses = list(addresses)

with open("./CSV/distances.csv") as distancesCSV:
    distances = csv.reader(distancesCSV)
    distances = list(distances)


#creating hash table
#source: https://www.youtube.com/watch?v=9HFbhPscPU0 (this video is in course tips for C950)
class ChainedHashTable:
    def __init__(self, starting_size=40):
        self.table = []
        for i in range(starting_size):
            self.table.append([])

    #inserting items into table
    #source: C950 - Webinar-1 - Let's Go Hashing.pdf
    def insert(self, key, item):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        #updating existing items
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        #appending nonexistent items to end of bucket list
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    #removing an item with matching key from the hash table
    #source: C950 - Webinar-1 - Let's Go Hashing.pdf
    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        #removing the item if it is present
        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove(kv)
                return True
        return False

    #lookup function that finds an item using a provided key
    #returning the item if found, or None if not found
    #source: C950 - Webinar-1 - Let's Go Hashing.pdf
    def lookup(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        #searching for key in bucket
        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]  # value
        return None


#class for packages
class Package:
    def __init__(self, id, address, deadline, city, zip, weight, status, notes):
        self.id = id
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zip = zip
        self.weight = weight
        self.status = status
        self.notes = notes
        self.departure_time = None  # Will be set during delivery
        self.delivery_time = None  # Will be set during delivery

    def __str__(self):
        return (f"ID: {self.id}, Address: {self.address}, City: {self.city}, "
                f"ZIP: {self.zip}, Weight: {self.weight}, Status: {self.status}, "
                f"Deadline: {self.deadline}, Departure: {self.departure_time}, "
                f"Delivery: {self.delivery_time}")

    #updating package status based on criteria
    def status_update(self, changed_time):
        if self.delivery_time < changed_time:
            self.status = "Delivered"
        elif self.departure_time > changed_time:
            self.status = "En route"
        else:
            self.status = "At Hub"

        #special handling for package 9
        if self.id == 9:
            if changed_time > datetime.timedelta(hours=10, minutes=20):
                self.address = "410 S. State St"
                self.zip = "84111"
            else:
                self.address = "300 State St"
                self.zip = "84103"


#creating package objects from and loading them into hash table
def load_packages(filename, package_hash):
    with open(filename) as package_info:
        package_data = csv.reader(package_info)

        #skips the header row
        next(package_data, None)

        for package in package_data:
            p_id = int(package[0])
            p_address = package[1]
            p_city = package[2]
            p_zipcode = package[3]
            p_deadline = package[4]
            p_weight = package[5]
            p_status = "At Hub"
            p_notes = package[6] if len(package) > 6 else ""

            #package object
            p = Package(p_id, p_address, p_deadline, p_city, p_zipcode, p_weight, p_status, p_notes)

            #inserting data into hash table
            package_hash.insert(p_id, p)


#class for trucks
class Truck:
    def __init__(self, capacity, speed, miles, packages, address, depart_time):
        self.capacity = capacity
        self.speed = speed
        self.miles = miles
        self.packages = packages
        self.address = address
        self.depart_time = depart_time
        self.time = depart_time
        self.current_location = "4001 South 700 East"  #hub address

    def __str__(self):
        return (f"Capacity: {self.capacity}, Speed: {self.speed}, "
                f"Miles: {self.miles:.2f}, Packages: {len(self.packages)}, "
                f"Address: {self.address}, Departure: {self.depart_time}")


#finding the minimum distance to the next address
def next_address(address):
    for row in addresses:
        if address in row[2]:
            return int(row[0])


#finding distance between two addresses
def distance_between(address1, address2):
    distance = distances[address1][address2]
    if distance == '':
        distance = distances[address2][address1]
    return float(distance)

#creating hash table
package_hash = ChainedHashTable()

#loading packages into table
load_packages("./CSV/packages.csv", package_hash)

#loading trucks and giving them a departure time
truck1 = Truck(16, 18, 0.0, [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40],
               "4001 South 700 East", datetime.timedelta(hours=8))
truck2 = Truck(16, 18, 0.0, [3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39],
               "4001 South 700 East", datetime.timedelta(hours=11))
truck3 = Truck(16, 18, 0.0, [2, 4, 5, 7, 8, 9, 10, 11, 25, 28, 32, 33],
               "4001 South 700 East", datetime.timedelta(hours=9, minutes=5))


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
    current_location = "4001 South 700 East"

    #continue until all packages are routed
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
        truck.packages.append(nearest_package.id)

        #removing from pending list efficiently using index
        pending_deliveries.pop(nearest_package_index)

        #updating truck metrics
        truck.miles += nearest_distance
        current_location = nearest_package.address
        truck.address = current_location

        #calculating travel time (assuming 18 mph average speed)
        travel_time_hours = nearest_distance / 18
        truck.time += datetime.timedelta(hours=travel_time_hours)

        #updating package delivery information
        nearest_package.delivery_time = truck.time
        nearest_package.departure_time = truck.depart_time

        #update package status based on current time
        nearest_package.status_update(truck.time)

    #after completing route, return to hub and add return distance
    return_to_hub_distance = distance_between(
        next_address(current_location),
        next_address("4001 South 700 East")  #this is the hub's address
    )
    truck.miles += return_to_hub_distance
    travel_time_hours = return_to_hub_distance / 18
    truck.time += datetime.timedelta(hours=travel_time_hours)

#executing delivery optimization for all trucks
def deliver_packages():
    #commence delivery operations for all trucks in sequence.

    print("Starting delivery route optimization...")

    #optimizing and dispatching first two trucks
    print("Optimizing routes for Truck 1...")
    optimize_routes(truck1)

    print("Optimizing routes for Truck 2...")
    optimize_routes(truck2)

    #truck 3 waits for first available return from Truck 1 or Truck 2
    print("Scheduling Truck 3 departure...")
    truck3.depart_time = min(truck1.time, truck2.time)

    print("Optimizing routes for Truck 3...")
    optimize_routes(truck3)

    #calculating and displaying summary statistics
    print("\n=== Delivery Operation Summary ===")
    print(f"Truck 1: {len(truck1.packages)} packages, {truck1.miles:.2f} miles, "
          f"completed at {truck1.time}")
    print(f"Truck 2: {len(truck2.packages)} packages, {truck2.miles:.2f} miles, "
          f"completed at {truck2.time}")
    print(f"Truck 3: {len(truck3.packages)} packages, {truck3.miles:.2f} miles, "
          f"completed at {truck3.time}")

    total_miles= truck1.miles + truck2.miles + truck3.miles
    print(f"\nTotal distance traveled: {total_miles:.2f} miles\n")

    #user interface
    class Main:
        print("Welcome to Western Governors University's Parcel Service")
        #asking user to enter the word "start" to start
        text = input("Type the word 'start' to begin, or anything else to quit.")
        #asking user to enter a time to check packages
        if text == "start":
            try:
                time_input = input(
                    "Enter time in the HH:MM:SS format to check package statuses. ")
                (h, m, s) = time_input.split(":")
                convert_timedelta = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                #asking user if they want list status of all or one package
                second_input = input(
                    "Enter 'all' or 'one' to list status of every or an individual package.")
                #asking user for one package ID if they enter 'one'
                if second_input == "one":
                    try:
                        #asking user to provide a package ID (program will quit if invalid input is given)
                        one_input = input("Enter the package's ID")
                        package = package_hash.lookup(int(one_input))
                        package.status_update(convert_timedelta)
                        print(str(package))
                    except ValueError:
                        print("Entry invalid. Closing program.")
                        exit()
                #listing status of every package if user enters 'all'
                elif second_input == "all":
                    try:
                        for packageID in range(1, 41):
                            package = package_hash.lookup(packageID)
                            package.status_update(convert_timedelta)
                            print(str(package))
                    except ValueError:
                        print("Entry invalid. Closing program.")
                        exit()
                else:
                    exit()
            except ValueError:
                print("Entry invalid. Closing program.")
                exit()
        elif input != "time":
            print("Entry invalid. Closing program.")
            exit()

if __name__ == "__main__":
    deliver_packages()