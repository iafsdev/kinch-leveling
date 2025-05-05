import reflex as rx

class Category(rx.Base):
  name: str
  type: str
    
class Time(rx.Base):
  category: str
  actual_time: float
  goal_time: float
  proportion: float
  
class Row(rx.Base):
  category: str
  pr_kinch: float
  nr_kinch: float
  wr_kinch: float
  kaizen: float
  