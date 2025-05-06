import reflex as rx
from kinch_leveling_reflex.api.api import get_prs

class HeaderState(rx.State):
  pr_kinch: float
  nr_kinch: float
  wr_kinch: float
  
  @rx.event
  async def load_data(self):
    prs = await get_prs()
    pr_sum = 0
    nr_sum = 0
    wr_sum = 0
    for pr in prs.values():
      pr_sum += pr
      
    self.pr_kinch = round(pr_sum / len(prs), 2)
    self.nr_kinch = 0
    self.wr_kinch = 0