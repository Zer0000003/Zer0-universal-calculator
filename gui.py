"""Zer0ian desktop interface for the existing local mathematics engine."""
from pathlib import Path
from queue import Empty, Queue
import subprocess
import sys
import threading
import tkinter as tk

ROOT = Path(__file__).resolve().parent
BG, PANEL, FIELD = "#080b13", "#101827", "#0b1220"
CYAN, BLUE, PINK = "#20f5ff", "#387bff", "#ff368f"
INK, MUTED, ERROR = "#e7f5ff", "#92a8c5", "#ff719a"
FONT = ("DejaVu Sans Mono", 11)
EXAMPLES = (
    ("ARITHMETIC", "2+3*4"), ("ALGEBRA", "2x+7=19"),
    ("QUADRATIC", "x^2-5x+6=0"), ("SYSTEM", "x+y=10;x-y=2"),
    ("INEQUALITY", "2x+1>5"), ("DERIVATIVE", "diff(x^3+2x,x)"),
    ("INTEGRAL", "integrate(x^2,x,0,3)"), ("LIMIT", "limit(sin(x)/x,x,0)"),
    ("MATRIX", "det([[1,2],[3,4]])"), ("STATISTICS", "mean([2,4,6])"),
    ("PROBABILITY", "binomial_pmf(5,2,1/2)"), ("PRECISION", "approx(pi,50)"),
)
KEYS = (
    ("7", "8", "9", "/", "(", ")"),
    ("4", "5", "6", "*", "x", "y"),
    ("1", "2", "3", "-", "^", "="),
    ("0", ".", "pi", "+", ",", ";"),
    ("sqrt(", "sin(", "cos(", "log(", "[", "]"),
)


def compute(expression):
    """Run a single trusted local expression without a shell."""
    if not expression.strip():
        return False, "Enter a mathematical expression."
    if len(expression) > 4096:
        return False, "Input exceeds 4096 characters."
    try:
        result = subprocess.run(
            [sys.executable, str(ROOT / "engine.py"), expression],
            cwd=ROOT, capture_output=True, text=True, timeout=20, check=False,
        )
    except subprocess.TimeoutExpired:
        return False, "Computation exceeded the 20-second process timeout."
    except (OSError, UnicodeError, ValueError) as exc:
        return False, str(exc)
    output = result.stdout.strip() if result.returncode == 0 else result.stderr.strip()
    if not output:
        output = "No result returned." if result.returncode == 0 else f"Engine exited with code {result.returncode}."
    if len(output) > 30000:
        output = output[:30000] + "\n[Display truncated]"
    return result.returncode == 0, output


