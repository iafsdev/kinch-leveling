import reflex as rx
from kinch_leveling_reflex.api.api import get_pbs, get_pr_kinch, get_nr_kinch, get_wr_kinch

class HeaderState(rx.State):
  pb_kinch: float
  pr_kinch: float
  nr_kinch: float
  wr_kinch: float
  
  @rx.event
  async def load_data(self):
    pbs = await get_pbs()
    prs = await get_pr_kinch()
    nrs = await get_nr_kinch()
    wrs = await get_wr_kinch()
    
    pb_sum = 0
    pr_sum = 0
    nr_sum = 0
    wr_sum = 0
    
    for pb in pbs.values():
      pb_sum += pb
      
    for pr in prs.values():
      pr_sum += pr
      
    for nr in nrs.values():
      nr_sum += nr
      
    for wr in wrs.values():
      wr_sum += wr
    
    self.pb_kinch = round(pb_sum / len(pbs), 2)
    self.pr_kinch = round(pr_sum / len(prs), 2)
    self.nr_kinch = round(nr_sum / len(nrs), 2)
    self.wr_kinch = round(wr_sum / len(wrs), 2)