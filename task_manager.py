import json
import os
#Displays task manager menu
def main_menu():
    print_task=""" Task Manager
                1. Add task 
                2. View tasks
                3. Delete task
                4. Mark task is Complete
                5. Exit
     """
    print( print_task)    
def main():

    #this main function to run the CLI application
    
    manager = TaskManager()
    while True:
        main_menu()
        choice = input("enter your choice 1 to 5 : ").strip()
        if choice == '1':
      
            title = input("enter your task title: ").strip()
            if title:
                manager.add_task(title)
            else:
                print("your task title cannot be empty.")
      
        elif choice == '2':
            manager.view_tasks()
      
        elif choice == '3':
            try:
                task_id = int(input("enter your delete task ID: ").strip())
                manager.delete_task(task_id)
            except ValueError:
                print("invalid input. please enter a number task ID.")
      
        elif choice == '4':
            try:
                task_id = int(input("complete your task:").strip())
                manager.mark_task_complete(task_id)
            except ValueError:
                print("invalid input. please enter a number task ID.")
      
        elif choice == '5':
            print("your task exit")
            break
        else:
            print("invalid choice. please select  1 to 5")

#this class manage the tasks

class TaskManager:
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = []
        self.next_id = 1
        self.load_tasks()

    #Add a new task
    
    def add_task(self, title):
        task = Task(id=self.next_id, title=title)
        self.tasks.append(task)
        self.next_id += 1
        self.save_tasks()
        print(f"Task added with ID {task.id}.")
    
    #Display the all tasks

    def view_tasks(self):
        if not self.tasks:
            print("No tasks available.")
            return
        print("\nYour Tasks Below")
        print("{:<20} {:<20} {:<50}".format("ID", "Status","Title"))
        print("=" *60)
      
        for task in self.tasks:
            status = "Completed" if task.completed else "Pending"
            print("{:<20} {:<20} {:<50}".format(task.id, status,task.title))
        print()
    
    #Delete a task by  ID
    
    def delete_task(self, task_id):
      
        for task in self.tasks:
            if task.id == task_id:
                self.tasks.remove(task)
                self.save_tasks()
                print(f"Task with ID {task_id} is deleted.")
                return
        print(f"No task found with ID {task_id}.")
    
    #task completed by ID

    def mark_task_complete(self, task_id):
      
        for task in self.tasks:
      
            if task.id == task_id:
      
                if not task.completed:
                    task.completed = True
                    self.save_tasks()
                    print(f"Task with ID {task_id} mark  completed.")
                else:
                    print(f"Task with ID {task_id} is already completed.")
      
                return
        print(f"task Not found This ID {task_id}.")
    
    #Save the tasks in JSON file

    def save_tasks(self):
      
        with open(self.filename, 'w') as f:
            tasks_data = [task.to_dict() for task in self.tasks]
            json.dump({'tasks': tasks_data, 'next_id': self.next_id}, f, indent=4)
    
    #Load tasks from the JSON file
    
    def load_tasks(self):
      
        if not os.path.exists(self.filename):
            return
      
        with open(self.filename, 'r') as f:
            data = json.load(f)
            tasks_data = data.get('tasks', [])
            self.next_id = data.get('next_id', 1)
            self.tasks = [Task.from_dict(task_dict) for task_dict in tasks_data]  
            
#this class represent a Task          

class Task:
    def __init__(self, id, title, completed=False):
        self.id = id
        self.title = title
        self.completed = completed

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'completed': self.completed
        }

    @staticmethod
    def from_dict(task_dict):
        return Task(
            id=task_dict['id'],
            title=task_dict['title'],
            completed=task_dict['completed']
        )

main()