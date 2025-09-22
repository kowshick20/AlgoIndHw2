package org.example;

import java.io.*;
import java.nio.file.*;
import java.util.Objects;
import java.util.Scanner;
/*
  @author: Kowshick Srinivasan
 * @version: 1.0
 * @Assignment: Hw2
 */

/**
 * Memory database class that does:
 * <p>
 * a) load the student-data.csv file into the memory database through recursive function.
 * <p>
 * b) When a row is added or removed from the CSV file, the memory database will adapt to the changes.
 * <p>
 * c) export the memory database into a csv file through recursive function.
 */
public class MemoryDatabase {

    LinkedList list;  //Object of the linked list

    private static final String FILENAME = "student-data.csv";  //input file name

    private static final String OUTFILE = "student-op-data.csv"; //output file name

    LinkedList.Node prevNode;

    Scanner sc;  //Scanner object

    private static boolean running = true;  //Condition variable

    //Constructor based dependency injection
    public MemoryDatabase(LinkedList list, Scanner sc, LinkedList.Node prevNode) {
        this.list = list;
        this.sc = sc;
        this.prevNode = prevNode;
    }

    public static void main(String[] args) {

        Scanner scanner = new Scanner(System.in);
        MemoryDatabase database = new MemoryDatabase(
                new LinkedList()  //Initialize the list object
                , new Scanner(System.in), null); //Initialize the scanner object

        //Since we used try with resources, we won't be needing a finally block
        try (BufferedReader br = new BufferedReader(new FileReader(FILENAME)); //Buffered reader to enable to the Java methods to read from the given file
             PrintWriter printWriter = new PrintWriter(new FileWriter(OUTFILE))) //Buffered writer to enable the Java methods to write on the given file
        {
            String header = br.readLine();  //read the Header of the csv
            database.read(br, database.list.head);   //Read the student details from the file and add it to the linked list
            System.out.println("Press 0 to exit");   //KeyBoard interrupt to signal make watcher thread to stop and join back to the main
            Thread watcherThread = new Thread(() -> {  //Load the watcher method to the watcherThread
                try {
                    database.watcher();
                } catch (Exception e) {
                    throw new RuntimeException(e);
                }
            });
            watcherThread.start();  //Start the watcher thread
            while (true) {
                if (scanner.hasNext() && Objects.equals(scanner.nextLine(), "0")) {  //If there is any keyboard input, and it is 0
                    running = false; //change the contention variable to false
                    //watcherThread.join();   //Resume after the completion of watcher thread
                    System.out.println("Stopping watcher..."); //Stop the watcher service
                    break;
//                    }
                }
            }


            printWriter.println(header);  //print the Header of the csv
            database.print(database.list.head, printWriter);  //Method to print the traverse the Linked list and print in the csv


        } catch (Exception e) { //Global catch block to handle all the exception thrown by the program
            e.printStackTrace(System.out);  //print the exception stack trace in console

        }

    }


    /**
     * Method recursively read each student details from the CSV file and adds it to the end of the linked list
     *
     * @param br      : The BufferedReader object
     * @param current : Current Node/pointer of the linked list
     * @return : Completion status of the read operation
     */
    private int read(BufferedReader br, LinkedList.Node current) throws IOException {
        String l = br.readLine();  //Read each line
        if (l == null) return 0;  //When reached EOF return
        String[] line = l.split(",");  //Split the row using "," as the separator
        Student student = convertLineToStudent(line);  //Convert the String array to the student class
        return read(br, list.insert(current, student, null));   //Recursively call the function with the buffered reader object and updated last Node/Pointer
    }


