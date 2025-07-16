import reflex as rx
from kinch_leveling_reflex.api.api import get_categories, get_times, update_time
from kinch_leveling_reflex.utils import format_time, unformat_time

class FormState(rx.State):
    categories: list[str]
    category: str
    actual_time: str
    goal_time: str
    proportion: str
    
    prop_map = {
      0: "Nula",
      1.00025: "Baja",
      1.0005: "Media",
      1.00075: "Alta",
    }
    
    async def fetch_categories(self):
      data = await get_categories()
      self.categories = [category.name for category in data]
      
    @rx.event
    async def get_category_times(self, category: str):
      self.category = category
      data = await get_times()
      for time in data:
        if time.category == category:
          self.actual_time = format_time(time.actual_time)
          self.goal_time = format_time(time.goal_time)
          self.proportion = self.prop_map[time.proportion]
          print(self.proportion)
          break
        
    @rx.event
    async def update_category_time(self):
      actual_time = unformat_time(self.actual_time)
      goal_time = unformat_time(self.goal_time)
      proportion_value = None
      for key, value in self.prop_map.items():
          if value == self.proportion:
              proportion_value = key
              break
            
      await update_time(self.category, actual_time, goal_time, proportion_value)
      
      self.actual_time = ""
      self.goal_time = ""
      self.proportion = ""