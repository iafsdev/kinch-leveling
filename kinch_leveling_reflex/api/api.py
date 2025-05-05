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
async def get_kaizen() -> dict[str, str]:
    data = supabase.get_times()
    kaizen = {}
    
    for time in data:
        kaizen_calculation = round(time.actual_time * time.proportion, 3)
        minutes = int(kaizen_calculation / 60)
        seconds = round(kaizen_calculation - minutes * 60, 3)
        kaizen[time.category] = f"{minutes}:{seconds:06.3f}" if minutes > 0 else f"{seconds:06.3f}"
    
    return kaizen