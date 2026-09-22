import math
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Обработка изображений - Вариант 16")
        self.root.geometry("1240x720")

        self.src_image = None
        self.dst_image = None
        self.src_marked = None
        self.tk_src = None
        self.tk_dst = None

        top_bar = tk.Frame(root, pady=8)
        top_bar.pack(side=tk.TOP, fill=tk.X, padx=10)

        tk.Label(top_bar, text="W:", font=("Tahoma", 8)).pack(side=tk.LEFT, padx=1)
        self.entry_w = tk.Entry(top_bar, width=5, font=("Tahoma", 8))
        self.entry_w.insert(0, "600")
        self.entry_w.pack(side=tk.LEFT, padx=2)

        tk.Label(top_bar, text="H:", font=("Tahoma", 8)).pack(side=tk.LEFT, padx=1)
        self.entry_h = tk.Entry(top_bar, width=5, font=("Tahoma", 8))
        self.entry_h.insert(0, "600")
        self.entry_h.pack(side=tk.LEFT, padx=2)

        tk.Button(top_bar, text="Создать 1", font=("Tahoma", 8), command=self.create_canvas).pack(side=tk.LEFT, padx=4)
        tk.Button(top_bar, text="Открыть 2", font=("Tahoma", 8), command=self.load_image).pack(side=tk.LEFT, padx=4)

        tk.Label(top_bar, text="x1:", font=("Tahoma", 8)).pack(side=tk.LEFT, padx=1)
        self.entry_x1 = tk.Entry(top_bar, width=4, font=("Tahoma", 8))
        self.entry_x1.insert(0, "300")
        self.entry_x1.pack(side=tk.LEFT, padx=2)

        tk.Label(top_bar, text="y1:", font=("Tahoma", 8)).pack(side=tk.LEFT, padx=1)
        self.entry_y1 = tk.Entry(top_bar, width=4, font=("Tahoma", 8))
        self.entry_y1.insert(0, "300")
        self.entry_y1.pack(side=tk.LEFT, padx=2)

        tk.Label(top_bar, text="L:", font=("Tahoma", 8)).pack(side=tk.LEFT, padx=1)
        self.entry_leg = tk.Entry(top_bar, width=4, font=("Tahoma", 8))
        self.entry_leg.insert(0, "150")
        self.entry_leg.pack(side=tk.LEFT, padx=2)

        tk.Label(top_bar, text="x2:", font=("Tahoma", 8)).pack(side=tk.LEFT, padx=1)
        self.entry_x2 = tk.Entry(top_bar, width=4, font=("Tahoma", 8))
        self.entry_x2.insert(0, "0")
        self.entry_x2.pack(side=tk.LEFT, padx=2)

        tk.Label(top_bar, text="y2:", font=("Tahoma", 8)).pack(side=tk.LEFT, padx=1)
        self.entry_y2 = tk.Entry(top_bar, width=4, font=("Tahoma", 8))
        self.entry_y2.insert(0, "0")
        self.entry_y2.pack(side=tk.LEFT, padx=2)

        tk.Button(top_bar, text="Перенести", font=("Tahoma", 8), command=self.transfer_fragment).pack(side=tk.LEFT, padx=5)
        tk.Button(top_bar, text="Координаты", font=("Tahoma", 8), command=self.draw_coordinates).pack(side=tk.LEFT, padx=4)
        tk.Button(top_bar, text="|x-1|", font=("Tahoma", 8), command=self.draw_function).pack(side=tk.LEFT, padx=4)

        tk.Button(top_bar, text="Сохранить BMP", font=("Tahoma", 8), command=lambda: self.save_image("BMP")).pack(side=tk.LEFT, padx=4)
        tk.Button(top_bar, text="Сохранить PBM", font=("Tahoma", 8), command=lambda: self.save_image("PBM")).pack(side=tk.LEFT, padx=4)

        panes = tk.Frame(root)
        panes.pack(fill=tk.BOTH, expand=True, padx=12, pady=6)

        left_box = tk.Frame(panes)
        left_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=6)
        tk.Label(left_box, text="Исходное изображение", font=("Tahoma", 9)).pack(anchor="center", pady=2)
        self.canvas_src = tk.Canvas(left_box, bg="white", highlightthickness=1, highlightbackground="gray80")
        self.canvas_src.pack(fill=tk.BOTH, expand=True)

        right_box = tk.Frame(panes)
        right_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=6)
        tk.Label(right_box, text="Обработанное изображение", font=("Tahoma", 9)).pack(anchor="center", pady=2)
        self.canvas_dst = tk.Canvas(right_box, bg="white", highlightthickness=1, highlightbackground="gray80")
        self.canvas_dst.pack(fill=tk.BOTH, expand=True)

    def create_canvas(self):
        try:
            w = int(self.entry_w.get())
            h = int(self.entry_h.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Размеры холста должны быть целыми числами!")
            return

        self.dst_image = Image.new("RGB", (w, h), (255, 255, 255))
        self.entry_x1.delete(0, tk.END)
        self.entry_x1.insert(0, str(w // 2))
        self.entry_y1.delete(0, tk.END)
        self.entry_y1.insert(0, str(h // 2))

        self.display_image(self.dst_image, self.canvas_dst, is_src=False)

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Изображения", "*.bmp *.png *.jpg *.jpeg *.ppm")])
        if not path:
            return
        loaded = Image.open(path)
        if loaded.mode != "RGB":
            messagebox.showinfo("project1", "invalid pixel color format. trying to convert")
            self.src_image = Image.new("RGB", loaded.size, (255, 255, 255))
            self.src_image.paste(loaded)
        else:
            self.src_image = loaded.copy()

        self.src_marked = self.src_image.copy()

        sw, sh = self.src_image.size
        self.entry_x2.delete(0, tk.END)
        self.entry_x2.insert(0, str(sw // 2))
        self.entry_y2.delete(0, tk.END)
        self.entry_y2.insert(0, str(sh // 2))

        self.display_image(self.src_marked, self.canvas_src, is_src=True)

    def transfer_fragment(self):
        if self.src_image is None or self.dst_image is None:
            messagebox.showwarning("Предупреждение", "Сначала создайте холст 1 и откройте изображение 2!")
            return

        try:
            x1 = int(self.entry_x1.get())
            y1 = int(self.entry_y1.get())
            leg = int(self.entry_leg.get())
            x2 = int(self.entry_x2.get())
            y2 = int(self.entry_y2.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Все параметры координат должны быть числами!")
            return

        w, h = self.dst_image.size
        sw, sh = self.src_image.size
        dst_pix = self.dst_image.load()
        src_pix = self.src_image.load()

        self.src_marked = self.src_image.copy()
        src_marked_pix = self.src_marked.load()

        for y in range(h):
            for x in range(w):
                u = x1 - x
                v = y1 - y

                if 0 <= u <= leg and 0 <= v <= leg and v < u:
                    sx = x2 - u
                    sy = y2 - v
                    if 0 <= sx < sw and 0 <= sy < sh:
                        dst_pix[x, y] = src_pix[sx, sy]
                    else:
                        dst_pix[x, y] = (0, 0, 0)
                elif 0 <= u <= leg and 0 <= v <= leg and v == u:
                    dst_pix[x, y] = (0, 180, 0)
                    sx = x2 - u
                    sy = y2 - v
                    if 0 <= sx < sw and 0 <= sy < sh:
                        src_marked_pix[sx, sy] = (255, 60, 60)

        self.display_image(self.src_marked, self.canvas_src, is_src=True)
        self.display_image(self.dst_image, self.canvas_dst, is_src=False)

    def draw_coordinates(self):
        if self.dst_image is None:
            messagebox.showwarning("Предупреждение", "Сначала создайте холст!")
            return

        w, h = self.dst_image.size
        dst_pix = self.dst_image.load()
        cx, cy = w // 2, h // 2

        for x in range(15, w - 15):
            dst_pix[x, cy] = (0, 0, 0)
        for i in range(1, 8):
            if cy - (i // 2) >= 0:
                dst_pix[w - 15 - i, cy - (i // 2)] = (0, 0, 0)
            if cy + (i // 2) < h:
                dst_pix[w - 15 - i, cy + (i // 2)] = (0, 0, 0)

        for y in range(15, h - 15):
            dst_pix[cx, y] = (0, 0, 0)
        for i in range(1, 8):
            if cx - (i // 2) >= 0 and 15 + i < h:
                dst_pix[cx - (i // 2), 15 + i] = (0, 0, 0)
            if cx + (i // 2) < w and 15 + i < h:
                dst_pix[cx + (i // 2), 15 + i] = (0, 0, 0)

        self.display_image(self.dst_image, self.canvas_dst, is_src=False)

    def draw_function(self):
        if self.dst_image is None:
            messagebox.showwarning("Предупреждение", "Сначала создайте холст!")
            return

        w, h = self.dst_image.size
        dst_pix = self.dst_image.load()
        cx, cy = w // 2, h // 2
        scale = 35.0

        prev_py = None
        for px in range(15, w - 15):
            math_x = (px - cx) / scale
            math_y = abs(math_x - 1.0)
            py = int(round(cy - math_y * scale))

            if 0 <= py < h:
                for dy in (0, 1):
                    if 0 <= py + dy < h:
                        dst_pix[px, py + dy] = (0, 0, 0)

                if prev_py is not None:
                    step = 1 if py > prev_py else -1
                    for y_mid in range(prev_py, py, step):
                        if 0 <= y_mid < h:
                            dst_pix[px, y_mid] = (0, 0, 0)
            prev_py = py

        self.display_image(self.dst_image, self.canvas_dst, is_src=False)

    def display_image(self, img, canvas, is_src=False):
        c_w = canvas.winfo_width()
        c_h = canvas.winfo_height()
        if c_w <= 1 or c_h <= 1:
            c_w, c_h = 560, 560

        rendered = img.copy()
        rendered.thumbnail((c_w, c_h), Image.Resampling.LANCZOS)
        tk_img = ImageTk.PhotoImage(rendered)

        if is_src:
            self.tk_src = tk_img
        else:
            self.tk_dst = tk_img

        canvas.delete("all")
        canvas.create_image(c_w // 2, c_h // 2, anchor="center", image=tk_img)

    def save_image(self, fmt):
        if self.dst_image is None:
            messagebox.showwarning("Внимание", "Сначала сформируйте изображение!")
            return

        ext = ".bmp" if fmt == "BMP" else ".pbm"
        path = filedialog.asksaveasfilename(defaultextension=ext, filetypes=[(f"{fmt} files", f"*{ext}")])
        if not path:
            return

        if fmt == "PBM":
            self.dst_image.convert("1").save(path)
        else:
            self.dst_image.save(path)
        messagebox.showinfo("Готово", f"Файл сохранен:\n{path}")


if __name__ == "__main__":
    app_root = tk.Tk()
    App(app_root)
    app_root.mainloop()