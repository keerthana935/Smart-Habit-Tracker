import mysql.connector
import datetime

# ---------------- CONNECT TO MYSQL ----------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Keerthana@09",
    buffered=True
)

cursor = conn.cursor()

# ---------------- DATABASE ----------------
cursor.execute("CREATE DATABASE IF NOT EXISTS habit_tracker")
cursor.execute("USE habit_tracker")

# ---------------- TABLE ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS habits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    habit_name VARCHAR(100),
    streak INT DEFAULT 0,
    last_completed DATE
)
""")

# ---------------- MAIN LOOP ----------------
while True:

    print("\n===== SMART HABIT TRACKER =====")
    print("1. Add Habit")
    print("2. View Habits")
    print("3. Mark Habit as Done")
    print("4. Streak Dashboard")
    print("5. Exit")

    choice = input("\nEnter choice: ")

    # ---------------- ADD HABIT ----------------
    if choice == "1":
        habit = input("Enter habit name: ")

        cursor.execute("SELECT * FROM habits WHERE habit_name = %s", (habit,))
        exists = cursor.fetchone()

        if exists:
            print("⚠ Habit already exists!")
        else:
            cursor.execute(
                "INSERT INTO habits (habit_name) VALUES (%s)",
                (habit,)
            )
            conn.commit()
            print("✔ Habit added successfully!")

    # ---------------- VIEW HABITS ----------------
    elif choice == "2":
        cursor.execute("SELECT * FROM habits")
        rows = cursor.fetchall()

        if len(rows) == 0:
            print("\nNo habits found!")
        else:
            print("\n📋 Your Habits:")
            for row in rows:
                print(row)

    # ---------------- MARK AS DONE ----------------
    elif choice == "3":
        habit_id = input("Enter habit ID: ")
        today = datetime.date.today()

        cursor.execute(
            "SELECT last_completed, streak FROM habits WHERE id = %s",
            (habit_id,)
        )
        result = cursor.fetchone()

        if result is None:
            print("❌ Habit not found!")
        else:
            last_date = result[0]

            if last_date == today:
                print("⚠ Already marked today!")
            else:
                cursor.execute("""
                    UPDATE habits
                    SET streak = streak + 1,
                        last_completed = %s
                    WHERE id = %s
                """, (today, habit_id))

                conn.commit()
                print("🔥 Habit marked as done! Streak updated!")

    # ---------------- DASHBOARD ----------------
    elif choice == "4":
        cursor.execute("SELECT * FROM habits")
        rows = cursor.fetchall()

        if len(rows) == 0:
            print("\nNo habits found!")
        else:
            print("\n📊 STREAK DASHBOARD")
            print("--------------------------------")
            print("ID | HABIT | STREAK | LAST DONE")

            best_streak = 0

            for row in rows:
                print(f"{row[0]}  | {row[1]}  | {row[2]}  | {row[3]}")

                if row[2] > best_streak:
                    best_streak = row[2]

            print("--------------------------------")
            print("Total Habits:", len(rows))
            print("Best Streak:", best_streak)

    # ---------------- EXIT ----------------
    elif choice == "5":
        print("👋 Exiting... Goodbye!")
        break

    else:
        print("❌ Invalid choice! Try again.")