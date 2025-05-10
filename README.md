# Sierpinski Fractal Viewer

Welcome to **Sierpinski Fractal Viewer**, a simple yet powerful tool to explore and generate beautiful Sierpinski fractals. It’s built with Python, Tkinter, and Matplotlib—no rocket science required! 🚀

---

## 🔍 Overview

This application lets you:

* **Draw** 2D triangles, 2D diamonds (two mirrored triangles), and 3D tetrahedrons of Sierpinski fractals.
* **Customize**:

  * Number of points (detail level)
  * Point color & background color (live preview!)
  * Window size (width & height with sliders and entries)
* **Plot** fractals in real time with a clean GUI.
* **Save** your artwork as PNGs in an `images/` folder and optionally log your parameters in `logs/`.

---

## 🔢 The Math Behind It

This viewer uses what’s called the **Chaos Game**, which is all about picking random corners and averaging:

1. Start with any point inside your shape (triangle in 2D or tetrahedron in 3D).
2. Pick one of the shape’s vertices at random.
3. Move halfway from your current point toward that vertex:
   *new\_point = (current\_point + chosen\_vertex) / 2*
4. Repeat steps 2–3 thousands of times.

After ignoring the first few points (to let things settle), the remaining points trace out the Sierpinski fractal pattern—no heavy formulas required, just random choices and simple midpoints!

---

## 🚀 Getting Started

```bash
git clone https://github.com/gpximenes/sierpinski-fractal-viewer
cd sierpinski-fractal-viewer
```

Make sure you have Python 3.7+ installed. Then:

```bash
pip install -r requirements.txt
```

Or also:

```bash
pip install matplotlib
```

```bash
python sierpinski_pyramid.py
```

---

## 🎨 Usage Tips

1. **Shape** dropdown: pick `triangle`, `diamond`, `tetrahedron`, or `all`.

2. **Points**: use the slider or type a number for how many points (10,000 is a sweet spot).

3. **Window W/H**: resize via sliders or type exact dimensions.

4. **Save Image**: exports to `images/`. Check “Save Params” to also log details in `logs/`.

> Tip: Larger point counts give smoother fractals but take longer to draw.

---

## 🎨 Images

1. Demo

![demo](https://github.com/user-attachments/assets/b6534a0b-3d9a-4a2d-a296-51992f5434a2)



2. Cyan Diamond

![cyan_diamond](https://github.com/user-attachments/assets/61c24016-043e-4b99-a36f-edf41ae37d77)


