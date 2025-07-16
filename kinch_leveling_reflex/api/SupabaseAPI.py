import os 
from dotenv import load_dotenv
from supabase import Client, create_client
from kinch_leveling_reflex.serializers import Category, Time

load_dotenv()

class SupabaseAPI:
    load_dotenv()
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
    
    def __init__(self):
        if self.SUPABASE_URL != None or self.SUPABASE_KEY != None:
            self.supabase: Client = create_client(
                self.SUPABASE_URL,
                self.SUPABASE_KEY,
            )

    def get_categories(self) -> list[Category]:
        response = self.supabase.table("categories").select("id, name, type(type)").execute()
        data = []
        
        if len(response.data) > 0:
            for category in response.data:
                data.append(Category(id=category['id'], name=category['name'], type=category['type']['type']))
                
        return data
        
    def get_times(self) -> list[Time]:
        response = self.supabase.table("times").select("categories(name), actual_time, goal_time, kaizen_proportion, xp").execute()
        data = []
        
        if len(response.data) > 0:
            for time in response.data:                                      
                data.append(Time(
                    category=time['categories']['name'], 
                    actual_time=float(time['actual_time']), 
                    goal_time=float(time['goal_time']), 
                    proportion=float(time['kaizen_proportion']),
                    xp=int(time['xp'])
                ))
            
        return data
    
    def update_time(self, category_id: int, actual_time: float, goal_time: float, proportion: float, xp: int) -> bool:
        response = self.supabase.table("times").update({
            "actual_time": actual_time,
            "goal_time": goal_time,
            "kaizen_proportion": proportion,
            "xp": xp
        }).eq("category_id", category_id).execute()
        
        return True if len(response.data) > 0 else False