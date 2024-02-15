"""
.................................Project Description:...........................................................

.....AIM: To develop an organiser that integrate to-do-list, a calendar, and also send alert when the weather is below 5 degrees.....
Main: 
I approached this project using a the python graphic user interface (GUI) based appplication.
As you requested in the proposal that I include a To-do-List and a calander to the weather information,
This project have integrated all those functionalities.
So, this GUI based application as 2 functionalities: 

1. Give information about the weather condition,
2. Allow for organising to-do-list with associated deadlines (Using the calendar) and set priorities, 

Futher discription: 
The weather data is fetched from the 'OpenWeatherMap API'realtime using conditions in Saint-Etienne.
Tasks can be added or deleted, and are displayed in a Treeview format.
This data is then written in a text file called the todolist text file 


Libraries Used:
    1. Tkinter: A GUI library for Python, used for creating the interface elements. 
    2. ttk: A submodule of Tkinter, providing access to design tools.
    3. tkcalendar: A Tkinter-compatible calendar widget library.
    4. requests: A library for making HTTP requests, used to fetch weather data.
    5. winsound: A library for playing sound, used for notifications.
"""

import datetime as dt
import requests
import winsound
from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar

# ................................ Main Application Class ...................................... #

class ProductivityAPP:

    # ......................... Function for initialization of the application.................................#
        # Time Complexity: O(1)
        # Explanation: Initialization of the application involves setting up the GUI elements.
        # This is a constant time operation, as it does not depend on any variable data size.
    def __init__(self, root):
        self.root = root
        self.root.title('Productivity APP')
        self.root.geometry("1200x600")

        self.setup_weather()
        self.setup_todo()
        self.setup_calendar()

    #............................... Function to Setup the Weather Information ...............................#
        # Time Complexity: O(1)
        # Explanation: The function makes an API request and processes a fixed amount of data,
        # regardless of user input or data size. Thus, it has a constant time complexity.
    def setup_weather(self):
        Base_url = "http://api.openweathermap.org/data/2.5/weather?"
        API_KEY = "beebada8e47c8ccac7fb1b9f3019d2c5"  
        CITY = "Saint-Etienne"

        url = Base_url + "appid=" + API_KEY + "&q=" + CITY
        response = requests.get(url).json()

        temp_kelvin = response['main']['temp']
        temp_celsius = self.kelvin_to_celsius(temp_kelvin)
        description = response['weather'][0]['description']

        weather_frame = Frame(self.root)
        weather_frame.pack(side=TOP, fill=X)
        weather_label = Label(weather_frame, text=f"Temperature in {CITY}: {temp_celsius}°C\nGeneral Weather in {CITY}: {description}")
        weather_label.pack()


        if temp_celsius < 5:
            alert_label = Label(weather_frame, text="Alert: The temperature is below 5°C. Please dress warmly.", fg="red")
            alert_label.pack()
            winsound.Beep(800, 1000)  

    #............................ fucntion for converting temperature from kelvin to degrees................#
            # Time Complexity: O(1)
             # This method performs an arithmetic operation and rounding, which are constant time operations.
    @staticmethod
    def kelvin_to_celsius(kelvin):
        return round(kelvin - 273.15)

    # ............................ Function to Setup the ToDoList to the Left ................................#
        # Time Complexity: O(1)
        # Explanation: The setup of the to-do list interface is a constant time operation.
        # It involves creating and packing static GUI elements.
    def setup_todo(self):
        todo_frame = Frame(self.root)
        todo_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

        label = Label(todo_frame, text="To-Do List", font=("ariel", 25, "bold"), bg="orange", fg="black")
        label.pack(side='top', fill=X)

        control_frame = Frame(todo_frame)
        control_frame.pack(fill=X, pady=5)

        task_entry = Text(control_frame, height=2, width=25, bd=5, font=("ariel", 10, "bold"))
        task_entry.pack(side=LEFT, padx=5)

        priority_label = Label(control_frame, text="Priority", font=("ariel", 12), bg="orange", fg="black")
        priority_label.pack(side=LEFT, padx=5)

        priority_var = StringVar(todo_frame)
        priority_var.set("Medium")
        priority_menu = OptionMenu(control_frame, priority_var, "High", "Medium", "Low")
        priority_menu.pack(side=LEFT, padx=5)

        add_button = Button(control_frame, text="Add Task", font=("ariel", 12, "bold"),
                            bg='orange', fg='black', command=lambda: self.add_task(task_entry, priority_var, task_tree))
        add_button.pack(side=LEFT, padx=5)

        delete_button = Button(control_frame, text="Delete Task", font=("ariel", 12, "bold"),
                               bg='orange', fg='black', command=lambda: self.delete_task(task_tree))
        delete_button.pack(side=LEFT, padx=5)

        tree_scroll = Scrollbar(todo_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        task_tree = ttk.Treeview(todo_frame, columns=("Task", "Deadline", "Priority"), show="headings", height=15, yscrollcommand=tree_scroll.set)
        task_tree.column("Task", width=300, anchor=W)
        task_tree.column("Deadline", width=100, anchor=CENTER)
        task_tree.column("Priority", width=100, anchor=CENTER)
        task_tree.heading("Task", text="Task")
        task_tree.heading("Deadline", text="Deadline")
        task_tree.heading("Priority", text="Priority")
        task_tree.pack(pady=5, side=LEFT, fill=BOTH, expand=True)

        tree_scroll.config(command=task_tree.yview)

        #...................................Function to  Setup Calendar on the Right .....................................#
        # Time Complexity: O(1)
            # Explanation: Similar to setup_todo, setting up the calendar involves static GUI elements,
            # and thus is a constant time operation.
    def setup_calendar(self):
        
        calendar_frame = Frame(self.root)
        calendar_frame.pack(side=RIGHT, fill=BOTH, expand=True)
        
        self.cal = Calendar(calendar_frame, selectmode="day", year=2023, month=12, day=22)
        self.cal.pack(pady=20, padx=10)

        self.my_label = Label(calendar_frame, text="")
        self.my_label.pack()


         # .......................................... Function to Add a Task .............................................#
         # Time Complexity: O(n)
            # Explanation: The complexity of getting text from the Text widget and inserting it into the Treeview
            # is generally O(n), where n is the number of characters in the task entry. Writing to a file is also O(n).
    def add_task(self, task_entry, priority_var, task_tree):
       
        content = task_entry.get(1.0, END).strip()
        date = self.cal.get_date()
        if content:
            priority = priority_var.get()
            task_tree.insert('', 'end', values=(content, date, priority))
            with open("todolist.txt", "a") as file:
                file.write(content + '|' + date + '|' + priority + '\n')
            task_entry.delete(1.0, END)

    # ...................................................... Function to Delete a Task ....................................... #
        # Time Complexity: O(n)
            # Explanation: The complexity is O(n) where n is the number of tasks. This is because the method
            # iterates over each line in the file to find and delete the selected task.
    def delete_task(self, task_tree):
        selected_item = task_tree.selection()
        if selected_item:
            task, date, priority = task_tree.item(selected_item, 'values')
            task_tree.delete(selected_item)

            with open("todolist.txt", "r+") as file:
                lines = file.readlines()
                file.seek(0)
                for line in lines:
                    if line.strip() != task + '|' + date + '|' + priority:
                        file.write(line)
                file.truncate()

    


if __name__ == "__main__":
    root = Tk()
    app = ProductivityAPP(root)
    root.mainloop()
