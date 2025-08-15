import reflex as rx
import asyncio
import time
from kinch_leveling_reflex.utils import format_time
from kinch_leveling_reflex.api.api import get_scramble, get_categories

class TimerState(rx.State):
    count: float = 0.0  # Tiempo en segundos con milisegundos
    is_running: bool = False
    last_time: float
    init_time: float
    toggle_guard: int = 2  # Nueva variable de control
    scramble: str
    category: str = '3x3'
    id_category: str = '333'
    svg_scramble: str

    categories_map: dict[str, str] = {
        "2x2": "222",
        "3x3": "333",
        "4x4": "444",
        "5x5": "555",
        "6x6": "666",
        "7x7": "777",
        "3BLD": "333ni",
        "Pyraminx": "pyram",
        "Skewb": "skewb",
        "Megaminx": "minx",
        "Clock": "clock",
        "4BLD": "444ni",
        "5BLD": "555ni",
        "OH": "333",
        "FMC": "333",
        "Square-1": "sq1",
        "MBLD": "333ni"
    }

    @rx.var
    def formatted_time(self) -> str:
        return format_time(self.count)
    
    @rx.var(cache=True)
    async def categories(self) -> list[str]:
        data = await get_categories()
        return [category.name for category in data]
    
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
                self.get_scramble(self.category)
        self.toggle_guard += 1
        
    @rx.event
    def get_scramble(self, category:str):
        self.category = category
        self.id_category = self.categories_map[category]
        self.scramble, self.svg_scramble = get_scramble(self.id_category)

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

