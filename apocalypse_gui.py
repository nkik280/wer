import tkinter as tk
from tkinter import ttk, messagebox
from apocalypse_simulation import World, SCENARIOS, ACTIONS

class ApocalypseApp:
    def __init__(self, master):
        self.master = master
        master.title("Apocalypse Simulator")

        self.scenario_var = tk.StringVar(value='1')
        self.world = None
        self.scenario = None
        self.day = 0

        self.create_widgets()

    def create_widgets(self):
        selection_frame = ttk.Frame(self.master)
        selection_frame.pack(padx=10, pady=10)

        ttk.Label(selection_frame, text="Выберите сценарий:").pack(side=tk.LEFT)
        self.scenario_menu = ttk.Combobox(selection_frame, textvariable=self.scenario_var,
                                           values=list(SCENARIOS.keys()), width=5)
        self.scenario_menu.pack(side=tk.LEFT, padx=5)

        self.start_button = ttk.Button(selection_frame, text="Начать", command=self.start)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.info_text = tk.Text(self.master, width=50, height=10, state=tk.DISABLED)
        self.info_text.pack(padx=10, pady=10)

        bars_frame = ttk.Frame(self.master)
        bars_frame.pack(padx=10, pady=5)
        ttk.Label(bars_frame, text="Население").pack()
        self.population_bar = ttk.Progressbar(bars_frame, length=300, maximum=1000000)
        self.population_bar.pack()
        ttk.Label(bars_frame, text="Ресурсы").pack(pady=(5,0))
        self.resources_bar = ttk.Progressbar(bars_frame, length=300, maximum=1000)
        self.resources_bar.pack()

        self.actions_frame = ttk.Frame(self.master)
        self.actions_frame.pack(padx=10, pady=10)

    def log(self, message):
        self.info_text.configure(state=tk.NORMAL)
        self.info_text.insert(tk.END, message + "\n")
        self.info_text.configure(state=tk.DISABLED)
        self.info_text.see(tk.END)

    def start(self):
        key = self.scenario_var.get()
        self.scenario = SCENARIOS.get(key)
        if not self.scenario:
            messagebox.showerror("Ошибка", "Неизвестный сценарий")
            return
        self.world = World()
        self.day = 0
        self.info_text.configure(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.configure(state=tk.DISABLED)
        self.log(f"Сценарий: {self.scenario.name}")
        self.log(self.scenario.description)
        self.update_bars()
        for widget in self.actions_frame.winfo_children():
            widget.destroy()
        actions = ACTIONS.get(self.scenario.name, {})
        for key, (action, desc) in actions.items():
            ttk.Button(self.actions_frame, text=desc,
                       command=lambda a=action: self.step(a)).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.actions_frame, text="Пропустить", command=lambda: self.step(None)).pack(side=tk.LEFT, padx=2)
        self.step(None)

    def update_bars(self):
        if not self.world:
            return
        self.population_bar['value'] = self.world.population
        self.resources_bar['value'] = max(0, self.world.resources)

    def step(self, action):
        if not self.world:
            return
        self.day += 1
        self.log(f"\nДень {self.day}")
        self.scenario.step(self.world, action)
        self.log(str(self.world))
        self.update_bars()
        if self.world.population == 0 or self.day >= 10:
            self.log("Симуляция завершена")
            for widget in self.actions_frame.winfo_children():
                widget.configure(state=tk.DISABLED)


def main():
    root = tk.Tk()
    app = ApocalypseApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
