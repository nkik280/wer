import random

class World:
    def __init__(self, population=1000000, resources=1000):
        self.population = population
        self.resources = resources

    def __str__(self):
        return f"Population: {self.population}, Resources: {self.resources}"

class ApocalypseScenario:
    name = ""
    description = ""

    def step(self, world, action=None):
        pass

class Pandemic(ApocalypseScenario):
    name = "Пандемия"
    description = "Смертельный вирус распространяется по планете."

    def step(self, world, action=None):
        loss = random.randint(5000, 15000)
        if action == 'quarantine':
            loss = int(loss * 0.7)
        if action == 'search_cure':
            world.resources -= 50
            loss = int(loss * 0.9)
        world.population = max(0, world.population - loss)

class NuclearWar(ApocalypseScenario):
    name = "Ядерная война"
    description = "Разразилась глобальная ядерная война."

    def step(self, world, action=None):
        loss = random.randint(20000, 50000)
        if action == 'defend':
            loss = int(loss * 0.8)
        world.population = max(0, world.population - loss)
        world.resources -= 100

class ZombieOutbreak(ApocalypseScenario):
    name = "Зомби-апокалипсис"
    description = "Орды зомби заполонили мир."

    def step(self, world, action=None):
        loss = random.randint(8000, 20000)
        if action == 'barricade':
            loss = int(loss * 0.5)
        world.population = max(0, world.population - loss)
        if random.random() < 0.3:
            world.resources -= 20

class AlienInvasion(ApocalypseScenario):
    name = "Нашествие инопланетян"
    description = "Враждебные инопланетяне атакуют Землю."

    def step(self, world, action=None):
        loss = random.randint(10000, 25000)
        if action == 'defend':
            loss = int(loss * 0.7)
        world.population = max(0, world.population - loss)
        world.resources -= 70

SCENARIOS = {
    '1': Pandemic(),
    '2': NuclearWar(),
    '3': ZombieOutbreak(),
    '4': AlienInvasion()
}

ACTIONS = {
    'Пандемия': {
        '1': ('quarantine', 'Ввести карантин'),
        '2': ('search_cure', 'Искать лекарство'),
        '0': (None, 'Ничего не делать')
    },
    'Ядерная война': {
        '1': ('defend', 'Организовать оборону'),
        '0': (None, 'Ничего не делать')
    },
    'Зомби-апокалипсис': {
        '1': ('barricade', 'Баррикадироваться'),
        '0': (None, 'Ничего не делать')
    },
    'Нашествие инопланетян': {
        '1': ('defend', 'Организовать оборону'),
        '0': (None, 'Ничего не делать')
    }
}

def main():
    print("Выберите сценарий апокалипсиса:")
    print("1. Пандемия")
    print("2. Ядерная война")
    print("3. Зомби-апокалипсис")
    print("4. Нашествие инопланетян")
    choice = input("Введите номер сценария: ")
    scenario = SCENARIOS.get(choice)
    if not scenario:
        print("Неизвестный сценарий.")
        return

    world = World()
    print(f"\nСценарий: {scenario.name}")
    print(scenario.description)
    steps = 10
    for day in range(1, steps + 1):
        print(f"\nДень {day}")
        print(world)
        actions = ACTIONS.get(scenario.name, {})
        if actions:
            print("Выберите действие:")
            for key, (_, desc) in actions.items():
                print(f"{key}. {desc}")
            action_key = input("Ваш выбор: ")
            action, _ = actions.get(action_key, (None, None))
        else:
            action = None
        scenario.step(world, action)
        if world.population == 0:
            print("Все люди погибли...")
            break
    print("\nИтог:")
    print(world)

if __name__ == "__main__":
    main()
