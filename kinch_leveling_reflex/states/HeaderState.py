import reflex as rx
from kinch_leveling_reflex.api.api import get_prs, get_nr_kinch, get_wr_kinch

class HeaderState(rx.State):
  pr_kinch: float
  nr_kinch: float
  wr_kinch: float
  
  @rx.event
  async def load_data(self):
    prs = await get_prs()
    nrs = await get_nr_kinch()
    wrs = await get_wr_kinch()
    
    pr_sum = 0
    nr_sum = 0
    wr_sum = 0
    
    for pr in prs.values():
      pr_sum += pr
      
    for nr in nrs.values():
      nr_sum += nr
      
    for wr in wrs.values():
      wr_sum += wr
    
    self.pr_kinch = round(pr_sum / len(prs), 2)
    self.nr_kinch = round(nr_sum / len(nrs), 2)
    self.wr_kinch = round(wr_sum / len(wrs), 2)