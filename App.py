import tkinter as tk
from tkinter import messagebox
from time import perf_counter
from turtle import RawTurtle, ScrolledCanvas, TurtleScreen
from map_utils import Map
from pathfinding import A_Star
class App:
    def __init__(self, root):
        self.root = root
        root.title("A* Pathfinding Demo")
        
        # Left: Canvas chứa turtle
        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.cv = ScrolledCanvas(self.canvas_frame, width=600, height=800)
        self.cv.pack(fill=tk.BOTH, expand=True)
        self.screen = TurtleScreen(self.cv)      # <-- từ turtle, không phải tk
        self.screen.mode("world")
        self.screen.setworldcoordinates(-410, -710, 410, 710)
        self.t = RawTurtle(self.screen, shape='turtle')

        
        # Right: Controls & Legend
        ctrl = tk.Frame(root, padx=10, pady=10)
        ctrl.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Start button
        self.btn_start = tk.Button(ctrl, text="Bắt đầu giải mã", command=self.start)
        self.btn_start.pack(fill=tk.X, pady=5)
        
        # Legend
        tk.Label(ctrl, text="Chú thích:", font=('Arial', 12, 'bold')).pack(anchor='w', pady=(20,5))
        self._add_legend(ctrl, "Đích đến", 'orange')
        self._add_legend(ctrl, "Vật cản / Tường", 'black')
        self._add_legend(ctrl, "Đường đi", 'blue')
        
        # Info & finish/reset buttons (ẩn ban đầu)
        self.info_label = tk.Label(ctrl, text="", wraplength=200, justify='left')
        self.btn_finish = tk.Button(ctrl, text="Hoàn tất", command=root.quit)
        self.btn_reset  = tk.Button(ctrl, text="Quay lại", command=self.reset)
        
        # Prepare map & turtle
        self.width_half, self.height_half = 400, 700
        self._prepare_map()
    
    def _add_legend(self, parent, label, color):
        f = tk.Frame(parent)
        f.pack(anchor='w', pady=2)
        c = tk.Canvas(f, width=20, height=20)
        c.pack(side=tk.LEFT)

        if label == "Đường đi":
            # Vẽ đường thẳng ngang (line)
            c.create_line(2, 10, 18, 10, fill=color, width=3)
        else:
            # Vẽ hình tròn (oval)
            c.create_oval(2, 2, 18, 18, fill=color, outline=color)

        tk.Label(f, text=label).pack(side=tk.RIGHT, padx=5)
    
    def _prepare_map(self):
        self.btn_start.config(state=tk.DISABLED)
        # khởi tạo bản đồ, start/goal
        self.mmap = Map.map_init(10,10)
        self.goals = Map.map_random(self.mmap)   # list of 3 goals
        self.start = Map.random_curpos(self.mmap)
        # vẽ grid + obstacles + goals
        self.t.clear()
        Map.draw_map(self.mmap, 'pink', self.t, self.width_half, self.height_half)
        # place turtle at start
        sx, sy = Map.turn2pixel(self.mmap, self.height_half, self.width_half, *self.start)
        self.t.up(); self.t.goto(sx, sy); self.t.down()
        self.btn_start.config(state=tk.NOMAL)
    
    def start(self):
        self.btn_start.config(state=tk.DISABLED)
        t0 = perf_counter()
        
        # chạy A*
        complete_run = Map.run(self.t, self.mmap, self.width_half, self.height_half, self.start, self.goals)
        
        dt = perf_counter() - t0
        if complete_run:
            info_text = f"Giải mã thành công!\nThời gian giải mã: {dt:.3f} giây"
            self.info_label.config(text=info_text, fg="green")
        else:
            info_text = f"Giải mã thất bại!\nThời gian giải mã: {dt:.3f} giây"
            self.info_label.config(text=info_text, fg="red")

        # hiện info + nút finish/reset
        self.info_label.pack(pady=(20,5))
        self.btn_finish.pack(fill=tk.X, pady=2)
        self.btn_reset.pack(fill=tk.X, pady=2)
    
    def reset(self):
        # ẩn info & nút finish/reset, hiện lại start
        self.info_label.pack_forget()
        self.btn_finish.pack_forget()
        self.btn_reset.pack_forget()
        self.btn_start.config(state=tk.NORMAL)
        # reset map & redraw
        self._prepare_map()
