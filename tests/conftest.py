import pytest_asyncio
import uuid
from httpx import AsyncClient, ASGITransport
from datetime import date
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.main import app
from app.infra.database import Base, AsyncSessionLocal
from app.core.dependencies import get_db
from app.models.user import User, RoleEnum
from app.models.transaction import Transaction, TypeEnum, CategoryEnum
from app.core.security import create_access_token

SQLALCHEMY_TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine_test = create_async_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

admin_id = uuid.uuid4()
analyst_id = uuid.uuid4()
viewer_id = uuid.uuid4()

# Pre-hashed passwords for testing (bcrypt hash of "password")
ADMIN_PASSWORD_HASH = "$2b$12$hQFKXbhjQXdJ9.JIFxTrWeaQVFazPeazM4c3XsIY/D3oKtVdGnVj2"
ANALYST_PASSWORD_HASH = "$2b$12$hQFKXbhjQXdJ9.JIFxTrWeaQVFazPeazM4c3XsIY/D3oKtVdGnVj2"
VIEWER_PASSWORD_HASH = "$2b$12$hQFKXbhjQXdJ9.JIFxTrWeaQVFazPeazM4c3XsIY/D3oKtVdGnVj2"
INACTIVE_PASSWORD_HASH = "$2b$12$hQFKXbhjQXdJ9.JIFxTrWeaQVFazPeazM4c3XsIY/D3oKtVdGnVj2"

async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async with TestingSessionLocal() as session:
        # Seed users
        admin_user = User(id=admin_id, email="admin@test.com", full_name="Admin", hashed_password=ADMIN_PASSWORD_HASH, role=RoleEnum.ADMIN, is_active=True)
        analyst_user = User(id=analyst_id, email="analyst@test.com", full_name="Analyst", hashed_password=ANALYST_PASSWORD_HASH, role=RoleEnum.ANALYST, is_active=True)
        viewer_user = User(id=viewer_id, email="viewer@test.com", full_name="Viewer", hashed_password=VIEWER_PASSWORD_HASH, role=RoleEnum.VIEWER, is_active=True)
        inactive_user = User(id=uuid.uuid4(), email="inactive@test.com", full_name="Inactive", hashed_password=INACTIVE_PASSWORD_HASH, role=RoleEnum.VIEWER, is_active=False)
        
        session.add_all([admin_user, analyst_user, viewer_user, inactive_user])
        await session.commit()
    
    yield
    
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest_asyncio.fixture
async def db_session():
    async with TestingSessionLocal() as session:
        yield session

@pytest_asyncio.fixture
def admin_token():
    return create_access_token(subject=str(admin_id), role=RoleEnum.ADMIN.value)

@pytest_asyncio.fixture
def analyst_token():
    return create_access_token(subject=str(analyst_id), role=RoleEnum.ANALYST.value)

@pytest_asyncio.fixture
def viewer_token():
    return create_access_token(subject=str(viewer_id), role=RoleEnum.VIEWER.value)

@pytest_asyncio.fixture
async def sample_transaction(db_session, setup_db):
    tx = Transaction(
        id=uuid.uuid4(),
        amount=150.00,
        type=TypeEnum.EXPENSE,
        category=CategoryEnum.FOOD,
        date=date(2026, 4, 1),
        created_by=admin_id,
        is_deleted=False
    )
    db_session.add(tx)
    await db_session.commit()
    await db_session.refresh(tx)
    return tx
