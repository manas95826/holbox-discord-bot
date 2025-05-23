from supabase import create_client
from config.config import SUPABASE_URL, SUPABASE_KEY

class SupabaseClient:
    _instance = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SupabaseClient, cls).__new__(cls)
            cls._client = create_client(SUPABASE_URL, SUPABASE_KEY)
        return cls._instance

    @property
    def client(self):
        return self._client

# Create a singleton instance
supabase = SupabaseClient().client 