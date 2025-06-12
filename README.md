
# 📝 Task Manager with MongoDB & Redis

A command-line task management application developed with **Python**, **MongoDB Atlas**, and **Redis**, as part of the **Computer Science** and **Software Engineering** course at **ULBRA Palmas**.

The project allows users to manage tasks (create, update, comment, delete) and visualize productivity metrics using Redis, offering a combination of persistent data storage and fast in-memory analytics.

---

## 🧱 Project Structure

```
📁 mongodb_python/
├── main.py        # CLI with interactive task menu
└── func.py        # Functions for MongoDB/Redis logic
```

- `main.py`: Contains the main program loop and user interface.
- `func.py`: Contains all the task manipulation functions and metric tracking.

---

## 🔗 Connections

- **MongoDB Atlas** is used as the main database.
- **Redis** is used to track real-time task metrics such as:
  - Status counters (e.g., pending, completed)
  - Daily task statistics
  - Tag rankings
  - Productivity calculations

The system uses a **fixed user ID** (`13`) for demonstration purposes.

---

## 🚀 Features

- ✅ Create tasks with title, description, tags, and status.
- ✏️ Modify tasks (status, description, tags).
- ❌ Remove tasks by ID.
- 💬 Comment on tasks with automatic timestamps.
- 📊 Redis-powered metrics including:
  - Task status counts
  - Completed tasks per day
  - Top 10 most used tags
  - Average time to complete a task
  - Weekly completion rate

---

## 📊 Redis Metrics Tracked

| Redis Key                             | Description                                |
|--------------------------------------|--------------------------------------------|
| `user:<id>:tasks:status`             | Hash of task count by status               |
| `user:<id>:tasks:created`            | Number of tasks created per day            |
| `user:<id>:tasks:completed`          | Number of tasks completed per day          |
| `user:<id>:tags:top`                 | Sorted set of top-used tags                |
| `user:<id>:stats:productivity`       | Completion time stats for productivity     |

---

## 🧪 Technologies Used

- [Python](https://www.python.org/)
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- [Redis](https://redis.io/)
- [PyMongo](https://pymongo.readthedocs.io/en/stable/)
- [redis-py](https://pypi.org/project/redis/)

---

## ⚙️ Installation & Setup

1. **Install dependencies**

   ```bash
   pip install pymongo redis
   ```

2. **Run Redis Server locally**  
   Make sure Redis is running on `localhost:6379`.  
   On Windows, use **WSL** or Docker for Redis compatibility.

3. **Run the program**

   ```bash
   python main.py
   ```
 ⚠️ **Important:**  
Don't forget to replace the default MongoDB connection string in `main.py` with your own MongoDB Atlas URI:

```python
cliente = MongoClient("your-mongodb-connection-string")
```

Using the provided credentials is only intended for demonstration and testing purposes.

---

## 🧭 Menu Options

```
1. Add new task
2. List all tasks
3. Modify task
4. Remove task
5. Insert comment
6. View metrics (Redis)
7. Exit
```

---

## ⚠️ Notes

- All task data is stored in MongoDB Atlas.
- Redis is used exclusively for metrics.
- Task objects are stored as Python dictionaries and converted to MongoDB documents.
- Redis metrics use `hincrby`, `zincrby`, `hget`, `hgetall`, and `zrevrange` commands.
- Time-based analysis (daily/weekly) is handled with Python’s `datetime`.

---

## 👤 Author & Contact

Developed by **Lucas da Silva Nascimento** – [@lukasnascky](https://github.com/lukasnascky)  
Co-authored by **Arthur Almeida de Souza** – [@ArthurSouzaDev](https://github.com/ArthurSouzaDev)

Feel free to get in touch:

**Lucas da Silva Nascimento**  
- ✉️ Email: [lucas.nascimento@rede.ulbra.br](mailto:lucas.nascimento@rede.ulbra.br)  
- 📷 Instagram: [@lukas_nascky](https://www.instagram.com/lukas_nascky/)  
- 💼 LinkedIn: [Lucas da Silva Nascimento](https://www.linkedin.com/in/lucas-da-silva-nascimento-1720302a3/)

**Arthur Almeida de Souza**  
- 📷 Instagram: [@manzinidev](https://www.instagram.com/manzinidev/)  
- 💼 LinkedIn: [arthursouzs](https://www.linkedin.com/in/arthursouzs/)

---

## 📄 License

This project was developed for educational purposes as part of the **Database** class at **ULBRA Palmas**.
