#@author Kowshick Srinivasan
#@version: 1.0
#@Assignment: Hw2
class Node: #class to define the structure of node
    def __init__(self, student):
        self.student = student #Contains object of student
        self.next = None  #Contains an object of itself,the next node is null by default

class LinkedList:
    def __init__(self):
        self.head = None #Contains  object of type Node

    def insert(self, current_node, student, next_node):
        """

        :param current_node: The current last Node/pointer
        :param student: The student object that needs to be inserted
        :param next_node: The following Node which needs to be pointed by the inserted node
        :return: new last node
        """
        new_student = Node(student) #Create the new student node
        new_student.next = next_node
        if current_node is None:
            self.head = new_student #If linked list is empty, make the new student as the first/head node
        else:
            current_node.next = new_student #Connect the previous node next to the new student node, extending the linked list chain
        return new_student

    def delete(self, prev_node, next_node):
        """
        The method is to delete the current node from the linked list.
        :param prev_node: The current last Node/ pointer
        :param next_node: The immediate next node after the current Node
        """
        # We can assign the next node pointer of the previous node to the next node instead of the current node.
        # Since the current node is hanging in the heap space the garbage collector will remove it.
        if prev_node is None:

            self.head = next_node  # Delete at the head
        else:
            prev_node.next = next_node
