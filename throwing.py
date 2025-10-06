import numpy as np
import simpy as sim


def throwing(env: sim.Environment, n=5, mean_gen_time=1.5):
    for _ in range(n):
        yield env.timeout(np.random.exponential(mean_gen_time))
        print(f"{env.now:.3f} сек.: новый камень создан")
        env.process(flying(
            env,
            speed=np.random.randint(8, 13),
            angle=np.random.randint(20, 60)
        ))


def flying(env: sim.Environment, speed: float, angle: float):
    print(
        f"{env.now:.3f} сек.: "
        f"камень брошен под углом {angle} градусов со скоростью {speed} м/с"
    )

    vy = speed * np.sin(np.radians(angle))
    dt = 2 * vy / 9.81
    yield env.timeout(dt)

    x = speed * np.cos(np.radians(angle)) * dt
    print(f"{env.now:.3f} сек.: камень упал а землю на расстоянии {x:.3f} м")


env = sim.Environment()
env.process(throwing(env))
env.run()
