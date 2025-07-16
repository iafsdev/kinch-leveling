import reflex as rx

class Category(rx.Base):
  id: int
  name: str
  type: str
    
class Time(rx.Base):
  category: str
  actual_time: float
  goal_time: float
  proportion: float
  xp: int
  
class Row(rx.Base):
  category: str
  pb_kinch: float
  pr_kinch: float
  nr_kinch: float
  wr_kinch: float
  kaizen: str
  xp: int
  
class Record(rx.Base):
  id: str
  name: str
  type: str
  
class WCARecord(rx.Base):
  category: str
  average: float
  single: float
  type: str