    /**
     * Accepts the String array and convert it to student object
     *
     * @param line Original String array formed after comma separation of the line
     * @return Student object
     */
    private Student convertLineToStudent(String[] line) {
        return new Student(line[0], line[1].charAt(0), Integer.parseInt(line[2]), line[3].charAt(0), line[4], line[5].charAt(0),
                Integer.parseInt(line[6]), Integer.parseInt(line[7]), line[8], line[9], line[10], line[11],
                Integer.parseInt(line[12]), Integer.parseInt(line[13]), Integer.parseInt(line[14]), line[15].equals("yes"), line[16].equals("yes"), line[17].equals("yes"), line[18].equals("yes"), line[19].equals("yes"),
                line[20].equals("yes"), line[21].equals("yes"), line[22].equals("yes"), Integer.parseInt(line[23]), Integer.parseInt(line[24]), Integer.parseInt(line[25]), Integer.parseInt(line[26]),
                Integer.parseInt(line[27]), Integer.parseInt(line[28]), Integer.parseInt(line[29]), line[30].equals("yes"));

    }


    /**
     * Recursively prints the student data to the csv file
     *
     * @param current     : Accepts the current NOde/pointer of the Linked List
     * @param printWriter : Accepts the Printed writer object
     * @return : return the completion status of the printing action
     */
    private int print(LinkedList.Node current, PrintWriter printWriter) {
        String row = current.student.toString(); //Converts the student object to comma separated string
        printWriter.println(row);  //Prints the string to the csv file
        if (current.next == null)  //When reached end node return completion status
            return 0;
        return print(current.next, printWriter); //recursively call the print method with updated last node pointer
    }

    /**
     * Watches for any changes in the csv file
     */
    private void watcher() throws Exception {
        WatchService watchService = FileSystems.getDefault().newWatchService(); //create a watcher service
        Path path = Paths.get("."); // current directory
        path.register(watchService, StandardWatchEventKinds.ENTRY_MODIFY);  //Notify when there is a modification event

        while (running) {  //run the loop until the condition variable is true
            WatchKey key = watchService.take(); // blocks until an event
            for (WatchEvent<?> event : key.pollEvents()) {
                WatchEvent.Kind<?> kind = event.kind();
                Path changed = (Path) event.context();
                if (changed.endsWith(FILENAME) && kind == StandardWatchEventKinds.ENTRY_MODIFY) {
                    System.out.println("student-data.csv has changed!");  //Notify there is a change detected in the file
                    BufferedReader br = new BufferedReader(new FileReader(FILENAME)); //buffered reader object of the file
                    br.readLine();  //skip the header
                    reload(list.head, br);  //Reload only the changes

                }

            }
            boolean valid = key.reset();
            if (!valid) break;
        }
    }


    private int reload(LinkedList.Node current, BufferedReader br) throws IOException {
        String row = br.readLine();
        if (current.next != null && row != null) {  //When both the linked list and file is not at the end,
            // i.e. insertion/deletion happens at head in the middle
            String[] line = row.split(",");
            Student newStudent = convertLineToStudent(line);
            //Change detected
            if (!newStudent.equals(current.student)) {  //There is a change in the current node and the file row, investigate further
                LinkedList.Node nextNode = current.next;
                if (nextNode.next == null || nextNode.student.equals(newStudent)) {   //if the current node is the last or if the next node is same as the current row,
                    // then the current row has been deleted, so we need to delete current node
                    list.delete(prevNode, nextNode); //deletion operation
                } else
                    list.insert(prevNode, newStudent, nextNode); //Insertion operation
            }
            prevNode = current;  //Store the current node
            return reload(current.next, br);  //recursively call with the next node and reader object
        } else if (current.next == null && row != null) {   //If the linked list has reached its end but not the file,
            // then there is something to be inserted at the end of the Linked list
            String[] line = row.split(",");
            Student newStudent = convertLineToStudent(line);
            LinkedList.Node newNode = list.insert(prevNode, newStudent, null);
            prevNode = newNode; //Store the current node
            return reload(newNode, br);  //recursively call with the next node and reader object
        } else if (current.next != null) {   //If the File has reached its end and not the Linked List,
            // there is something to be deleted from the end of the LinkedList
            list.delete(prevNode, null);  //delete all the Node that are excess than the File
            //No need to recursively call since we need to delete everything that are excess
        }
        return 0;     //both File and Linked list has reached the end
    }
}

