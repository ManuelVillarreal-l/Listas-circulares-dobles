"""Spanish-language desktop interface for the card table."""
import tkinter as tk
from tkinter import ttk, messagebox
from .structure import GameTable

BACKGROUND = "#101827"
PANEL = "#182438"
GOLD = "#d9a441"
TEXT = "#f3f4f6"
MUTED = "#aab7ca"

class CardTableApp:
    def __init__(self, root):
        self.root = root
        self.table = GameTable()
        root.title("Mesa Arcana | Turnos de cartas")
        root.geometry("1020x700")
        root.minsize(850, 620)
        root.configure(bg=BACKGROUND)
        self.configure_styles()
        self.build_layout()
        self.refresh_view()

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=BACKGROUND)
        style.configure("Panel.TFrame", background=PANEL)
        style.configure("TLabel", background=BACKGROUND, foreground=TEXT, font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 25, "bold"), foreground=GOLD)
        style.configure("Muted.TLabel", foreground=MUTED, font=("Segoe UI", 10))
        style.configure("Panel.TLabel", background=PANEL, foreground=TEXT)
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=8)
        style.configure("Gold.TButton", background=GOLD, foreground="#171717")
        style.map("Gold.TButton", background=[("active", "#f1c66e")])
        style.configure("Treeview", background="#111c2d", foreground=TEXT, fieldbackground="#111c2d", rowheight=30)
        style.configure("Treeview.Heading", background="#26364d", foreground=TEXT, font=("Segoe UI", 10, "bold"))

    def build_layout(self):
        container = ttk.Frame(self.root, padding=22)
        container.pack(fill="both", expand=True)
        header = ttk.Frame(container)
        header.pack(fill="x", pady=(0, 16))
        ttk.Label(header, text="♠  MESA ARCANA", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="Laboratorio de turnos · Lista circular doblemente enlazada", style="Muted.TLabel").pack(anchor="w", pady=(3, 0))
        body = ttk.Frame(container)
        body.pack(fill="both", expand=True)
        controls = ttk.Frame(body, style="Panel.TFrame", padding=16)
        controls.pack(side="left", fill="y", padx=(0, 14))
        ttk.Label(controls, text="CONTROL DE MESA", style="Panel.TLabel", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 12))
        ttk.Label(controls, text="Nombre del jugador", style="Panel.TLabel").pack(anchor="w")
        self.name_var = tk.StringVar()
        ttk.Entry(controls, textvariable=self.name_var, width=27).pack(fill="x", pady=(4, 10))
        ttk.Label(controls, text="Carta favorita / alias", style="Panel.TLabel").pack(anchor="w")
        self.card_var = tk.StringVar()
        ttk.Entry(controls, textvariable=self.card_var, width=27).pack(fill="x", pady=(4, 10))
        ttk.Button(controls, text="＋  Insertar al inicio", style="Gold.TButton", command=self.insert_start).pack(fill="x", pady=3)
        ttk.Button(controls, text="＋  Insertar al final", command=self.insert_end).pack(fill="x", pady=3)
        ttk.Label(controls, text="Posición (desde 1)", style="Panel.TLabel").pack(anchor="w", pady=(10, 0))
        self.position_var = tk.StringVar(value="2")
        ttk.Entry(controls, textvariable=self.position_var, width=8).pack(anchor="w", pady=(4, 4))
        ttk.Button(controls, text="Insertar en posición", command=self.insert_position).pack(fill="x", pady=3)
        ttk.Button(controls, text="⌕  Buscar jugador", command=self.search_player).pack(fill="x", pady=3)
        ttk.Button(controls, text="✕  Eliminar seleccionado", command=self.delete_player).pack(fill="x", pady=3)
        ttk.Separator(controls).pack(fill="x", pady=13)
        ttk.Label(controls, text="MOVIMIENTO DE TURNOS", style="Panel.TLabel", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 7))
        ttk.Button(controls, text="← Reversa", command=self.reverse_turn).pack(fill="x", pady=3)
        ttk.Button(controls, text="Avanzar →", style="Gold.TButton", command=self.advance_turn).pack(fill="x", pady=3)
        ttk.Label(controls, text="Saltos (+ derecha / − izquierda)", style="Panel.TLabel", wraplength=225).pack(anchor="w", pady=(9, 0))
        self.skip_var = tk.StringVar(value="2")
        ttk.Entry(controls, textvariable=self.skip_var).pack(fill="x", pady=4)
        ttk.Button(controls, text="⤼  Saltar turnos", command=self.skip_turns).pack(fill="x", pady=3)

        right = ttk.Frame(body)
        right.pack(side="left", fill="both", expand=True)
        status_card = ttk.Frame(right, style="Panel.TFrame", padding=16)
        status_card.pack(fill="x", pady=(0, 12))
        ttk.Label(status_card, text="JUGADOR EN TURNO", style="Panel.TLabel").pack(anchor="w")
        self.current_label = ttk.Label(status_card, text="Sin jugadores", style="Panel.TLabel", font=("Segoe UI", 22, "bold"), foreground=GOLD)
        self.current_label.pack(anchor="w", pady=5)
        self.status_var = tk.StringVar()
        ttk.Label(status_card, textvariable=self.status_var, style="Panel.TLabel").pack(anchor="w")
        ttk.Label(right, text="ASIENTOS EN LA MESA · recorrido desde el turno actual", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(2, 8))
        self.player_grid = ttk.Treeview(right, columns=("order", "name", "card", "status"), show="headings", height=11)
        for column, heading, width in [("order", "#", 48), ("name", "Jugador", 190), ("card", "Carta favorita / alias", 210), ("status", "Estado", 120)]:
            self.player_grid.heading(column, text=heading)
            self.player_grid.column(column, width=width, anchor="center" if column in ("order", "status") else "w")
        self.player_grid.pack(fill="both", expand=True)
        self.player_grid.bind("<<TreeviewSelect>>", self.on_player_selected)
        footer = ttk.Frame(right, style="Panel.TFrame", padding=12)
        footer.pack(fill="x", pady=(12, 0))
        self.directions_label = ttk.Label(footer, text="", style="Panel.TLabel", wraplength=560, justify="left")
        self.directions_label.pack(anchor="w")
        ttk.Label(container, text="Mesa Arcana · Proyecto académico · Python + Tkinter · Sin dependencias externas", style="Muted.TLabel").pack(anchor="w", pady=(14, 0))

    def form_data(self):
        return self.name_var.get().strip(), self.card_var.get().strip() or "Sin preferencia"

    def perform_action(self, action):
        try:
            action()
            self.name_var.set("")
            self.card_var.set("")
            self.refresh_view()
        except (ValueError, KeyError) as error:
            messagebox.showwarning("No se pudo completar", str(error))

    def insert_start(self):
        name, card = self.form_data()
        self.perform_action(lambda: self.table.insert_at_start(name, card))

    def insert_end(self):
        name, card = self.form_data()
        self.perform_action(lambda: self.table.insert_at_end(name, card))

    def insert_position(self):
        name, card = self.form_data()
        try:
            position = int(self.position_var.get())
        except ValueError:
            messagebox.showwarning("Posición inválida", "La posición debe ser un número entero.")
            return
        self.perform_action(lambda: self.table.insert_at_position(position, name, card))

    def search_player(self):
        player = self.table.find_player(self.name_var.get().strip())
        if player:
            messagebox.showinfo("Jugador encontrado", f"{player.name}\nCarta favorita / alias: {player.favorite_card}")
            for item in self.player_grid.get_children():
                if self.player_grid.item(item, "values")[1].casefold() == player.name.casefold():
                    self.player_grid.selection_set(item)
                    self.player_grid.see(item)
                    break
        else:
            messagebox.showinfo("Búsqueda", "No se encontró ese jugador en la mesa.")

    def selected_name(self):
        selection = self.player_grid.selection()
        return self.player_grid.item(selection[0], "values")[1] if selection else None

    def delete_player(self):
        name = self.selected_name() or self.name_var.get().strip()
        if not name:
            messagebox.showinfo("Selecciona un jugador", "Selecciona una fila o escribe el nombre del jugador.")
            return
        self.perform_action(lambda: self.table.remove_player(name))

    def advance_turn(self):
        self.perform_action(self.table.next_turn)

    def reverse_turn(self):
        self.perform_action(self.table.previous_turn)

    def skip_turns(self):
        try:
            steps = int(self.skip_var.get())
        except ValueError:
            messagebox.showwarning("Salto inválido", "Escribe un entero: positivo para derecha y negativo para izquierda.")
            return
        self.perform_action(lambda: self.table.skip_turns(steps))

    def on_player_selected(self, _event=None):
        selected = self.selected_name()
        if selected:
            self.name_var.set(selected)

    def refresh_view(self):
        for item in self.player_grid.get_children():
            self.player_grid.delete(item)
        names = self.table.traverse_right()
        for index, name in enumerate(names, 1):
            player = self.table.find_player(name)
            status = "▶ EN TURNO" if player is self.table.current_player else "En espera"
            self.player_grid.insert("", "end", values=(index, name, player.favorite_card, status))
        if self.table.current_player:
            self.current_label.configure(text=f"♛  {self.table.current_player.name}")
            self.status_var.set(f"{self.table.player_count} jugador(es) conectados · Círculo validado ✓")
            self.directions_label.configure(text=f"↻ DERECHA: {'  →  '.join(self.table.traverse_right())}\n↺ IZQUIERDA: {'  ←  '.join(self.table.traverse_left())}")
        else:
            self.current_label.configure(text="Sin jugadores")
            self.status_var.set("0 jugadores · Agrega participantes para comenzar")
            self.directions_label.configure(text="Los enlaces se crean automáticamente al agregar el primer jugador.")

def launch_app():
    root = tk.Tk()
    CardTableApp(root)
    root.mainloop()
