import os 
from dotenv import load_dotenv
from supabase import Client, create_client
from kinch_leveling_reflex.serializers import Category

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
        response = self.supabase.table("categories").select("name", "type(type)").execute()
        data = []
        
        if len(response.data) > 0:
            for category in response.data:
                data.append(Category(name=category['name'], type=category['type']['type']))
                
        return data
        