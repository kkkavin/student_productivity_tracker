import sqlite3
import time
from datetime import datetime

# --- DATABASE SETUP ---
def init_db():
    """Initializes the database and creates tables if they don't exist."""
    conn = sqlite3.connect('tracker.db') # Creates a file named tracker.db
    c = conn.cursor()
    
    # Create table for Tasks
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY, 
                  subject TEXT, 
                  task TEXT, 
                  status TEXT, 
                  deadline TEXT)''')
    
    # Create table for Study Sessions
    c.execute('''CREATE TABLE IF NOT EXISTS study_log
                 (id INTEGER PRIMARY KEY, 
                  date TEXT, 
                  minutes INTEGER)''')
    
    conn.commit()
    conn.close()

# Run this once when the app starts
init_db()

# --- TASK FUNCTIONS ---
def add_task():
    subject = input("Enter Subject (e.g., Math): ")
    task_name = input("Enter Task Description: ")
    deadline = input("Enter Deadline (YYYY-MM-DD): ")
    
    conn = sqlite3.connect('tracker.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (subject, task, status, deadline) VALUES (?, ?, ?, ?)", 
              (subject, task_name, "Pending", deadline))
    conn.commit()
    conn.close()
    print(f"\n✅ Task '{task_name}' added successfully!")

def view_tasks():
    conn = sqlite3.connect('tracker.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE status='Pending'")
    tasks = c.fetchall()
    conn.close()
    
    print("\n--- 📝 PENDING TASKS ---")
    if not tasks:
        print("No pending tasks! Great job.")
    else:
        for task in tasks:
            # task[0] is ID, task[1] is Subject, etc.
            print(f"[ID: {task[0]}] {task[1]}: {task[2]} (Due: {task[4]})")
    print("------------------------")

def complete_task():
    view_tasks()
    task_id = input("Enter the ID of the task to mark complete: ")
    
    conn = sqlite3.connect('tracker.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET status='Completed' WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    print("\n🎉 Task marked as complete!")

# --- PRODUCTIVITY FUNCTIONS ---
def start_study_session():
    print("\n⏱️  Focus Timer Started! Press Ctrl+C to stop studying.")
    start_time = time.time()
    
    try:
        while True:
            elapsed = int(time.time() - start_time)
            minutes, seconds = divmod(elapsed, 60)
            # This prints the time on the same line, overwriting the previous second
            print(f"\rTime Elapsed: {minutes:02d}:{seconds:02d}", end="")
            time.sleep(1)
    except KeyboardInterrupt:
        # Runs when you press Ctrl+C
        end_time = time.time()
        total_minutes = int((end_time - start_time) / 60)
        
        # Save to DB
        today = datetime.now().strftime("%Y-%m-%d")
        conn = sqlite3.connect('tracker.db')
        c = conn.cursor()
        c.execute("INSERT INTO study_log (date, minutes) VALUES (?, ?)", (today, total_minutes))
        conn.commit()
        conn.close()
        
        print(f"\n\n🛑 Session ended. You studied for {total_minutes} minutes.")

def view_progress():
    conn = sqlite3.connect('tracker.db')
    c = conn.cursor()
    c.execute("SELECT SUM(minutes) FROM study_log")
    result = c.fetchone()[0]
    conn.close()
    
    total = result if result else 0
    print(f"\n📈 Total Lifetime Study Hours: {total / 60:.1f} hours")

# --- MAIN MENU ---
def main():
    while True:
        print("\n=== 🎓 STUDENT PRODUCTIVITY TRACKER ===")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task Complete")
        print("4. Start Focus Timer")
        print("5. View Study Stats")
        print("6. Exit")
        
        choice = input("Select an option (1-6): ")
        
        if choice == '1':
            add_task()
        elif choice == '2':
            view_tasks()
        elif choice == '3':
            complete_task()
        elif choice == '4':
            start_study_session()
        elif choice == '5':
            view_progress()
        elif choice == '6':
            print("Goodbye! 👋")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()