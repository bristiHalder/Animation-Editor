import tkinter as tk
from tkinter import messagebox
import random
import math

class AnimationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Animation Creator")
        
        # Create a frame for the left panel (controls)
        self.left_frame = tk.Frame(root, width=200, bg="#f0f0f0", padx=10, pady=10)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Create a frame for the main panel (animation display)
        self.main_frame = tk.Frame(root, bg="white")
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create the main canvas for animations
        self.main_canvas = tk.Canvas(self.main_frame, bg="white", width=800, height=600)
        self.main_canvas.pack(fill=tk.BOTH, expand=True)

        # Initialize shape options and animation curves
        self.shape_options = ["Square", "Oval", "Triangle"]
        self.animation_options = ["Jump", "Diagonal"]
        
        # Create StringVar for dropdown selections
        self.selected_shape = tk.StringVar(value=self.shape_options[0])
        self.selected_animation = tk.StringVar(value=self.animation_options[0])

        # Add buttons to the left panel
        self.shape_frame = tk.LabelFrame(self.left_frame, text="Select Shape", bg="#e0e0e0", padx=10, pady=10)
        self.shape_frame.pack(pady=10, fill=tk.X)

        for shape in self.shape_options:
            button = tk.Button(self.shape_frame, text=shape, command=lambda s=shape: self.display_shape(s))
            button.pack(pady=5)

        self.change_color_button = tk.Button(self.left_frame, text="Change Color", command=self.change_color)
        self.change_color_button.pack(pady=10)
       
        self.animate_color_button = tk.Button(self.left_frame, text="Animate Color", command=self.animate_color)
        self.animate_color_button.pack(pady=10)

        # Animation selection dropdown
        self.animation_menu = tk.OptionMenu(self.left_frame, self.selected_animation, *self.animation_options)
        self.animation_menu.pack(pady=10)

        # Toggle button for smooth transitions
        self.smooth_transition_var = tk.BooleanVar(value=False)
        self.smooth_transition_toggle = tk.Checkbutton(self.left_frame, text="Smooth Transitions", variable=self.smooth_transition_var, bg="#f0f0f0")
        self.smooth_transition_toggle.pack(pady=10)

        self.stop_animation_button = tk.Button(self.left_frame, text="Stop Animation", command=self.stop_animation)
        self.stop_animation_button.pack(pady=10)

        self.start_again_button = tk.Button(self.left_frame, text="Start Again", command=self.start_again)
        self.start_again_button.pack(pady=10)

        # Add resizing slider
        self.size_label = tk.Label(self.left_frame, text="Size")
        self.size_label.pack(pady=10)
        self.size_slider = tk.Scale(self.left_frame, from_=20, to_=200, orient=tk.HORIZONTAL, command=self.resize_shape)
        self.size_slider.set(100)
        self.size_slider.pack(pady=10)

        self.color_change_interval = 100  # Interval in milliseconds for color animation
        self.animating_color = False
        self.animating = False
        self.shape_id = None
        self.current_shape = None
        self.color = "blue"
        self.shape_size = 100  # Default shape size

    def display_shape(self, shape):
        self.main_canvas.delete("all")  # Clear previous shape
        self.current_shape = shape
        self.shape_size = self.size_slider.get()  # Get the current size from slider
        if shape == "Square":
            self.shape_id = self.main_canvas.create_rectangle(50, 50, 50 + self.shape_size, 50 + self.shape_size, fill=self.color)
        elif shape == "Oval":
            self.shape_id = self.main_canvas.create_oval(50, 50, 50 + self.shape_size, 50 + self.shape_size, fill=self.color)
        elif shape == "Triangle":
            self.shape_id = self.main_canvas.create_polygon(50, 50 + self.shape_size, 50 + self.shape_size / 2, 50, 50 + self.shape_size, 50 + self.shape_size, fill=self.color)
        self.animate_shape()  # Automatically start animation

    def resize_shape(self, value):
        if self.shape_id:
            self.shape_size = int(value)
            if self.current_shape == "Square":
                self.main_canvas.coords(self.shape_id, 50, 50, 50 + self.shape_size, 50 + self.shape_size)
            elif self.current_shape == "Oval":
                self.main_canvas.coords(self.shape_id, 50, 50, 50 + self.shape_size, 50 + self.shape_size)
            elif self.current_shape == "Triangle":
                self.main_canvas.coords(self.shape_id, 50, 50 + self.shape_size, 50 + self.shape_size / 2, 50, 50 + self.shape_size, 50 + self.shape_size)

    def change_color(self):
        self.color = self.random_color()
        if self.shape_id:
            self.main_canvas.itemconfig(self.shape_id, fill=self.color)

    def animate_shape(self):
        if self.shape_id and self.current_shape:
            animation_type = self.selected_animation.get()
            self.animating = True
            if animation_type == "Jump":
                self.animate_curve()
            elif animation_type == "Diagonal":
                self.animate_diagonal()
            else:
                messagebox.showerror("Invalid Animation Type", "Please choose a valid animation type.")
        else:
            messagebox.showerror("Animation Error", "Please select a shape first.")

    def animate_bounce(self):
        if self.shape_id and self.animating:
            width = self.main_canvas.winfo_width()
            height = self.main_canvas.winfo_height()
            amplitude = 100
            frequency = 0.02
            y_offset = amplitude * math.sin(frequency * (self.root.winfo_screenwidth() // 2))
            step = 10
            delay = 40

            for t in range(0, width, step):
                if not self.animating:
                    break
                x = t
                y = amplitude * math.sin(frequency * t) + height / 2 + y_offset
                if x + self.shape_size > width:
                    x = width - self.shape_size
                if y + self.shape_size > height:
                    y = height - self.shape_size
                if self.current_shape == "Square":
                    self.main_canvas.coords(self.shape_id, x, y, x + self.shape_size, y + self.shape_size)
                elif self.current_shape == "Oval":
                    self.main_canvas.coords(self.shape_id, x, y, x + self.shape_size, y + self.shape_size)
                elif self.current_shape == "Triangle":
                    self.main_canvas.coords(self.shape_id, x, y, x + self.shape_size / 2, y - self.shape_size, x + self.shape_size, y)
                self.root.update()
                self.root.after(delay)

    def animate_curve(self):
        if self.shape_id and self.animating:
            width = self.main_canvas.winfo_width()
            height = self.main_canvas.winfo_height()
            step = 10
            delay = 40

            for t in range(0, width, step):
                if not self.animating:
                    break
                x = t
                y = 0.01 * (x - width / 2) ** 2 + height / 2  # Parabolic curve
                if x + self.shape_size > width:
                    x = width - self.shape_size
                if y + self.shape_size > height:
                    y = height - self.shape_size
                if self.current_shape == "Square":
                    self.main_canvas.coords(self.shape_id, x, y, x + self.shape_size, y + self.shape_size)
                elif self.current_shape == "Oval":
                    self.main_canvas.coords(self.shape_id, x, y, x + self.shape_size, y + self.shape_size)
                elif self.current_shape == "Triangle":
                    self.main_canvas.coords(self.shape_id, x, y, x + self.shape_size / 2, y - self.shape_size, x + self.shape_size, y)
                self.root.update()
                self.root.after(delay)

    def animate_diagonal(self):
        if self.shape_id and self.animating:
            width = self.main_canvas.winfo_width()
            height = self.main_canvas.winfo_height()
            step = 10
            delay = 40

            for t in range(0, width, step):
                if not self.animating:
                    break
                x = t
                y = (height / width) * x  # Diagonal line
                if x + self.shape_size > width:
                    x = width - self.shape_size
                if y + self.shape_size > height:
                    y = height - self.shape_size
                if self.current_shape == "Square":
                    self.main_canvas.coords(self.shape_id, x, y, x + self.shape_size, y + self.shape_size)
                elif self.current_shape == "Oval":
                    self.main_canvas.coords(self.shape_id, x, y, x + self.shape_size, y + self.shape_size)
                elif self.current_shape == "Triangle":
                    self.main_canvas.coords(self.shape_id, x, y, x + self.shape_size / 2, y - self.shape_size, x + self.shape_size, y)
                self.root.update()
                self.root.after(delay)

    def animate_color(self):
        if self.shape_id:
            self.animating_color = True
            self._animate_color_step()

    def _animate_color_step(self):
        if self.animating_color:
            new_color = self.random_color()
            self.main_canvas.itemconfig(self.shape_id, fill=new_color)
            self.root.after(self.color_change_interval, self._animate_color_step)

    def start_again(self):
        self.main_canvas.delete("all")
        self.shape_id = None
        self.current_shape = None
        self.animating = False
        self.animating_color = False

    def stop_animation(self):
        self.animating = False
        self.animating_color = False

    def random_color(self):
        return f'#{random.randint(0, 0xFFFFFF):06x}'

if __name__ == "__main__":
    root = tk.Tk()
    app = AnimationApp(root)
    root.mainloop()
