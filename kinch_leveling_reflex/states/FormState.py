import reflex as rx
from kinch_leveling_reflex.api.api import get_categories

class FormState(rx.State):
    categories: list[str]
    
    async def fetch_categories(self):
      data = await get_categories()
      self.categories = [category.name for category in data]