import reflex as rx
from kinch_leveling_reflex.api.api import get_categories
from kinch_leveling_reflex.serializers import Category

class TableState(rx.State):
  categories: list[Category]    
  
  @rx.event
  async def fetch_categories(self):
    self.categories = await get_categories()
