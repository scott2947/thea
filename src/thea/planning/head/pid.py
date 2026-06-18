from dataclasses import dataclass, field


@dataclass
class PIDController:
    kp: float
    ki: float
    kd: float
    integral_limit: float = 1.0

    _integral: float = field(default=0.0, init=False)
    _last_error: float = field(default=0.0, init=False)
    _last_ts: float | None = field(default=None, init=False)

    def update(self, error: float, timestamp: float) -> float:
        if self._last_ts is None:
            self._last_ts = timestamp
            self._last_error = error
            return self.kp * error

        dt = timestamp - self._last_ts
        if dt <= 0:
            return 0.0

        self._integral += error * dt
        self._integral = max(-self.integral_limit, min(self.integral_limit, self._integral))

        derivative = (error - self._last_error) / dt

        self._last_error = error
        self._last_ts = timestamp

        return self.kp * error + self.ki * self._integral + self.kd * derivative
    
    def reset(self):
        self._integral = 0.0
        self._last_ts = None
        self._last_error = 0.0
