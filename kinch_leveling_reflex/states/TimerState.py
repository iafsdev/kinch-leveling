import reflex as rx
import asyncio
import time
from kinch_leveling_reflex.utils import format_time

class TimerState(rx.State):
    count: float = 0.0  # Tiempo en segundos con milisegundos
    is_running: bool = False
    last_time: float
    init_time: float
    toggle_guard: int = 2  # Nueva variable de control

    @rx.var
    def formatted_time(self) -> str:
        return format_time(self.count)
    
    @rx.event
    def toggle_timer(self, action: str):
        if action == 'up':
            if not self.is_running and self.toggle_guard >= 3:
                self.is_running = True
                self.last_time = time.perf_counter()
                self.count = 0.0
                self.toggle_guard = 0  # Resetea para el siguiente ciclo
        elif action == 'down':
            if self.is_running:
                self.is_running = False
                self.toggle_guard = 0  # Prepara para el siguiente ciclo
        self.toggle_guard += 1

    @rx.event(background=True)
    async def increment(self):
        print('Incrementing timer...')
        while True:
            if self.is_running:
                now = time.perf_counter()
                elapsed = now - self.last_time
                async with self:
                    self.count = elapsed
                    yield
            await asyncio.sleep(0.001)

