import reflex as rx
from kinch_leveling_reflex.api.SupabaseAPI import SupabaseAPI
from fastapi import FastAPI
from kinch_leveling_reflex.serializers import Category

fastapi_app = FastAPI()
supabase = SupabaseAPI()

@fastapi_app.get("/get_categories")
async def get_categories() -> list[Category]:
    return supabase.get_categories()

async def get_kaizen() -> list[str]:
    pass