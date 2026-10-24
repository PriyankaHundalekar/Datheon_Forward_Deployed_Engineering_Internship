class RBACManager:
    """Manages multi-tenant role-based access control and security metadata filters."""
    
    USER_PROFILES = {
        "alice_exec": {
            "name": "Alice Smith",
            "department": "Executive",
            "access_tier": "Tier-1"
        },
        "bob_eng": {
            "name": "Bob Jones",
            "department": "Engineering",
            "access_tier": "Tier-1"
        },
        "charlie_guest": {
            "name": "Charlie Davis",
            "department": "Engineering",
            "access_tier": "Tier-3"
        }
    }

    @classmethod
    def get_user_profile(cls, username: str) -> dict:
        """Retrieves user profile or defaults to a restricted guest profile."""
        return cls.USER_PROFILES.get(username, {
            "name": "External Guest",
            "department": "General",
            "access_tier": "Tier-3"
        })

    @staticmethod
    def build_filter(department: str) -> dict:
        """Constructs strict ChromaDB metadata filter for department isolation."""
        # Pass direct dictionary for single-condition filtering
        return {"department": {"$eq": department}}