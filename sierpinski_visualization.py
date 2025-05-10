import os
import random
import math
import tkinter as tk
from tkinter import ttk, colorchooser, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Ensure output directories exist
os.makedirs('images', exist_ok=True)
os.makedirs('logs', exist_ok=True)


def generate_triangle_points(n=10000):
    """Chaos game for 2D Sierpinski triangle with burn-in."""
    verts = [(0, 0), (1, 0), (0.5, math.sqrt(3) / 2)]
    x, y = random.random(), random.random()
    for _ in range(10):  # burn-in
        vx, vy = random.choice(verts)
        x, y = (x + vx) / 2, (y + vy) / 2
    pts = []
    for _ in range(n):
        vx, vy = random.choice(verts)
        x, y = (x + vx) / 2, (y + vy) / 2
        pts.append((x, y))
    return pts


def generate_diamond_points(n=10000):
    """Diamond from mirrored Sierpinski triangles."""
    base = generate_triangle_points(n)
    inverted = [(x, -y) for x, y in base]
    return base + inverted


def generate_tetrahedron_points(n=10000):
    """Chaos game for 3D Sierpinski tetrahedron with burn-in."""
    verts = [
        (0, 0, 0), (1, 0, 0),
        (0.5, math.sqrt(3) / 2, 0),
        (0.5, math.sqrt(3) / 6, math.sqrt(6) / 3)
    ]
    x, y, z = random.random(), random.random(), random.random()
    for _ in range(10):  # burn-in
        vx, vy, vz = random.choice(verts)
        x, y, z = (x + vx) / 2, (y + vy) / 2, (z + vz) / 2
    pts = []
    for _ in range(n):
        vx, vy, vz = random.choice(verts)
        x, y, z = (x + vx) / 2, (y + vy) / 2, (z + vz) / 2
        pts.append((x, y, z))
    return pts


