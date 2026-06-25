import pytest
from src.models.user import User
from src.config.settings import UserRole, PrivacyMode

def test_user_model_creation():
    """Test that we can create a User model instance."""
    user = User(
        name="Test User",
        email="test@engageiq.com",
        password="hashed_password",
        role=UserRole.STUDENT,
        privacy_mode=PrivacyMode.LOCAL_ONLY
    )
    
    assert user.name == "Test User"
    assert user.email == "test@engageiq.com"
    assert user.role == UserRole.STUDENT
