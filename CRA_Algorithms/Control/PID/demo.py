import matplotlib.pyplot as plt
from pid import PID

dt = 0.01
simulation_time = 10.0
target = 1.0

a = 1.0
b = 1.0
x = 0.0

pid = PID(
    kp=4.0,
    ki=1.5,
    kd=0.5,
    dt=dt,
    output_limits=(-10, 10),
    integral_limits=(-5, 5),
)

time_history = []
state_history = []
control_history = []

steps = int(simulation_time / dt)

for i in range(steps):
    t = i * dt
    u = pid.update(
        setpoint=target,
        measurement=x,
    )
    dx = -a * x + b * u
    x += dx * dt
    time_history.append(t)
    state_history.append(x)
    control_history.append(u)

plt.plot(
    time_history,
    state_history,
    label="System Output",
)

plt.axhline(
    target,
    linestyle="--",
    label="Target",
)

plt.xlabel("Time (s)")
plt.ylabel("State")
plt.title("PID Control")
plt.grid()
plt.legend()
plt.show()