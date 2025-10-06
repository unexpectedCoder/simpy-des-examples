import random as rand
import simpy as sim


def loot_generation(env: sim.Environment, loot: list):
    """Процесс случайной генерации предметов.
    """
    possible_loot = "apple", "zebra", "dog", "cat", "sock"
    while True:
        yield env.timeout(rand.expovariate(1/5))
        item = rand.choice(possible_loot)
        print(f"{env.now:.3f}: сгенерирован предмет '{item}'")
        loot.append(item)


def loot_checking(env: sim.Environment, loot: list):
    """Процесс мониторинга числа предметов в коллекции.
    """
    while True:
        yield env.timeout(10)
        print(f"{env.now:.3f}: число предметов = {len(loot)}")


# Инициализация среды дискретно-событийного моделирования
env = sim.Environment()
# Начальная коллекция
loot = []
# Инициализация (регистрация) процессов
env.process(loot_generation(env, loot))
env.process(loot_checking(env, loot))
# Запуск моделирования до достижения заданного времени
env.run(until=100)
