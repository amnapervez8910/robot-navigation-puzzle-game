import tkinter as tk
from tkinter import messagebox, ttk
from collections import deque
import time
import random

class RobotNavigationGame:
    """
    Main class for Robot Navigation Puzzle Game.
    Implements BFS and DFS pathfinding algorithms with visualization.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Robot Navigation Puzzle - BFS vs DFS Pathfinding")
        self.root.geometry("900x750")
        self.root.resizable(False, False)
        self.root.configure(bg='#2c3e50')
        
        # Grid settings
        self.grid_size = 10  # 10x10 grid
        self.cell_size = 50
        self.grid = []  # 0=empty, 1=obstacle, 2=visited, 3=path
        self.obstacles = set()
        
        # Robot position
        self.start_pos = None
        self.end_pos = None
        self.robot_id = None
        
        # Pathfinding variables
        self.current_path = []
        self.visited_nodes = []
        
        # Algorithm selection
        self.current_algorithm = "BFS"
        
        # Colors
        self.colors = {
            'empty': '#ecf0f1',
            'obstacle': '#2c3e50',
            'start': '#27ae60',
            'end': '#e74c3c',
            'visited_bfs': '#3498db',
            'visited_dfs': '#2ecc71',
            'path': '#f39c12',
            'robot': '#e67e22',
            'grid_line': '#bdc3c7'
        }
        
        # State flags
        self.is_animating = False
        self.animation_speed = 0.3  # seconds per step
        
        self.setup_ui()
        self.initialize_grid()
        
    def setup_ui(self):
        """Setup the graphical user interface."""
        
        # Title Frame
        title_frame = tk.Frame(self.root, bg='#2c3e50')
        title_frame.pack(fill='x', padx=10, pady=5)
        
        title_label = tk.Label(title_frame, text="🤖 ROBOT NAVIGATION PUZZLE", 
                                font=('Arial', 20, 'bold'), 
                                fg='white', bg='#2c3e50')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="BFS vs DFS Pathfinding Visualization", 
                                   font=('Arial', 10), 
                                   fg='#bdc3c7', bg='#2c3e50')
        subtitle_label.pack()
        
        # Control Frame
        control_frame = tk.Frame(self.root, bg='#34495e', relief='raised', bd=2)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        # Algorithm Selection
        algo_frame = tk.LabelFrame(control_frame, text="Algorithm", 
                                    font=('Arial', 10, 'bold'),
                                    fg='white', bg='#34495e', bd=0)
        algo_frame.pack(side='left', padx=10, pady=5)
        
        self.algo_var = tk.StringVar(value="BFS")
        bfs_radio = tk.Radiobutton(algo_frame, text="BFS (Shortest Path)", 
                                    variable=self.algo_var, value="BFS",
                                    bg='#34495e', fg='white', selectcolor='#34495e',
                                    font=('Arial', 9))
        dfs_radio = tk.Radiobutton(algo_frame, text="DFS (Depth First)", 
                                    variable=self.algo_var, value="DFS",
                                    bg='#34495e', fg='white', selectcolor='#34495e',
                                    font=('Arial', 9))
        bfs_radio.pack(anchor='w')
        dfs_radio.pack(anchor='w')
        
        # Action Buttons
        action_frame = tk.LabelFrame(control_frame, text="Controls", 
                                      font=('Arial', 10, 'bold'),
                                      fg='white', bg='#34495e', bd=0)
        action_frame.pack(side='left', padx=20, pady=5)
        
        self.start_btn = tk.Button(action_frame, text="▶ Start Navigation", 
                                    command=self.start_navigation,
                                    bg='#27ae60', fg='white', font=('Arial', 10, 'bold'),
                                    padx=10, pady=3)
        self.start_btn.pack(side='left', padx=5)
        
        self.reset_btn = tk.Button(action_frame, text="🔄 Reset Grid", 
                                    command=self.reset_grid,
                                    bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'),
                                    padx=10, pady=3)
        self.reset_btn.pack(side='left', padx=5)
        
        self.clear_btn = tk.Button(action_frame, text="🗑 Clear Path", 
                                    command=self.clear_path,
                                    bg='#f39c12', fg='white', font=('Arial', 10, 'bold'),
                                    padx=10, pady=3)
        self.clear_btn.pack(side='left', padx=5)
        
        # Settings Frame
        settings_frame = tk.LabelFrame(control_frame, text="Settings", 
                                        font=('Arial', 10, 'bold'),
                                        fg='white', bg='#34495e', bd=0)
        settings_frame.pack(side='right', padx=10, pady=5)
        
        tk.Label(settings_frame, text="Speed:", bg='#34495e', fg='white').pack(side='left', padx=5)
        self.speed_var = tk.DoubleVar(value=0.3)
        speed_scale = tk.Scale(settings_frame, from_=0.1, to=1.0, resolution=0.1,
                                orient='horizontal', variable=self.speed_var,
                                bg='#34495e', fg='white', length=100,
                                showvalue=False)
        speed_scale.pack(side='left', padx=5)
        
        # Info Frame
        info_frame = tk.Frame(self.root, bg='#2c3e50')
        info_frame.pack(fill='x', padx=10, pady=5)
        
        self.info_label = tk.Label(info_frame, text="📍 Click: Start (Green) | 🚫 Right-click: Obstacle | 🎯 Double-click: End (Red)",
                                    font=('Arial', 10), fg='#bdc3c7', bg='#2c3e50')
        self.info_label.pack()
        
        self.status_label = tk.Label(info_frame, text="Ready | Select start and end points",
                                      font=('Arial', 10, 'bold'), fg='#f39c12', bg='#2c3e50')
        self.status_label.pack()
        
        # Metrics Frame
        metrics_frame = tk.Frame(self.root, bg='#34495e', relief='sunken', bd=1)
        metrics_frame.pack(fill='x', padx=10, pady=5)
        
        self.bfs_time_label = tk.Label(metrics_frame, text="BFS Time: -- ms", 
                                        font=('Arial', 9), fg='#3498db', bg='#34495e')
        self.bfs_time_label.pack(side='left', padx=20, pady=5)
        
        self.dfs_time_label = tk.Label(metrics_frame, text="DFS Time: -- ms", 
                                        font=('Arial', 9), fg='#2ecc71', bg='#34495e')
        self.dfs_time_label.pack(side='left', padx=20, pady=5)
        
        self.nodes_visited_label = tk.Label(metrics_frame, text="Nodes Visited: --", 
                                             font=('Arial', 9), fg='#f39c12', bg='#34495e')
        self.nodes_visited_label.pack(side='left', padx=20, pady=5)
        
        self.path_length_label = tk.Label(metrics_frame, text="Path Length: --", 
                                           font=('Arial', 9), fg='#27ae60', bg='#34495e')
        self.path_length_label.pack(side='left', padx=20, pady=5)
        
        # Grid Frame
        grid_frame = tk.Frame(self.root, bg='#2c3e50')
        grid_frame.pack(padx=10, pady=10)
        
        self.canvas = tk.Canvas(grid_frame, width=self.grid_size * self.cell_size,
                                 height=self.grid_size * self.cell_size,
                                 bg='white', highlightthickness=2,
                                 highlightbackground='#34495e')
        self.canvas.pack()
        
        # Bind mouse events
        self.canvas.bind("<Button-1>", self.left_click)  # Left click for start
        self.canvas.bind("<Button-3>", self.right_click)  # Right click for obstacle
        self.canvas.bind("<Double-Button-1>", self.double_click)  # Double click for end
        
        # Legend Frame
        self.create_legend()
        
    def create_legend(self):
        """Create legend for the grid colors."""
        legend_frame = tk.Frame(self.root, bg='#2c3e50')
        legend_frame.pack(fill='x', padx=10, pady=5)
        
        legend_items = [
            ('⬜ Empty', '#ecf0f1'),
            ('⬛ Obstacle', '#2c3e50'),
            ('🟢 Start', '#27ae60'),
            ('🔴 End', '#e74c3c'),
            ('🔵 BFS Visited', '#3498db'),
            ('🟢 DFS Visited', '#2ecc71'),
            ('🟡 Path', '#f39c12'),
            ('🤖 Robot', '#e67e22')
        ]
        
        for text, color in legend_items:
            label = tk.Label(legend_frame, text=text, font=('Arial', 8),
                              bg=color, fg='white', padx=5, pady=2,
                              relief='ridge', bd=1)
            label.pack(side='left', padx=5)
            
    def initialize_grid(self):
        """Initialize the grid with empty cells."""
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.obstacles = set()
        self.start_pos = None
        self.end_pos = None
        self.current_path = []
        self.draw_grid()
        
    def draw_grid(self):
        """Draw the grid on canvas."""
        self.canvas.delete("all")
        
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                # Determine cell color
                if (row, col) == self.start_pos:
                    color = self.colors['start']
                elif (row, col) == self.end_pos:
                    color = self.colors['end']
                elif (row, col) in self.obstacles:
                    color = self.colors['obstacle']
                elif self.grid[row][col] == 2:  # Visited
                    if hasattr(self, 'current_algo') and self.current_algo == "BFS":
                        color = self.colors['visited_bfs']
                    else:
                        color = self.colors['visited_dfs']
                elif self.grid[row][col] == 3:  # Path
                    color = self.colors['path']
                else:
                    color = self.colors['empty']
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=self.colors['grid_line'])
                
                # Add coordinates text
                self.canvas.create_text(x1 + self.cell_size//2, y1 + self.cell_size//2,
                                         text=f"{row},{col}", font=('Arial', 8), fill='gray')
        
        # Draw robot if at start position
        if self.start_pos and not self.is_animating:
            self.draw_robot(self.start_pos[0], self.start_pos[1])
            
    def draw_robot(self, row, col):
        """Draw robot at given position."""
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        
        # Draw robot circle
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        r = self.cell_size // 3
        self.robot_id = self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, 
                                                  fill=self.colors['robot'], outline='white', width=2)
        # Draw eyes
        eye_r = r // 4
        self.canvas.create_oval(cx - r//2 - 2, cy - r//2, cx - r//2, cy - r//2 + eye_r*2, fill='white')
        self.canvas.create_oval(cx + r//2 - 2, cy - r//2, cx + r//2, cy - r//2 + eye_r*2, fill='white')
        
    def animate_robot(self, path, index=0):
        """Animate robot moving along the path."""
        if index >= len(path):
            self.is_animating = False
            self.status_label.config(text="✅ Navigation complete! Robot reached destination.")
            return
        
        row, col = path[index]
        
        # Update robot position
        if self.robot_id:
            self.canvas.delete(self.robot_id)
        self.draw_robot(row, col)
        
        # Mark as path
        if (row, col) != self.start_pos and (row, col) != self.end_pos:
            self.grid[row][col] = 3
        
        self.draw_grid()
        self.root.update()
        
        self.root.after(int(self.speed_var.get() * 1000), 
                        lambda: self.animate_robot(path, index + 1))
        
    def left_click(self, event):
        """Handle left click - set start position."""
        if self.is_animating:
            return
        
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            if (row, col) in self.obstacles:
                messagebox.showwarning("Invalid", "Cannot place start on obstacle!")
                return
            
            self.start_pos = (row, col)
            self.clear_path()
            self.status_label.config(text=f"Start set at ({row}, {col}) | Set end point with double-click")
            self.draw_grid()
            
    def right_click(self, event):
        """Handle right click - toggle obstacle."""
        if self.is_animating:
            return
        
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            if (row, col) == self.start_pos:
                messagebox.showwarning("Invalid", "Cannot place obstacle on start!")
                return
            if (row, col) == self.end_pos:
                messagebox.showwarning("Invalid", "Cannot place obstacle on end!")
                return
            
            if (row, col) in self.obstacles:
                self.obstacles.remove((row, col))
                self.grid[row][col] = 0
            else:
                self.obstacles.add((row, col))
                self.grid[row][col] = 1
            
            self.clear_path()
            self.draw_grid()
            
    def double_click(self, event):
        """Handle double click - set end position."""
        if self.is_animating:
            return
        
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            if (row, col) in self.obstacles:
                messagebox.showwarning("Invalid", "Cannot place end on obstacle!")
                return
            
            self.end_pos = (row, col)
            self.clear_path()
            self.status_label.config(text=f"End set at ({row}, {col}) | Click 'Start Navigation'")
            self.draw_grid()
            
    def bfs_pathfinding(self):
        """BFS algorithm to find shortest path."""
        if not self.start_pos or not self.end_pos:
            return None, None, None
        
        queue = deque()
        queue.append(self.start_pos)
        visited = {self.start_pos}
        parent = {self.start_pos: None}
        
        while queue:
            current = queue.popleft()
            
            if current == self.end_pos:
                break
            
            # Check all 4 neighbors (up, down, left, right)
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = current[0] + dr, current[1] + dc
                neighbor = (nr, nc)
                
                if (0 <= nr < self.grid_size and 0 <= nc < self.grid_size and
                    neighbor not in visited and neighbor not in self.obstacles):
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)
        
        # Reconstruct path
        path = []
        if self.end_pos in parent:
            current = self.end_pos
            while current is not None:
                path.append(current)
                current = parent[current]
            path.reverse()
        
        return path, visited, parent
    
    def dfs_pathfinding(self):
        """DFS algorithm to find path (not necessarily shortest)."""
        if not self.start_pos or not self.end_pos:
            return None, None, None
        
        stack = [self.start_pos]
        visited = {self.start_pos}
        parent = {self.start_pos: None}
        
        while stack:
            current = stack.pop()
            
            if current == self.end_pos:
                break
            
            # Check all 4 neighbors
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = current[0] + dr, current[1] + dc
                neighbor = (nr, nc)
                
                if (0 <= nr < self.grid_size and 0 <= nc < self.grid_size and
                    neighbor not in visited and neighbor not in self.obstacles):
                    visited.add(neighbor)
                    parent[neighbor] = current
                    stack.append(neighbor)
        
        # Reconstruct path
        path = []
        if self.end_pos in parent:
            current = self.end_pos
            while current is not None:
                path.append(current)
                current = parent[current]
            path.reverse()
        
        return path, visited, parent
    
    def start_navigation(self):
        """Start the navigation with selected algorithm."""
        if self.is_animating:
            messagebox.showinfo("Info", "Navigation already in progress!")
            return
        
        if not self.start_pos:
            messagebox.showwarning("Warning", "Please set a start point (left-click)")
            return
        
        if not self.end_pos:
            messagebox.showwarning("Warning", "Please set an end point (double-click)")
            return
        
        # Reset grid for new navigation
        self.clear_visited()
        
        algorithm = self.algo_var.get()
        self.current_algo = algorithm
        
        self.status_label.config(text=f"🔄 Running {algorithm} algorithm...")
        self.root.update()
        
        # Run algorithm and measure time
        start_time = time.time()
        
        if algorithm == "BFS":
            path, visited, parent = self.bfs_pathfinding()
        else:
            path, visited, parent = self.dfs_pathfinding()
        
        end_time = time.time()
        elapsed_ms = (end_time - start_time) * 1000
        
        # Update metrics
        if algorithm == "BFS":
            self.bfs_time_label.config(text=f"BFS Time: {elapsed_ms:.2f} ms")
        else:
            self.dfs_time_label.config(text=f"DFS Time: {elapsed_ms:.2f} ms")
        
        self.nodes_visited_label.config(text=f"Nodes Visited: {len(visited)}")
        
        if path:
            self.path_length_label.config(text=f"Path Length: {len(path)} steps")
            self.status_label.config(text=f"✅ Path found! {len(path)} steps, {elapsed_ms:.2f}ms")
            
            # Mark visited nodes
            for node in visited:
                if node != self.start_pos and node != self.end_pos:
                    self.grid[node[0]][node[1]] = 2
            
            self.draw_grid()
            self.root.update()
            
            # Animate robot
            self.is_animating = True
            self.animate_robot(path)
        else:
            self.status_label.config(text="❌ No path found! Try removing obstacles.")
            messagebox.showinfo("No Path", "Could not find a path from start to end!")
    
    def clear_path(self):
        """Clear the path and visited nodes."""
        if self.is_animating:
            return
        
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] in [2, 3]:
                    self.grid[i][j] = 0
        
        self.current_path = []
        self.draw_grid()
        self.status_label.config(text="Path cleared | Select start and end points")
        
    def clear_visited(self):
        """Clear only visited nodes (keep obstacles)."""
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] == 2:
                    self.grid[i][j] = 0
    
    def reset_grid(self):
        """Reset the entire grid."""
        self.is_animating = False
        self.initialize_grid()
        self.status_label.config(text="Grid reset | Select start and end points")
        self.bfs_time_label.config(text="BFS Time: -- ms")
        self.dfs_time_label.config(text="DFS Time: -- ms")
        self.nodes_visited_label.config(text="Nodes Visited: --")
        self.path_length_label.config(text="Path Length: --")


def main():
    """Main function to run the application."""
    root = tk.Tk()
    app = RobotNavigationGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
