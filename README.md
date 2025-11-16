# Pathfinder Algorithm Visualization

**Pathfinder Visualization** is a Python based interactive program that visualizes popular pathfinding algorithms on a grid, and so assisting people in learning how different algorithms seek the target.

---
## Prerequisites
- Python 3.7 or higher
- pip (Python package installer)
---

## Installation
__1. Clone the repository__
```bash
git clone https://github.com/for-fahad-ahmed/Pathfinder-Visualization
cd pathfinder-visualization
```
__2. Install required dependencies__
```bash
pip install pygame
```

__3. Run the program__
```bash
python main.py
```

# 1. Project Overview
This project is an interactive pathfinding visualizer made in Python using Pygame. It lets you see how different pathfinding algorithms find a path from a start point to an end point in a grid with obstacles.

You can place start, end, and barrier nodes on a grid and watch the algorithms work in real time. This project is useful for learning how pathfinding works and for comparing different algorithms visually.

## 1.1 Objectives
- Implement multiple pathfinding algorithms with visual feedback  
- Compare algorithms based on number of nodes visited and path length  
- Provide a fun, interactive tool for learning algorithms  
- Show how different data structures are used in practice  

## 1.2 Features
- **Interactive Grid System:** 60×31 node grid  
- **Three Pathfinding Algorithms:** A*, BFS, and DFS implementations  
- **Real-Time Visualization:** Color-coded node states during execution  
- **Performance Metrics:** Live statistics showing nodes visited and path length  

## 1.3 Node Colors
- **Green** – Start node  
- **Red** – End node  
- **Black** – Barrier node  
- **Blue** – Node currently being considered (open)  
- **Purple** – Node already visited (closed)  
- **Gold** – Node part of the final path  

---

# 2. Technical Stack
- **Language:** Python 3.7+  
- **Graphics:** Pygame 2.0+  
- **GUI (instructions popup):** Tkinter  
- **Grid:** 60×31 nodes, 30px each  

---

# 3. Program Flow
![Program Flow](Screenshot_20251116_155729.png)
1. You place the start and end nodes on the grid.  
2. You can add barriers by left-clicking empty spaces.  
3. Right-click removes a node.  
4. Press **A** to run A*, **B** to run BFS, **D** to run DFS, and **C** to reset the grid.  
5. The algorithm runs and colors the nodes as it explores.  
6. When finished, the final path is shown in gold, and stats are displayed at the top.  

---

# 4. Data Structures Used

## 4.1 Grid – 2D Array
**Why used:** Nodes naturally fit into rows and columns.  
**Benefits:** Fast access, easy neighbor lookup, memory efficient.  
**Usage:** Stores all 1,860 nodes.

## 4.2 Priority Queue (A* Algorithm)
**Why used:** Pick node with lowest f-score first.  
**Benefits:** Efficient min-heap selection.  
**Usage:** Stores nodes based on `f = g + h`.

## 4.3 Queue (BFS Algorithm)
**Why used:** FIFO order needed for level-by-level exploration.  
**Benefits:** Guarantees shortest path.  
**Usage:** Stores discovered but unvisited nodes.

## 4.4 Stack (DFS Algorithm)
**Why used:** Explore deeply before backtracking.  
**Benefits:** Simple, memory-friendly for deep paths.  
**Usage:** Holds current path state.

## 4.5 Hash Set (Visited Tracking)
**Why used:** Fast membership checks.  
**Benefits:** O(1) lookup, prevents cycles.  
**Usage:** Used in A* and DFS.

## 4.6 Dictionary (Hash Map)
**Why used:** Store parent relationships and cost values.  
**Benefits:** Constant-time access.  
**Usage:**  
- `came_from` – reconstructs path  
- `g_score` – distance from start  
- `f_score` – total estimated cost  

## 4.7 2D Boolean Array (Visited Matrix for BFS)
**Why used:** Track visited nodes in BFS.  
**Benefits:** Fast, memory efficient, grid-aligned.  

---

# 5. Algorithm Analysis

## 5.1 A* Algorithm  
**Time Complexity:** `O(b^d log(b^d))`  
- **b:** branching factor (≤4)  
- **d:** depth of solution  

**Advantages:**  
- Always finds the shortest path  
- Uses heuristic for efficiency  
- Complete and optimal  

**Heuristic Function (Manhattan Distance):**
```python
def h_score(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)
```

## 5.2 Breadth-First Search (BFS) 
**Time Complexity:** `O(V+E)`
- V = number of vertices (nodes)
- E = number of edges (connections)


**Advantages:**  
- Finds the shortest path in unweighted grid, and here the grid is unweighted 
- Simple implementation 
- Complete: Always finds solution

## 5.3 Depth-First Search (DFS)
**Time Complexity:** `O(V+E)`  

**Advantages:**  
- Memory efficient for deep graphs 
- Fast for dense mazes 
- Simple implementation

# 6. Performance Comparison

## 6.1 Metrics Collected
- **Nodes Visited:** Total nodes explored during search
- **Path Length:** Number of steps in final path

## 6.2 Expected Performance

| **Algorithm** | **Nodes Visited** | **Optimal Solution** | **Best Use Case**         |
|---------------|-------------------|----------------------|---------------------------|
| A*            | Lowest            | Yes                  | Navigation Systems, games |
| BFS           | Medium-High       | Yes                  | Shortest Path Required    |
| DFS           |                   | No                   | Maze solving, exploration |


# Conclusion
This pathfinding visualization project successfully demonstrates the practical application of fundamental data structures in algorithm implementation. By comparing A*, BFS, and DFS side, users can understand the differences between optimality, efficiency, and implementation.
 
