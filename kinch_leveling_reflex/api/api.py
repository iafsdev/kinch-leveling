import reflex as rx
from kinch_leveling_reflex.api.SupabaseAPI import SupabaseAPI
from fastapi import FastAPI
from kinch_leveling_reflex.serializers import Category

fastapi_app = FastAPI()
supabase = SupabaseAPI()

@fastapi_app.get("/get_categories")
async def get_categories() -> list[Category]:
    return supabase.get_categories()

@fastapi_app.get("/get_kaizen")
async def get_kaizen() -> dict[str, float]:
    data = supabase.get_times()
    kaizen = {}
    
    for time in data:
        kaizen[time.category] = round(time.actual_time * time.proportion, 3)
    
    return kaizen