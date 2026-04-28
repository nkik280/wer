import random
import tkinter as tk
from tkinter import messagebox


class CitySimulator:
    """Простая симуляция развития города на примере Воронежа."""

    CELL_SIZE = 36
    GRID_ROWS = 10
    GRID_COLS = 14

    EMPTY = "empty"
    ROAD = "road"
    RESIDENTIAL = "residential"
    INDUSTRIAL = "industrial"
    PARK = "park"

    TILE_COLORS = {
        EMPTY: "#edf2f7",
        ROAD: "#4a5568",
        RESIDENTIAL: "#4299e1",
        INDUSTRIAL: "#ed8936",
        PARK: "#48bb78",
    }

    TILE_LABELS = {
        EMPTY: "Пусто",
        ROAD: "Дорога",
        RESIDENTIAL: "Жилой квартал",
        INDUSTRIAL: "Промышленность",
        PARK: "Парк",
    }

    BUILD_COST = {
        ROAD: 20,
        RESIDENTIAL: 60,
        INDUSTRIAL: 80,
        PARK: 40,
    }

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Симулятор развития Воронежа")
        self.root.geometry("1100x560")

        self.turn = 1
        self.budget = 1200
        self.population = 120000
        self.happiness = 62
        self.ecology = 58

        self.selected_tile_type = self.ROAD

        self.grid = [
            [self.EMPTY for _ in range(self.GRID_COLS)]
            for _ in range(self.GRID_ROWS)
        ]

        self.cells = {}

        self._build_ui()
        self._create_initial_voronezh_layout()
        self._refresh_metrics()

    def _build_ui(self):
        container = tk.Frame(self.root, bg="#f7fafc")
        container.pack(fill=tk.BOTH, expand=True)

        self.left_panel = tk.Frame(container, width=330, bg="#1a202c", padx=14, pady=14)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)
        self.left_panel.pack_propagate(False)

        self.right_panel = tk.Frame(container, bg="#e2e8f0", padx=14, pady=14)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self._build_control_panel()
        self._build_map_panel()

    def _build_control_panel(self):
        title = tk.Label(
            self.left_panel,
            text="Воронеж: развитие города",
            bg="#1a202c",
            fg="#f7fafc",
            font=("Arial", 16, "bold"),
            justify=tk.LEFT,
        )
        title.pack(anchor="w")

        subtitle = tk.Label(
            self.left_panel,
            text="Слева — управление и показатели\nСправа — схема города",
            bg="#1a202c",
            fg="#cbd5e0",
            font=("Arial", 10),
            justify=tk.LEFT,
        )
        subtitle.pack(anchor="w", pady=(4, 14))

        self.metrics_labels = {}
        for key in ["Ход", "Бюджет", "Население", "Счастье", "Экология"]:
            lbl = tk.Label(
                self.left_panel,
                text="",
                bg="#2d3748",
                fg="#f7fafc",
                font=("Arial", 12),
                padx=10,
                pady=8,
                anchor="w",
                justify=tk.LEFT,
            )
            lbl.pack(fill=tk.X, pady=3)
            self.metrics_labels[key] = lbl

        tk.Label(
            self.left_panel,
            text="\nВыберите строительство:",
            bg="#1a202c",
            fg="#f7fafc",
            font=("Arial", 11, "bold"),
            justify=tk.LEFT,
        ).pack(anchor="w")

        self.tile_var = tk.StringVar(value=self.ROAD)

        options = [
            (self.ROAD, "Дорога (20)") ,
            (self.RESIDENTIAL, "Жилой квартал (60)"),
            (self.INDUSTRIAL, "Промышленность (80)"),
            (self.PARK, "Парк (40)"),
        ]

        for tile_type, text in options:
            tk.Radiobutton(
                self.left_panel,
                text=text,
                variable=self.tile_var,
                value=tile_type,
                bg="#1a202c",
                fg="#e2e8f0",
                activebackground="#2d3748",
                activeforeground="#f7fafc",
                selectcolor="#2d3748",
                command=self._on_tile_selection_change,
                font=("Arial", 10),
                anchor="w",
                justify=tk.LEFT,
            ).pack(fill=tk.X, pady=2)

        tk.Button(
            self.left_panel,
            text="Следующий ход",
            bg="#3182ce",
            fg="white",
            font=("Arial", 11, "bold"),
            relief=tk.FLAT,
            padx=10,
            pady=8,
            command=self.next_turn,
        ).pack(fill=tk.X, pady=(18, 8))

        tk.Button(
            self.left_panel,
            text="Очистить выбранную клетку",
            bg="#718096",
            fg="white",
            font=("Arial", 10),
            relief=tk.FLAT,
            padx=10,
            pady=6,
            command=self.clear_selected_info,
        ).pack(fill=tk.X)

        self.info_label = tk.Label(
            self.left_panel,
            text="Нажмите на клетку справа, чтобы строить.",
            bg="#1a202c",
            fg="#cbd5e0",
            font=("Arial", 10),
            wraplength=280,
            justify=tk.LEFT,
            anchor="w",
        )
        self.info_label.pack(fill=tk.X, pady=(14, 0))

    def _build_map_panel(self):
        tk.Label(
            self.right_panel,
            text="Схема города Воронежа",
            bg="#e2e8f0",
            fg="#1a202c",
            font=("Arial", 15, "bold"),
        ).pack(anchor="w")

        legend = tk.Label(
            self.right_panel,
            text=(
                "Цвета: дорога — серый, жильё — синий, "
                "промышленность — оранжевый, парк — зелёный"
            ),
            bg="#e2e8f0",
            fg="#4a5568",
            font=("Arial", 10),
        )
        legend.pack(anchor="w", pady=(2, 10))

        map_frame = tk.Frame(self.right_panel, bg="#cbd5e0", padx=8, pady=8)
        map_frame.pack(anchor="nw")

        for row in range(self.GRID_ROWS):
            for col in range(self.GRID_COLS):
                btn = tk.Button(
                    map_frame,
                    width=4,
                    height=2,
                    bg=self.TILE_COLORS[self.EMPTY],
                    relief=tk.RAISED,
                    command=lambda r=row, c=col: self.build_on_cell(r, c),
                )
                btn.grid(row=row, column=col, padx=1, pady=1)
                self.cells[(row, col)] = btn

    def _create_initial_voronezh_layout(self):
        # Условная базовая схема: центральная магистраль и жилые районы.
        center_row = self.GRID_ROWS // 2
        center_col = self.GRID_COLS // 2

        for c in range(self.GRID_COLS):
            self.grid[center_row][c] = self.ROAD

        for r in range(self.GRID_ROWS):
            self.grid[r][center_col] = self.ROAD

        for r in range(2, 5):
            for c in range(2, 6):
                self.grid[r][c] = self.RESIDENTIAL

        for r in range(6, 9):
            for c in range(9, 12):
                self.grid[r][c] = self.INDUSTRIAL

        self.grid[1][10] = self.PARK
        self.grid[8][3] = self.PARK

        self._redraw_grid()

    def _redraw_grid(self):
        for r in range(self.GRID_ROWS):
            for c in range(self.GRID_COLS):
                tile = self.grid[r][c]
                self.cells[(r, c)].configure(bg=self.TILE_COLORS[tile])

    def _on_tile_selection_change(self):
        self.selected_tile_type = self.tile_var.get()
        cost = self.BUILD_COST[self.selected_tile_type]
        label = self.TILE_LABELS[self.selected_tile_type]
        self.info_label.config(text=f"Выбрано: {label}. Стоимость: {cost}.")

    def _refresh_metrics(self):
        self.metrics_labels["Ход"].config(text=f"Ход: {self.turn}")
        self.metrics_labels["Бюджет"].config(text=f"Бюджет: {self.budget}")
        self.metrics_labels["Население"].config(text=f"Население: {self.population}")
        self.metrics_labels["Счастье"].config(text=f"Счастье: {self.happiness}%")
        self.metrics_labels["Экология"].config(text=f"Экология: {self.ecology}%")

    def build_on_cell(self, row, col):
        chosen = self.tile_var.get()
        current = self.grid[row][col]
        cost = self.BUILD_COST[chosen]

        if current == chosen:
            self.info_label.config(text="Эта клетка уже содержит выбранный объект.")
            return

        if self.budget < cost:
            self.info_label.config(text="Недостаточно бюджета для строительства.")
            return

        self.budget -= cost
        self.grid[row][col] = chosen
        self.cells[(row, col)].configure(bg=self.TILE_COLORS[chosen])

        self._apply_build_impact(chosen)
        self._refresh_metrics()

        self.info_label.config(
            text=(
                f"Построено: {self.TILE_LABELS[chosen]} в клетке ({row + 1}, {col + 1}). "
                f"Потрачено: {cost}."
            )
        )

    def _apply_build_impact(self, tile_type):
        if tile_type == self.ROAD:
            self.happiness = min(100, self.happiness + 1)
            self.ecology = max(0, self.ecology - 1)
        elif tile_type == self.RESIDENTIAL:
            self.population += random.randint(1500, 5000)
            self.happiness = min(100, self.happiness + 2)
            self.ecology = max(0, self.ecology - 2)
        elif tile_type == self.INDUSTRIAL:
            self.budget += random.randint(30, 90)
            self.population += random.randint(500, 1800)
            self.happiness = max(0, self.happiness - 3)
            self.ecology = max(0, self.ecology - 5)
        elif tile_type == self.PARK:
            self.happiness = min(100, self.happiness + 4)
            self.ecology = min(100, self.ecology + 6)

    def next_turn(self):
        self.turn += 1

        residential_count = self._count_tiles(self.RESIDENTIAL)
        industrial_count = self._count_tiles(self.INDUSTRIAL)
        park_count = self._count_tiles(self.PARK)

        tax_income = residential_count * 25 + industrial_count * 45
        maintenance = residential_count * 12 + industrial_count * 20 + park_count * 10

        self.budget += tax_income - maintenance

        growth_factor = max(0.95, 1 + (self.happiness - 50) / 500)
        self.population = int(self.population * growth_factor)

        pollution_penalty = max(0, industrial_count * 2 - park_count)
        self.ecology = max(0, min(100, self.ecology - pollution_penalty + 1))

        if self.ecology < 25:
            self.happiness = max(0, self.happiness - 4)
        elif self.ecology > 70:
            self.happiness = min(100, self.happiness + 2)

        random_event_roll = random.random()
        event_msg = ""

        if random_event_roll < 0.08:
            self.budget += 180
            event_msg = "Город получил федеральный грант (+180 к бюджету)."
        elif random_event_roll > 0.92:
            self.budget -= 150
            self.happiness = max(0, self.happiness - 3)
            event_msg = "Авария на сети: экстренные траты (-150)."

        self._refresh_metrics()

        if self.budget < -400:
            messagebox.showwarning(
                "Финансовый кризис",
                "Бюджет сильно отрицательный. Нужны реформы и рост налоговой базы!",
            )

        if self.happiness <= 15:
            messagebox.showwarning(
                "Социальный кризис",
                "Уровень счастья жителей критически низкий.",
            )

        base_text = (
            f"Ход {self.turn}: доход {tax_income}, расходы {maintenance}. "
            f"Население: {self.population}."
        )

        self.info_label.config(text=f"{base_text} {event_msg}".strip())

    def clear_selected_info(self):
        self.info_label.config(text="Выберите тип строительства и нажмите на клетку справа.")

    def _count_tiles(self, tile_type):
        return sum(
            1
            for row in self.grid
            for tile in row
            if tile == tile_type
        )


def main():
    root = tk.Tk()
    CitySimulator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
