

#@author Kowshick Srinivasan
#@version: 1.0
#@Assignment: Hw2
import csv
import os
import threading

from LinkedList import LinkedList
from Student import Student


def convert_bool(param):
    if param == "yes":
        return True
    else:
        return False


def convert_to_student(row):
    line = list(row)
    return Student(line[0], line[1], int(line[2]), line[3], line[4], line[5],
                   int(line[6]), int(line[7]), line[8], line[9], line[10], line[11],
                   int(line[12]), int(line[13]), int(line[14]), convert_bool(line[15]), convert_bool(line[16]),
                   convert_bool(line[17]), convert_bool(line[18]), convert_bool(line[19]),
                   convert_bool(line[20]), convert_bool(line[21]), convert_bool(line[22]), int(line[23]), int(line[24]),
                   int(line[25]), int(line[26]),
                   int(line[27]), int(line[28]), int(line[29]), convert_bool(line[30]))


# Memory database class that does:
# a) load the student-data. csv file into the memory database through recursive function.
# b) When a row is added or removed from the CSV file, the memory database will adapt to the changes.
# c) export the memory database into a csv file through recursive function.
class MemoryDatabase:
    BASEPATH = r"D:\Algorithms\IndHw2\Data"
    FILENAME = os.path.join(BASEPATH, 'student-data.csv')
    OUTFILE = os.path.join(BASEPATH, 'student-op-data.csv')

    def read(self, current_node, input_csv):
        """
        Recursive method to read the CSV file and add the contends to the back of the Linked list
        :param current_node: The current Node
        :param input_csv: Reader object
        :return: Completion status of the read operation
        """
        row = next(input_csv, None)
        if row is None:
            return 0
        student = convert_to_student(row)
        return self.read(self.list.insert(current_node, student, None), input_csv)

    # Constructor based dependency injection
    def __init__(self):
        self.list = LinkedList()
        self.running = True
        self.prev_node = None

    def run(self):
        with open(self.FILENAME, newline="") as inputFile:
            input_csv = csv.reader(inputFile)
            header = next(input_csv, None)  # read the Header of the csv
            self.read(self.list.head, input_csv)  # Read the student details from the file and add it to the linked list
        print('enter 0 to stop watching')  # KeyBoard interrupt to signal make watcher thread to stop and join back to the main
        watcher_thread = threading.Thread(target=self.file_watcher)  # Load the watcher method to the watcherThread
        watcher_thread.start()  # Start the watcher thread

        if input() == '0':  # Blocking-instruction, makes the main thread to wait until there is user input 0
            self.running = False  # Signal the watcher thread to stop

        watcher_thread.join()  # Resume after the completion of watcher thread

        with open(self.OUTFILE, mode='w', newline="") as outputFile:
            output_csv_writer = csv.writer(outputFile)
            output_csv_writer.writerow(header)  # print the Header of the csv
            self.printer(self.list.head,
                         output_csv_writer)  # Method to print the traverse the Linked list and print in the csv

    def printer(self, current, output_csv_writer):
        """
        Recursively prints the student data to the csv file
        :param current: Accepts the current NOde/ pointer of the Linked List
        :param output_csv_writer: Accepts the Printer writer object
        :return: completion status of the printing action
        """
        row = current.student.__str__()
        output_csv_writer.writerow(row)
        if current.next is None:
            return 0
        return self.printer(current.next, output_csv_writer)

    # Watches for any changes in the csv file
    def file_watcher(self):
        last_modified = None
        if os.path.exists(self.FILENAME):
            last_modified = os.path.getmtime(self.FILENAME)
        while self.running:  # run the loop until the condition variable is true
            if os.path.exists(self.FILENAME):
                current_modified = os.path.getmtime(self.FILENAME)
                if last_modified is None or current_modified != last_modified:
                    print("changes detected in file")
                    with open(self.FILENAME, mode='r', newline='') as modified_file:
                        modified_csv = csv.reader(modified_file)
                        next(modified_csv, None)  # skip header
                        self.reload(self.list.head, modified_csv)  # Reload only the changes
                        last_modified = current_modified

    def reload(self, current_node, input_csv):
        row = next(input_csv, None)
        # When both the linked list and file is not at the end,
        # i.e. insertion/deletion happens at head in the middle
        if current_node.next is not None and row is not None:
            new_student = convert_to_student(row)
            # There is a change in the current node and the file row, investigate further
            if not new_student.__eq__(current_node.student):  #######problem
                next_node = current_node.next
                # if the current node is the last or if the next node is same as the current row,
                # then the current row has been deleted, so we need to delete current node
                if next_node.next is None or next_node.student.__eq__(new_student):
                    self.list.delete(self.prev_node, next_node)  # deletion operation
                else:
                    self.list.insert(self.prev_node, new_student, next_node)  # Insertion operation

            self.prev_node = current_node  # Store the current node
            return self.reload(current_node.next, input_csv)  # recursively call with the next node and reader object
        # If the linked list has reached its end but not the file,
        # then there is something to be inserted at the end of the Linked list
        elif current_node.next is None and row is not None:
            new_student = convert_to_student(row)
            new_node = self.list.insert(self.prev_node, new_student, None)
            self.prev_node = new_node  # Store the current node
            return self.reload(new_node, input_csv)  # recursively call with the next node and reader object
        # If the File has reached its end and not the Linked List,
        # there is something to be deleted from the end of the LinkedList
        elif current_node.next is not None:
            self.list.delete(self.prev_node, None)
            # No need to recursively call since we need to delete everything that are excess
        return 0  # both File and Linked list has reached the end


if __name__ == '__main__':
    db = MemoryDatabase()
    db.run()
