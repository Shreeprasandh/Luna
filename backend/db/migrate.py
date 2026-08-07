"""
Luna Database Migration Runner
Runs pending migrations directly against Supabase PostgreSQL.
"""

import os
import sys
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn_params = {
    "host": os.getenv("SUPABASE_DB_HOST", "aws-0-ap-southeast-1.pooler.supabase.com"),
    "port": int(os.getenv("SUPABASE_DB_PORT", "5432")),
    "dbname": os.getenv("SUPABASE_DB_NAME", "postgres"),
    "user": os.getenv("SUPABASE_DB_USER", "postgres.aamwujutwulaaspjvdeg"),
    "password": os.getenv("SUPABASE_DB_PASSWORD", ""),
    "sslmode": "require",
    "connect_timeout": 15,
}

MIGRATIONS = {
    "001_memories_table": """
        CREATE TABLE IF NOT EXISTS memories (
            id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            content       TEXT NOT NULL,
            source        TEXT DEFAULT 'conversation',
            embedding     vector(768),
            tags          TEXT[] DEFAULT '{}',
            importance    FLOAT DEFAULT 1.0,
            user_id       TEXT DEFAULT 'default',
            created_at    TIMESTAMPTZ DEFAULT now(),
            last_accessed TIMESTAMPTZ DEFAULT now()
        );
        ALTER TABLE memories ENABLE ROW LEVEL SECURITY;
    """,

    "003_preferences": """
        CREATE TABLE IF NOT EXISTS preferences (
            id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            key        TEXT NOT NULL UNIQUE,
            value      TEXT NOT NULL,
            updated_at TIMESTAMPTZ DEFAULT now()
        );
        ALTER TABLE preferences ENABLE ROW LEVEL SECURITY;
    """,

    "004_pending_tasks": """
        CREATE TABLE IF NOT EXISTS pending_tasks (
            id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            description  TEXT NOT NULL,
            tool         TEXT NOT NULL,
            params       JSONB,
            status       TEXT DEFAULT 'pending',
            created_at   TIMESTAMPTZ DEFAULT now(),
            completed_at TIMESTAMPTZ
        );
        ALTER TABLE pending_tasks ENABLE ROW LEVEL SECURITY;
    """,

    "005_match_memories_fn": """
        CREATE OR REPLACE FUNCTION match_memories(
            query_embedding vector(768),
            match_threshold FLOAT DEFAULT 0.75,
            match_count     INT   DEFAULT 5
        )
        RETURNS TABLE (
            id            UUID,
            content       TEXT,
            source        TEXT,
            tags          TEXT[],
            importance    FLOAT,
            similarity    FLOAT
        )
        LANGUAGE sql STABLE
        AS $$
            SELECT
                m.id,
                m.content,
                m.source,
                m.tags,
                m.importance,
                1 - (m.embedding <=> query_embedding) AS similarity
            FROM memories m
            WHERE 1 - (m.embedding <=> query_embedding) > match_threshold
            ORDER BY m.embedding <=> query_embedding
            LIMIT match_count;
        $$;
    """,

    "006_update_last_accessed_fn": """
        CREATE OR REPLACE FUNCTION update_memory_accessed(memory_id UUID)
        RETURNS void
        LANGUAGE sql
        AS $$
            UPDATE memories
            SET last_accessed = now()
            WHERE id = memory_id;
        $$;
    """,

    "007_rls_policies": """
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'service_role_all_memories') THEN
                CREATE POLICY "service_role_all_memories" ON memories FOR ALL USING (auth.role() = 'service_role');
            END IF;

            IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'service_role_all_preferences') THEN
                CREATE POLICY "service_role_all_preferences" ON preferences FOR ALL USING (auth.role() = 'service_role');
            END IF;

            IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'service_role_all_pending_tasks') THEN
                CREATE POLICY "service_role_all_pending_tasks" ON pending_tasks FOR ALL USING (auth.role() = 'service_role');
            END IF;
        END $$;
    """,
}


def run():
    print("Connecting to Supabase PostgreSQL...")
    try:
        conn = psycopg2.connect(**conn_params)
        conn.autocommit = True
        cur = conn.cursor()
        print("Connected.\n")

        for name, sql in MIGRATIONS.items():
            print(f"Running migration: {name}...")
            try:
                cur.execute(sql)
                print(f"  {name} — OK\n")
            except psycopg2.Error as e:
                print(f"  {name} — FAILED: {e}\n")
                cur.close()
                conn.close()
                sys.exit(1)

        cur.close()
        conn.close()
        print("All migrations complete.")

    except psycopg2.OperationalError as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()
