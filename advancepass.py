import tkinter as tk
from tkinter import ttk, messagebox
import string
import secrets

# ==========================
# PASSWORD GENERATOR
# ==========================

def generate_password():
    try:
        length = int(length_var.get())

        if length < 4:
            messagebox.showerror(
                "Error",
                "Password length must be at least 4."
            )
            return

        use_upper = upper_var.get()
        use_lower = lower_var.get()
        use_digits = digit_var.get()
        use_symbols = symbol_var.get()
        exclude_similar = exclude_var.get()

        if not (use_upper or use_lower or use_digits or use_symbols):
            messagebox.showerror(
                "Error",
                "Select at least one character type."
            )
            return

        uppercase = string.ascii_uppercase
        lowercase = string.ascii_lowercase
        digits = string.digits
        symbols = "!@#$%^&*()-_=+[]{};:,.<>?/"

        # Exclude confusing characters
        similar_chars = "0O1lI"

        if exclude_similar:
            uppercase = ''.join(
                c for c in uppercase if c not in similar_chars
            )
            lowercase = ''.join(
                c for c in lowercase if c not in similar_chars
            )
            digits = ''.join(
                c for c in digits if c not in similar_chars
            )

        character_pool = ""
        password_chars = []

        # Security rules
        if use_upper:
            character_pool += uppercase
            password_chars.append(secrets.choice(uppercase))

        if use_lower:
            character_pool += lowercase
            password_chars.append(secrets.choice(lowercase))

        if use_digits:
            character_pool += digits
            password_chars.append(secrets.choice(digits))

        if use_symbols:
            character_pool += symbols
            password_chars.append(secrets.choice(symbols))

        # Fill remaining password length
        while len(password_chars) < length:
            password_chars.append(
                secrets.choice(character_pool)
            )

        # Secure shuffle
        secrets.SystemRandom().shuffle(password_chars)

        password = ''.join(password_chars)

        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)

        check_strength(password)

    except ValueError:
        messagebox.showerror(
            "Error",
            "Please enter a valid number."
        )

# ==========================
# PASSWORD STRENGTH
# ==========================

def check_strength(password):
    score = 0

    if len(password) >= 8:
        score += 1

    if len(password) >= 12:
        score += 1

    if any(c.isupper() for c in password):
        score += 1

    if any(c.islower() for c in password):
        score += 1

    if any(c.isdigit() for c in password):
        score += 1

    if any(c in string.punctuation for c in password):
        score += 1

    if score <= 2:
        strength_label.config(
            text="Weak",
            fg="red"
        )

    elif score <= 4:
        strength_label.config(
            text="Medium",
            fg="orange"
        )

    else:
        strength_label.config(
            text="Strong",
            fg="green"
        )

# ==========================
# COPY PASSWORD
# ==========================

def copy_password():
    password = password_entry.get()

    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        root.update()

        messagebox.showinfo(
            "Copied",
            "Password copied to clipboard!"
        )

# ==========================
# CLEAR
# ==========================

def clear_all():
    password_entry.delete(0, tk.END)
    strength_label.config(text="", fg="black")

# ==========================
# GUI WINDOW
# ==========================

root = tk.Tk()
root.title("Advanced Password Generator")
root.geometry("550x550")
root.resizable(False, False)
root.configure(bg="#f0f4f8")

# ==========================
# TITLE
# ==========================

title = tk.Label(
    root,
    text="🔐 Advanced Password Generator",
    font=("Arial", 18, "bold"),
    bg="#f0f4f8",
    fg="#1f4e79"
)
title.pack(pady=15)

# ==========================
# LENGTH FRAME
# ==========================

length_frame = tk.Frame(root, bg="#f0f4f8")
length_frame.pack(pady=10)

tk.Label(
    length_frame,
    text="Password Length:",
    font=("Arial", 11),
    bg="#f0f4f8"
).grid(row=0, column=0, padx=5)

length_var = tk.StringVar(value="12")

length_entry = ttk.Entry(
    length_frame,
    textvariable=length_var,
    width=10
)
length_entry.grid(row=0, column=1)

# ==========================
# OPTIONS
# ==========================

options_frame = tk.LabelFrame(
    root,
    text="Character Options",
    font=("Arial", 11, "bold"),
    padx=10,
    pady=10
)
options_frame.pack(
    fill="x",
    padx=20,
    pady=15
)

upper_var = tk.BooleanVar(value=True)
lower_var = tk.BooleanVar(value=True)
digit_var = tk.BooleanVar(value=True)
symbol_var = tk.BooleanVar(value=True)
exclude_var = tk.BooleanVar()

tk.Checkbutton(
    options_frame,
    text="Uppercase Letters (A-Z)",
    variable=upper_var
).pack(anchor="w")

tk.Checkbutton(
    options_frame,
    text="Lowercase Letters (a-z)",
    variable=lower_var
).pack(anchor="w")

tk.Checkbutton(
    options_frame,
    text="Numbers (0-9)",
    variable=digit_var
).pack(anchor="w")

tk.Checkbutton(
    options_frame,
    text="Symbols (!@#$%^&*)",
    variable=symbol_var
).pack(anchor="w")

tk.Checkbutton(
    options_frame,
    text="Exclude Similar Characters (0,O,1,l,I)",
    variable=exclude_var
).pack(anchor="w")

# ==========================
# GENERATE BUTTON
# ==========================

generate_btn = tk.Button(
    root,
    text="Generate Password",
    font=("Arial", 11, "bold"),
    bg="#4CAF50",
    fg="white",
    command=generate_password
)
generate_btn.pack(pady=10)

# ==========================
# PASSWORD DISPLAY
# ==========================

password_entry = tk.Entry(
    root,
    width=35,
    font=("Consolas", 15),
    justify="center"
)
password_entry.pack(pady=15)

# ==========================
# STRENGTH
# ==========================

strength_frame = tk.Frame(root, bg="#f0f4f8")
strength_frame.pack()

tk.Label(
    strength_frame,
    text="Password Strength:",
    font=("Arial", 11),
    bg="#f0f4f8"
).pack(side=tk.LEFT)

strength_label = tk.Label(
    strength_frame,
    text="",
    font=("Arial", 11, "bold"),
    bg="#f0f4f8"
)
strength_label.pack(side=tk.LEFT, padx=5)

# ==========================
# BUTTONS
# ==========================

button_frame = tk.Frame(root, bg="#f0f4f8")
button_frame.pack(pady=20)

copy_btn = tk.Button(
    button_frame,
    text="Copy Password",
    bg="#2196F3",
    fg="white",
    width=15,
    command=copy_password
)
copy_btn.grid(row=0, column=0, padx=10)

clear_btn = tk.Button(
    button_frame,
    text="Clear",
    bg="#f44336",
    fg="white",
    width=15,
    command=clear_all
)
clear_btn.grid(row=0, column=1, padx=10)

# ==========================
# FOOTER
# ==========================

footer = tk.Label(
    root,
    text="Secure Password Generator using Python & Tkinter",
    bg="#f0f4f8",
    fg="gray"
)
footer.pack(side="bottom", pady=10)

# ==========================
# RUN APPLICATION
# ==========================

root.mainloop()