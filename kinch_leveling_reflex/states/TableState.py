import reflex as rx
from kinch_leveling_reflex.api.api import get_categories, get_kaizen, get_prs
from kinch_leveling_reflex.serializers import Category, Row

class TableState(rx.State):
  categories: list[Category]    
  kaizen: dict[str, str]
  rows: list[Row]
  prs: dict[str, float]
  
  @rx.event
  async def load_data(self):
    self.categories = await get_categories()
    self.kaizen = await get_kaizen()
    self.prs = await get_prs()
    self.rows = []
    for category in self.categories:
      self.rows.append(Row(
        category=category.name,
        pr_kinch=self.prs[category.name],
        nr_kinch=0,
        wr_kinch=0,
        kaizen=self.kaizen[category.name],
      ))
