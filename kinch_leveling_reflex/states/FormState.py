import reflex as rx
from kinch_leveling_reflex.api.api import get_categories, get_times, update_time
from kinch_leveling_reflex.utils import format_time, unformat_time
from kinch_leveling_reflex.states.AuthState import AuthState

class FormState(rx.State):
    categories: list[str]
    category: str
    actual_time: str
    goal_time: str
    proportion: str
    original_proportion: str
    wca_id: str
    
    prop_map = {
      0: "Nula",
      1.00025: "Baja",
      1.0005: "Media",
      1.00075: "Alta",
    }
    
    positive_points = [0, 1, 2, 3]
    negative_points = [0, -3, -2, -1]
    
    async def fetch_categories(self):
      data = await get_categories()
      self.categories = [category.name for category in data]
      
    @rx.event
    async def get_category_times(self, category: str):
      auth_state = await self.get_state(AuthState)
      self.wca_id = auth_state.wca_id

      self.category = category
      data = await get_times(self.wca_id)
      for time in data:
        if time.category == category:
          self.actual_time = format_time(time.actual_time)
          self.goal_time = format_time(time.goal_time)
          self.proportion = self.prop_map[time.proportion]
          self.original_proportion = self.prop_map[time.proportion]
          break
        
    @rx.event
    async def update_category_time(self, kaizen: dict[str, str], xps: dict[str, int]):
      kaizen_time = unformat_time(kaizen[self.category])
      xp = xps[self.category]
      actual_time = unformat_time(self.actual_time)
      goal_time = unformat_time(self.goal_time)
      proportion_value = None
      proportion_index = 0  # Valor por defecto
      for i, (key, value) in enumerate(self.prop_map.items()):
          if value == self.proportion:
              proportion_value = key
          if value == self.original_proportion:
              proportion_index = i     
      xp += self.positive_points[proportion_index] if actual_time <= kaizen_time else self.negative_points[proportion_index]
      xp = xp if xp >= 0 else 0
            
      await update_time(self.category, actual_time, goal_time, proportion_value, xp)
      
      self.actual_time = ""
      self.goal_time = ""
      self.proportion = ""