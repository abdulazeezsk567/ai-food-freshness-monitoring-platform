import pytest
from sqlalchemy import create_engine
from app.core.config import normalize_database_url, Settings

def test_normalize_database_url_postgres_prefix():
    raw_url = "postgres://render_user:secret_pass@dpg-abc123xyz.oregon-postgres.render.com/food_freshness_db"
    normalized = normalize_database_url(raw_url)
    assert normalized == "postgresql+psycopg2://render_user:secret_pass@dpg-abc123xyz.oregon-postgres.render.com/food_freshness_db"

def test_normalize_database_url_postgresql_prefix():
    raw_url = "postgresql://local_user:local_pass@localhost:5432/food_freshness_db"
    normalized = normalize_database_url(raw_url)
    assert normalized == "postgresql+psycopg2://local_user:local_pass@localhost:5432/food_freshness_db"

def test_normalize_database_url_already_normalized():
    raw_url = "postgresql+psycopg2://custom_user:custom_pass@pg.host:5432/food_freshness_db"
    normalized = normalize_database_url(raw_url)
    assert normalized == raw_url
    assert not normalized.startswith("postgresql+psycopg2+psycopg2://")

def test_normalize_database_url_sqlite_preserved():
    sqlite_url = "sqlite:///./food_freshness.db"
    assert normalize_database_url(sqlite_url) == sqlite_url

    memory_url = "sqlite:///:memory:"
    assert normalize_database_url(memory_url) == memory_url

def test_sqlalchemy_engine_dialect_psycopg2_selection():
    normalized = normalize_database_url("postgres://render_user:secret_pass@dpg-abc123xyz.oregon-postgres.render.com/food_freshness_db")
    engine = create_engine(normalized)
    assert engine.dialect.name == "postgresql"
    assert engine.dialect.driver == "psycopg2"

def test_settings_pydantic_validator_normalizes_postgres_url():
    test_settings = Settings(DATABASE_URL="postgres://usr:pwd@host:5432/db")
    assert test_settings.DATABASE_URL == "postgresql+psycopg2://usr:pwd@host:5432/db"

def test_normalize_database_url_psycopg_v3_prefix():
    raw_url = "postgresql+psycopg://render_user:secret_pass@dpg-abc123xyz.oregon-postgres.render.com/food_freshness_db"
    normalized = normalize_database_url(raw_url)
    assert normalized == "postgresql+psycopg2://render_user:secret_pass@dpg-abc123xyz.oregon-postgres.render.com/food_freshness_db"

def test_normalize_database_url_quoted_and_whitespace():
    raw_url = '  "postgres://render_user:secret_pass@host:5432/food_freshness_db"  '
    normalized = normalize_database_url(raw_url)
    assert normalized == "postgresql+psycopg2://render_user:secret_pass@host:5432/food_freshness_db"
