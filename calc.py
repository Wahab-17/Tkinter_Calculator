import tkinter as tk
from tkinter import font


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Modern Tkinter Calculator")
        self.configure(bg="#0f1724")
        self.geometry("360x520")
        self.minsize(300, 420)

        self._expression = ""
        self._create_widgets()
        self._bind_keys()

    def _create_widgets(self):
        display_font = font.Font(family="Segoe UI", size=28, weight="bold")
        btn_font = font.Font(family="Segoe UI", size=16, weight="normal")

        # Display
        self.display_var = tk.StringVar()
        display_frame = tk.Frame(self, bg="#0f1724")
        display_frame.pack(fill="both", padx=12, pady=(16, 8))

        self.display = tk.Entry(
            display_frame,
            textvariable=self.display_var,
            font=display_font,
            bd=0,
            bg="#071025",
            fg="#e6f0ff",
            justify="right",
            relief="flat",
        )
        self.display.pack(fill="both", ipady=18, padx=4)

        # Buttons area
        buttons_frame = tk.Frame(self, bg="#0f1724")
        buttons_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Button configuration: label, column span, background, foreground
        buttons = [
            [("AC", 1, "#ff5c5c", "#fff"), ("C", 1, "#ff9f43", "#fff"), ("%", 1, "#00a8ff", "#fff"), ("/", 1, "#00a8ff", "#fff")],
            [("7", 1, "#1f2937", "#fff"), ("8", 1, "#1f2937", "#fff"), ("9", 1, "#1f2937", "#fff"), ("*", 1, "#00a8ff", "#fff")],
            [("4", 1, "#1f2937", "#fff"), ("5", 1, "#1f2937", "#fff"), ("6", 1, "#1f2937", "#fff"), ("-", 1, "#00a8ff", "#fff")],
            [("1", 1, "#1f2937", "#fff"), ("2", 1, "#1f2937", "#fff"), ("3", 1, "#1f2937", "#fff"), ("+", 1, "#00a8ff", "#fff")],
            [("0", 2, "#1f2937", "#fff"), (".", 1, "#1f2937", "#fff"), ("=", 1, "#00d084", "#fff")],
        ]

        for r, row in enumerate(buttons):
            for c, (text, colspan, bg, fg) in enumerate(row):
                btn = tk.Button(
                    buttons_frame,
                    text=text,
                    font=btn_font,
                    bd=0,
                    bg=bg,
                    fg=fg,
                    activebackground=self._darken(bg, 0.9),
                    activeforeground=fg,
                    relief="flat",
                    command=lambda t=text: self._on_button_click(t),
                )
                grid_col = sum(item[1] for item in row[:c])
                btn.grid(row=r, column=grid_col, columnspan=colspan, sticky="nsew", padx=6, pady=6)

        # Configure grid weights so it resizes nicely
        max_cols = 4
        for i in range(6):
            buttons_frame.rowconfigure(i, weight=1)
        for j in range(max_cols):
            buttons_frame.columnconfigure(j, weight=1)

    def _on_button_click(self, char):
        if char == "=":
            self._calculate()
        elif char == "C":
            self._clear_entry()
        elif char == "AC":
            self._all_clear()
        else:
            self._add_to_expression(char)

    def _add_to_expression(self, char):
        # Prevent consecutive operators (minor polish)
        if char in "+-*/%":
            if not self._expression or self._expression[-1] in "+-*/%":
                return
        self._expression += str(char)
        self.display_var.set(self._expression)

    def _clear_entry(self):
        # remove last char
        self._expression = self._expression[:-1]
        self.display_var.set(self._expression)

    def _all_clear(self):
        self._expression = ""
        self.display_var.set("")

    def _safe_eval(self, expr):
        allowed_chars = "0123456789+-*/(). %"
        for ch in expr:
            if ch not in allowed_chars:
                raise ValueError("Invalid character")
        # Replace percentage operator for simple percent handling: 'x%' -> '(x/100)'
        # Simple approach: convert occurrences of a number followed by %
        import re

        def repl_percent(match):
            num = match.group(1)
            return f"({num}/100)"

        expr = re.sub(r"(\d+\.?\d*)%", repl_percent, expr)
        return eval(expr)

    def _calculate(self):
        if not self._expression:
            return
        try:
            result = self._safe_eval(self._expression)
            # Format result: remove trailing .0
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self._expression = str(result)
            self.display_var.set(self._expression)
        except Exception:
            self.display_var.set("Error")
            self._expression = ""

    def _bind_keys(self):
        self.bind("<Return>", lambda e: self._calculate())
        self.bind("<BackSpace>", lambda e: self._clear_entry())
        self.bind("<Escape>", lambda e: self._all_clear())
        for key in "0123456789.+-*/%()":
            self.bind(key, lambda e, k=key: self._add_to_expression(k))

    @staticmethod
    def _darken(hex_color, factor=0.85):
        hex_color = hex_color.lstrip("#")
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        r = max(0, int(r * factor))
        g = max(0, int(g * factor))
        b = max(0, int(b * factor))
        return f"#{r:02x}{g:02x}{b:02x}"


if __name__ == "__main__":
    app = Calculator()
    app.mainloop()