class Zer0Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("ZER0 // UNIVERSAL CALCULATOR")
        self.root.configure(bg=BG)
        self.root.geometry("1120x760")
        self.root.minsize(760, 660)
        self.expression = tk.StringVar()
        self.status = tk.StringVar(value="READY // LOCAL ENGINE")
        self.results = Queue()
        self.history = []
        self.busy = False
        self.build()
        self.root.bind("<Return>", self.solve)
        self.root.bind("<Control-l>", self.clear)
        self.root.bind("<Control-Return>", self.solve)
        self.root.after(60, self.poll)

    def label(self, parent, text, color=MUTED, size=10):
        return tk.Label(parent, text=text, fg=color, bg=PANEL,
                        font=("DejaVu Sans Mono", size, "bold"), anchor="w")

    def button(self, parent, text, command, accent=False):
        return tk.Button(parent, text=text, command=command,
                         bg=CYAN if accent else FIELD, fg=BG if accent else INK,
                         activebackground=PINK, activeforeground=BG,
                         disabledforeground=MUTED, relief="flat", bd=0,
                         highlightthickness=1, highlightbackground=BLUE,
                         highlightcolor=CYAN, font=FONT, padx=8, pady=5,
                         cursor="hand2", takefocus=True)

    def draw_banner(self, event):
        canvas = self.banner
        canvas.delete("all")
        w, h = event.width, event.height
        for x in range(0, w, 26):
            canvas.create_line(x, 0, x, h, fill="#14223b")
        for y in range(0, h, 26):
            canvas.create_line(0, y, w, y, fill="#14223b")
        for i in range(9):
            x = w - 130 + i * 13
            canvas.create_line(x, 0, x - 35, h, fill=BLUE, width=3)
        canvas.create_polygon(12, 14, 34, 7, 375, 7, 355, 18, fill=BLUE)
        canvas.create_text(27, 48, text="ZER0 // MATH", anchor="w",
                           font=("DejaVu Sans", 30, "bold italic"), fill=PINK)
        canvas.create_text(24, 45, text="ZER0 // MATH", anchor="w",
                           font=("DejaVu Sans", 30, "bold italic"), fill=CYAN)
        canvas.create_line(24, 71, 289, 68, 318, 75, fill=PINK, width=4)
        canvas.create_text(26, 92, text="TRUTH GUIDES  /  INQUIRE EVOLVES",
                           anchor="w", font=FONT, fill=INK)
        canvas.create_text(w - 20, 111, text="LOCAL CAS  //  0x01",
                           anchor="e", font=FONT, fill=CYAN)

    def build(self):
        self.banner = tk.Canvas(self.root, height=125, bg=BG, highlightthickness=0)
        self.banner.pack(fill="x")
        self.banner.bind("<Configure>", self.draw_banner)
        body = tk.Frame(self.root, bg=BG, padx=12, pady=8)
        body.pack(fill="both", expand=True)
        body.columnconfigure(0, weight=3)
        body.columnconfigure(1, weight=1, minsize=218)
        body.rowconfigure(0, weight=1)
        main = tk.Frame(body, bg=PANEL, padx=12, pady=10)
        main.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        side = tk.Frame(body, bg=PANEL, padx=10, pady=10)
        side.grid(row=0, column=1, sticky="nsew")

        self.label(main, "01 // EXPRESSION INPUT", CYAN).pack(fill="x")
        self.entry = tk.Entry(main, textvariable=self.expression, bg=FIELD,
                              fg=INK, insertbackground=CYAN, relief="flat",
                              font=("DejaVu Sans Mono", 16), highlightthickness=1,
                              highlightbackground=BLUE, highlightcolor=CYAN)
        self.entry.pack(fill="x", ipady=9, pady=(5, 8))
        controls = tk.Frame(main, bg=PANEL)
        controls.pack(fill="x")
        self.solve_button = self.button(controls, "EXECUTE [ENTER]", self.solve, True)
        self.solve_button.pack(side="left", fill="x", expand=True, padx=(0, 4))
        self.button(controls, "CLEAR", self.clear).pack(side="left", padx=4)
        self.button(controls, "COPY", self.copy).pack(side="left", padx=(4, 0))

        self.label(main, "02 // RESULT OUTPUT", PINK).pack(fill="x", pady=(10, 4))
        output_frame = tk.Frame(main, bg=FIELD)
        output_frame.pack(fill="both", expand=True)
        self.output = tk.Text(output_frame, height=5, wrap="word", state="disabled",
                              bg=FIELD, fg=CYAN, font=("DejaVu Sans Mono", 14),
                              relief="flat", padx=8, pady=8)
        scrollbar = tk.Scrollbar(output_frame, command=self.output.yview)
        self.output.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.output.pack(side="left", fill="both", expand=True)
        self.show_output("Awaiting mathematical input.")

        self.label(main, "03 // SYMBOL DECK", CYAN).pack(fill="x", pady=(10, 4))
        deck = tk.Frame(main, bg=PANEL)
        deck.pack(fill="x")
        for col in range(6):
            deck.columnconfigure(col, weight=1, uniform="keys")
        for row, keys in enumerate(KEYS):
            for col, key in enumerate(keys):
                self.button(deck, key, lambda value=key: self.insert(value)).grid(
                    row=row, column=col, sticky="nsew", padx=2, pady=2)

        self.label(side, "04 // MATH MODULES", CYAN).pack(fill="x")
        examples = tk.Frame(side, bg=PANEL)
        examples.pack(fill="x", pady=(4, 8))
        for name, sample in EXAMPLES:
            self.button(examples, name, lambda value=sample: self.load(value)).pack(
                fill="x", pady=1)
        self.label(side, "05 // SESSION HISTORY", PINK).pack(fill="x")
        self.history_box = tk.Listbox(side, bg=FIELD, fg=INK, font=FONT,
                                      height=5, relief="flat", exportselection=False,
                                      selectbackground=BLUE, selectforeground=INK)
        self.history_box.pack(fill="both", expand=True, pady=(4, 0))
        self.history_box.bind("<Double-Button-1>", self.recall)
        self.history_box.bind("<Return>", self.recall)
        self.button(side, "CLEAR HISTORY", self.clear_history).pack(fill="x", pady=(4, 0))
        footer = tk.Label(self.root, textvariable=self.status, bg=FIELD, fg=CYAN,
                          anchor="w", font=FONT, padx=12, pady=6)
        footer.pack(fill="x")
        self.entry.focus_set()

    def insert(self, value):
        if self.entry.selection_present():
            self.entry.delete("sel.first", "sel.last")
        self.entry.insert("insert", value)
        self.entry.focus_set()

    def load(self, value):
        self.expression.set(value)
        self.entry.icursor("end")
        self.entry.focus_set()

    def show_output(self, text, ok=True):
        self.output.configure(state="normal", fg=CYAN if ok else ERROR)
        self.output.delete("1.0", "end")
        self.output.insert("1.0", text)
        self.output.configure(state="disabled")

    def solve(self, event=None):
        if self.busy:
            return "break"
        expression = self.expression.get()
        if not expression.strip():
            self.status.set("INPUT REQUIRED")
            return "break"
        self.busy = True
        self.solve_button.configure(state="disabled")
        self.status.set("COMPUTING // SYMBOLIC ENGINE")
        self.show_output("Processing...")
        threading.Thread(target=self.worker, args=(expression,), daemon=True).start()
        return "break"

    def worker(self, expression):
        try:
            ok, output = compute(expression)
        except Exception as exc:
            ok, output = False, str(exc)
        self.results.put((expression, ok, output))

    def poll(self):
        try:
            expression, ok, output = self.results.get_nowait()
        except Empty:
            pass
        else:
            self.show_output(output, ok)
            self.history.insert(0, (expression, output, ok))
            self.history_box.insert(0, expression)
            if len(self.history) > 100:
                self.history.pop()
                self.history_box.delete(100)
            self.busy = False
            self.solve_button.configure(state="normal")
            self.status.set("COMPLETE // CHECK DOMAIN ASSUMPTIONS" if ok else "ERROR // CHECK INPUT")
        self.root.after(60, self.poll)

    def recall(self, event=None):
        selection = self.history_box.curselection()
        if selection and not self.busy:
            expression, output, ok = self.history[selection[0]]
            self.load(expression)
            self.show_output(output, ok)
            self.status.set("HISTORY // RECALLED")
        return "break"

    def clear_history(self):
        self.history.clear()
        self.history_box.delete(0, "end")

    def clear(self, event=None):
        self.load("")
        if not self.busy:
            self.show_output("Awaiting mathematical input.")
            self.status.set("READY // LOCAL ENGINE")
        return "break"

    def copy(self):
        text = self.output.get("1.0", "end-1c")
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.status.set("OUTPUT COPIED")


def main():
    root = tk.Tk()
    Zer0Calculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
