import tkinter as tk
from tkinter import ttk, messagebox

ITEMS = [
    ("Notebook", 2.50),
    ("Ballpoint Pen", 0.80),
    ("Pencil Box", 3.20),
    ("Highlighter", 1.40),
    ("Stapler", 4.75),
    ("Sticky Notes", 1.90),
    ("Geometry Set", 5.30),
]

USD_TO_INR = 83.0
WIDTH = 760
HEIGHT = 620


class StationeryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stationery Order Management App")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.resizable(False, False)

        self.currency = tk.StringVar(value="USD")
        self.qty_vars = []
        self.price_labels = []
        self.subtotal_labels = []

        self.setup_style()
        self.setup_canvas()
        self.build_interface()
        self.refresh_prices()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Card.TFrame", background="#fdfaf3")
        style.configure("Head.TLabel", background="#fdfaf3", font=("Segoe UI", 10, "bold"), foreground="#2d3a4f")
        style.configure("Cell.TLabel", background="#fdfaf3", font=("Segoe UI", 10), foreground="#333333")
        style.configure("Title.TLabel", background="#fdfaf3", font=("Segoe UI", 16, "bold"), foreground="#1f4e79")
        style.configure("Total.TLabel", background="#fdfaf3", font=("Segoe UI", 12, "bold"), foreground="#1b6e3c")
        style.configure("Card.TRadiobutton", background="#fdfaf3", font=("Segoe UI", 10))
        style.configure("Order.TButton", font=("Segoe UI", 10, "bold"), padding=6)

    def setup_canvas(self):
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        try:
            self.bg_image = tk.PhotoImage(file="background.png")
            self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        except tk.TclError:
            steps = 40
            for i in range(steps):
                shade = 70 + int(i * 3)
                color = f"#{40:02x}{shade:02x}{min(255, shade + 60):02x}"
                y1 = i * HEIGHT // steps
                y2 = (i + 1) * HEIGHT // steps
                self.canvas.create_rectangle(0, y1, WIDTH, y2, fill=color, outline=color)

    def build_interface(self):
        card = ttk.Frame(self.canvas, style="Card.TFrame", padding=18)
        self.canvas.create_window(WIDTH // 2, HEIGHT // 2, window=card, anchor="center")

        ttk.Label(card, text="Stationery Order Form", style="Title.TLabel").grid(
            row=0, column=0, columnspan=4, pady=(0, 10)
        )

        ttk.Label(card, text="Currency:", style="Head.TLabel").grid(row=1, column=0, sticky="w")
        picker = ttk.Frame(card, style="Card.TFrame")
        picker.grid(row=1, column=1, columnspan=3, sticky="w", pady=(0, 10))
        for label in ("USD", "INR"):
            ttk.Radiobutton(
                picker,
                text=label,
                value=label,
                variable=self.currency,
                style="Card.TRadiobutton",
                command=self.refresh_prices,
            ).pack(side="left", padx=(0, 12))

        for col, heading in enumerate(("Item", "Price", "Quantity", "Subtotal")):
            ttk.Label(card, text=heading, style="Head.TLabel").grid(row=2, column=col, padx=8, pady=4, sticky="w")

        for index, (name, price) in enumerate(ITEMS):
            row = index + 3

            ttk.Label(card, text=name, style="Cell.TLabel").grid(row=row, column=0, padx=8, pady=3, sticky="w")

            price_label = ttk.Label(card, text="", style="Cell.TLabel")
            price_label.grid(row=row, column=1, padx=8, pady=3, sticky="w")
            self.price_labels.append(price_label)

            qty_var = tk.StringVar(value="0")
            qty_var.trace_add("write", lambda *args: self.update_totals())
            ttk.Entry(card, textvariable=qty_var, width=8, justify="center").grid(row=row, column=2, padx=8, pady=3)
            self.qty_vars.append(qty_var)

            subtotal_label = ttk.Label(card, text="", style="Cell.TLabel")
            subtotal_label.grid(row=row, column=3, padx=8, pady=3, sticky="w")
            self.subtotal_labels.append(subtotal_label)

        last_row = len(ITEMS) + 3

        ttk.Separator(card, orient="horizontal").grid(row=last_row, column=0, columnspan=4, sticky="ew", pady=10)

        self.total_label = ttk.Label(card, text="", style="Total.TLabel")
        self.total_label.grid(row=last_row + 1, column=0, columnspan=3, sticky="w", padx=8)

        ttk.Button(card, text="Place Order", style="Order.TButton", command=self.place_order).grid(
            row=last_row + 1, column=3, sticky="e", padx=8
        )

        self.status_label = ttk.Label(card, text="", style="Cell.TLabel", foreground="#b00020")
        self.status_label.grid(row=last_row + 2, column=0, columnspan=4, sticky="w", padx=8, pady=(8, 0))

    def convert(self, usd_amount):
        return usd_amount if self.currency.get() == "USD" else usd_amount * USD_TO_INR

    def symbol(self):
        return "$" if self.currency.get() == "USD" else "₹"

    def refresh_prices(self):
        for index, (name, price) in enumerate(ITEMS):
            self.price_labels[index].config(text=f"{self.symbol()}{self.convert(price):.2f}")
        self.update_totals()

    def update_totals(self):
        total = 0.0
        bad_rows = []

        for index, (name, price) in enumerate(ITEMS):
            raw = self.qty_vars[index].get().strip()

            if raw == "":
                qty = 0
            elif raw.isdigit():
                qty = int(raw)
            else:
                qty = 0
                bad_rows.append(name)

            line_total = self.convert(price) * qty
            total += line_total
            self.subtotal_labels[index].config(text=f"{self.symbol()}{line_total:.2f}")

        self.total_label.config(text=f"Total: {self.symbol()}{total:.2f}")
        self.status_label.config(
            text=f"Please enter whole numbers only for: {', '.join(bad_rows)}" if bad_rows else ""
        )
        return total, bad_rows

    def place_order(self):
        total, bad_rows = self.update_totals()

        if bad_rows:
            messagebox.showerror("Invalid quantity", "Quantities must be whole numbers (0, 1, 2...).")
            return

        if total == 0:
            messagebox.showinfo("Empty order", "Add at least one item before placing your order.")
            return

        lines = []
        for index, (name, price) in enumerate(ITEMS):
            raw = self.qty_vars[index].get().strip()
            qty = int(raw) if raw.isdigit() else 0
            if qty > 0:
                lines.append(f"{name} x {qty}")

        summary = "\n".join(lines)
        messagebox.showinfo("Order placed", f"{summary}\n\nTotal: {self.symbol()}{total:.2f}")

        for var in self.qty_vars:
            var.set("0")


if __name__ == "__main__":
    window = tk.Tk()
    StationeryApp(window)
    window.mainloop()