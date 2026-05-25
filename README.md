# 🤖 Robot Navigation Puzzle Game

An interactive **pathfinding visualization** project developed in **Python** using **Tkinter**.
This application demonstrates how robots navigate through obstacles using **BFS** and **DFS** algorithms.

Users can place obstacles, define start and destination points, and watch the robot’s movement through animated path traversal.

---

## ✨ Features

| Feature            | Description                               |
| ------------------ | ----------------------------------------- |
| 🎮 10×10 Grid      | Interactive grid-based environment        |
| 🚧 Obstacles       | Add or remove barriers dynamically        |
| 🟢 Start Point     | Left-click to set robot starting position |
| 🔴 End Point       | Double-click to set destination           |
| 🔵 BFS Algorithm   | Shortest path visualization               |
| 🟢 DFS Algorithm   | Depth-first traversal visualization       |
| 🤖 Robot Animation | Smooth robot movement across the grid     |

---

## 🖱️ Controls

| Action              | Mouse Button |
| ------------------- | ------------ |
| Set Start           | Left Click   |
| Set End             | Double Click |
| Add/Remove Obstacle | Right Click  |

---

## 🛠 Technologies Used

* **Language:** Python
* **GUI:** Tkinter (built-in)
* **Algorithms:** BFS, DFS
* **Concepts:** Pathfinding, Graph Traversal

---

## 🧠 Algorithms

| Algorithm | Approach     | Shortest Path? |
| --------- | ------------ | -------------- |
| BFS       | Queue (FIFO) | ✅ Yes          |
| DFS       | Stack (LIFO) | ❌ No           |

---

## 📊 Complexity

| Algorithm | Time     | Space |
| --------- | -------- | ----- |
| BFS       | O(V + E) | O(V)  |
| DFS       | O(V + E) | O(V)  |

> V = cells, E = neighbor connections

---

## 📦 Requirements

* Python 3.x
* Tkinter (comes built-in with Python)

---

## 🚀 Run the Project

```bash
python robot_navigation_puzzle.py
```

---

## 📁 Project Structure

```text
robot-navigation-puzzle/
├── robot_navigation_puzzle.py
└── README.md
```

---

## 👨‍💻 Author

**Amna Pervez**
