import numpy as np
import simpy as sim
from collections import namedtuple
from itertools import count


np.random.seed = 113


Gun = namedtuple("Gun", "name aim_time hit_prob ammo_consumption")
Target = namedtuple("Target", "name danger destroy_hits")


class Model:
    def __init__(self, env: sim.Environment, guns: list[Gun]):
        self.env = env
        # Допустим, что радар способен сопровождать максимум 10 целей
        self.targets = sim.PriorityStore(env, capacity=10)
        self.guns = sim.Store(env, capacity=len(guns))
        for gun in guns:
            self.guns.put(gun)
        # Регистрация (инициализация) процессов
        self.env.process(self.targets_appearing())
        self.env.process(self.targeting())
    
    def targets_appearing(self):
        """Генератор новых целей.
        """
        for i in count(start=1):
            yield self.env.timeout(np.random.exponential(7))
            priority = np.random.randint(0, 3)
            name = f"T-{i}"
            yield self.targets.put(sim.PriorityItem(priority, Target(
                name,
                danger=priority,
                destroy_hits=np.random.randint(1, 5)
            )))
            print(f"{self.env.now:.3f}: появилась новая цель {name}")
    
    def targeting(self):
        """Распределение целей между орудиями.
        """
        while True:
            with self.guns.get() as gun_req:
                with self.targets.get() as target_req:
                    target_gun = yield target_req & gun_req
                    (_, target), gun = tuple(target_gun.values())
                    
                    print(f"{self.env.now:.3f}: обнаружена цель {target.name}")
                    self.env.process(self.defeating(gun, target))

    def defeating(self, gun: Gun, target: Target):
        """Обстрел цели `target` орудием `gun`.
        """
        print(f"{self.env.now:.3f}: цель {target.name} распределена пушке {gun.name}")

        hits, required_hits = 0, target.destroy_hits
        ammo_consumption = 0
        t0 = self.env.now

        while hits < required_hits:
            # Время прицеливания
            yield self.env.timeout(np.random.exponential(gun.aim_time))
            # Очередь
            yield self.env.timeout(1)   # время на полёт снарядов к цели
            if np.random.random() < gun.hit_prob:   # попадание по цели
                hits += 1
                ammo_consumption += gun.ammo_consumption

        # Цель поражена — пушка свободна
        yield self.guns.put(gun)
        t1 = self.env.now
        print(
            f"{self.env.now:.3f}: цель {target.name} поражена пушкой {gun.name}:\n"
            f"\t - приоритет цели {target.danger}\n"
            f"\t - потрачено {ammo_consumption} снарядов\n"
            f"\t - затрачено времени {t1 - t0:.3f}\n"
            f"\t - {hits} попаданий по цели"
        )
    
    def run(self, until=None):
        """Запуск цикла дискретно-событийного моделирования.
        """
        self.env.run(until)


# Инициализация модели и запуск симуляции
model = Model(
    sim.Environment(),
    [Gun("G-1", 3, 0.6, 30), Gun("G-2", 3, 0.75, 20)]
)
model.run(until=50)