class SierpinskiApp(tk.Tk):
    """Tkinter GUI for Sierpinski fractals with responsive controls."""
    def __init__(self):
        super().__init__()
        self.title("Sierpinski Fractal Viewer")
        self.default_w, self.default_h = 1200, 700
        self.geometry(f"{self.default_w}x{self.default_h}")

        # Color states
        self.point_color = (0, 0, 1)
        self.bg_color = (1, 1, 1)

        # UI variables
        self.shape_var = tk.StringVar(master=self, value='all')
        self.points_var = tk.IntVar(master=self, value=10000)
        self.width_var = tk.IntVar(master=self, value=self.default_w)
        self.height_var = tk.IntVar(master=self, value=self.default_h)
        self.save_params = tk.BooleanVar(master=self, value=False)

        self._build_ui()
        self.bind('<Configure>', self._on_resize)

    def _build_ui(self):
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)

        ctrl = ttk.Frame(paned, padding=10)
        paned.add(ctrl, weight=0)
        canvas_fr = ttk.Frame(paned, padding=10)
        paned.add(canvas_fr, weight=1)

        # Controls
        row = 0
        for label, var, opts in [
            ('Shape:', self.shape_var, {'values': ['triangle','diamond','tetrahedron','all'], 'state': 'readonly'}),
            ('Points:', self.points_var, {}),
            ('Window W:', self.width_var, {}),
            ('Window H:', self.height_var, {}),
        ]:
            ttk.Label(ctrl, text=label).grid(row=row, column=0, sticky='w', pady=4)
            if label == 'Shape:':
                ttk.Combobox(ctrl, textvariable=var, **opts).grid(row=row, column=1, sticky='ew', padx=5)
            else:
                ttk.Entry(ctrl, textvariable=var).grid(row=row, column=1, sticky='ew', padx=5)
            row += 1

        # Sliders
        ttk.Label(ctrl, text='Adjust Points').grid(row=row, column=0, sticky='w', pady=4)
        ttk.Scale(ctrl, from_=1000, to=200000, variable=self.points_var, orient=tk.HORIZONTAL).grid(
            row=row, column=1, sticky='ew', padx=5)
        row += 1
        ttk.Label(ctrl, text='Adjust Width').grid(row=row, column=0, sticky='w', pady=4)
        ttk.Scale(ctrl, from_=300, to=2000, variable=self.width_var, orient=tk.HORIZONTAL).grid(
            row=row, column=1, sticky='ew', padx=5)
        row += 1
        ttk.Label(ctrl, text='Adjust Height').grid(row=row, column=0, sticky='w', pady=4)
        ttk.Scale(ctrl, from_=200, to=1200, variable=self.height_var, orient=tk.HORIZONTAL).grid(
            row=row, column=1, sticky='ew', padx=5)
        row += 1

        # Color pickers
        ttk.Label(ctrl, text='Point Color').grid(row=row, column=0, sticky='w', pady=4)
        self.point_preview = ttk.Label(ctrl, background=self._hex(self.point_color), width=3)
        self.point_preview.grid(row=row, column=1, sticky='w')
        ttk.Button(ctrl, text='Choose', command=self._choose_point_color).grid(row=row, column=2, padx=5)
        row += 1
        ttk.Label(ctrl, text='BG Color').grid(row=row, column=0, sticky='w', pady=4)
        self.bg_preview = ttk.Label(ctrl, background=self._hex(self.bg_color), width=3)
        self.bg_preview.grid(row=row, column=1, sticky='w')
        ttk.Button(ctrl, text='Choose', command=self._choose_bg_color).grid(row=row, column=2, padx=5)
        row += 1

        # Save options
        ttk.Checkbutton(ctrl, text='Save Params', variable=self.save_params).grid(
            row=row, column=0, columnspan=2, sticky='w', pady=4)
        row += 1
        ttk.Button(ctrl, text='Plot', command=self.plot).grid(row=row, column=0, columnspan=3, sticky='ew', pady=6)
        row += 1
        ttk.Button(ctrl, text='Save Image', command=self._save_image).grid(
            row=row, column=0, columnspan=3, sticky='ew')

        ctrl.grid_columnconfigure(1, weight=1)

        # Canvas
        self.figure = plt.Figure(figsize=(8,6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=canvas_fr)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _hex(self, rgb):
        return '#{:02x}{:02x}{:02x}'.format(*(int(c * 255) for c in rgb))

    def _choose_point_color(self):
        init = self._hex(self.point_color)
        chosen = colorchooser.askcolor(initialcolor=init)
        if chosen[0]:
            self.point_color = tuple(v/255 for v in chosen[0])
            self.point_preview.configure(background=self._hex(self.point_color))

    def _choose_bg_color(self):
        init = self._hex(self.bg_color)
        chosen = colorchooser.askcolor(initialcolor=init)
        if chosen[0]:
            self.bg_color = tuple(v/255 for v in chosen[0])
            self.bg_preview.configure(background=self._hex(self.bg_color))

    def _on_resize(self, event):
        if event.widget == self:
            self.width_var.set(event.width)
            self.height_var.set(event.height)

    def plot(self):
        # Apply window size
        w, h = self.width_var.get(), self.height_var.get()
        self.geometry(f"{w}x{h}")

        self.figure.clf()
        self.figure.patch.set_facecolor(self.bg_color)

        shape = self.shape_var.get()
        count = self.points_var.get()
        shapes = ['triangle','diamond','tetrahedron'] if shape=='all' else [shape]

        for idx, shp in enumerate(shapes, start=1):
            proj = '3d' if shp=='tetrahedron' else None
            ax = self.figure.add_subplot(1,len(shapes),idx, projection=proj)
            ax.set_facecolor(self.bg_color)
            if shp=='triangle':
                pts = generate_triangle_points(count)
                xs,ys = zip(*pts)
                ax.scatter(xs, ys, s=0.5, color=self.point_color)
                ax.set_title('Triangle')
            elif shp=='diamond':
                pts = generate_diamond_points(count)
                xs,ys = zip(*pts)
                ax.scatter(xs, ys, s=0.5, color=self.point_color)
                ax.set_title('Diamond')
            elif shp=='tetrahedron':
                pts = generate_tetrahedron_points(count)
                xs,ys,zs = zip(*pts)
                ax.scatter(xs, ys, zs, s=0.5, color=self.point_color)
                ax.view_init(elev=20, azim=30)
                ax.set_title('Tetrahedron')
            ax.axis('off')

        self.figure.tight_layout()
        self.canvas.draw()

    def _save_image(self):
        # Save image in images folder
        filename = filedialog.asksaveasfilename(defaultextension='.png', initialdir='images', filetypes=[('PNG','*.png')])
        if not filename: return
        if not filename.startswith('images'): filename = os.path.join('images', os.path.basename(filename))
        self.figure.savefig(filename)
        # Save params log in logs folder
        if self.save_params.get():
            base = os.path.splitext(os.path.basename(filename))[0]
            log_path = os.path.join('logs', f'{base}_params.txt')
            with open(log_path, 'w') as f:
                f.write(f"Shape: {self.shape_var.get()}\nPoints: {self.points_var.get()}\n")
                f.write(f"Point Color: {self.point_color}\nBG Color: {self.bg_color}\n")
                f.write(f"Window: {self.width_var.get()}x{self.height_var.get()}\n")

if __name__ == '__main__':
    SierpinskiApp().mainloop()