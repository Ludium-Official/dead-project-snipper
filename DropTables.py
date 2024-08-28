import psycopg2

# PostgreSQL 연결 정보
conn = psycopg2.connect(
    host="your_host",     # PostgreSQL 서버 주소
    port = "your_port",   # PostgreSQL 포트
    database="your_database",   # 데이터베이스 이름
    user="your_user",     # 사용자 이름
    password="your_password"  # 비밀번호
)

# 커서 생성
cur = conn.cursor()

# 모든 테이블 삭제
drop_tables_query = """
DO $$ DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
        EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
    END LOOP;
END $$;
"""

# 모든 프로시저 삭제
drop_procedures_query = """
DO $$ DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT proname, oidvectortypes(proargtypes) AS args
              FROM pg_proc
              JOIN pg_namespace ns ON (pg_proc.pronamespace = ns.oid)
              WHERE ns.nspname = 'public') LOOP
        EXECUTE 'DROP PROCEDURE IF EXISTS ' || quote_ident(r.proname) || '(' || r.args || ')';
    END LOOP;
END $$;
"""

try:
    # 쿼리 실행
    cur.execute(drop_tables_query)
    cur.execute(drop_procedures_query)
    
    # 변경사항 커밋
    conn.commit()
    print("모든 테이블과 프로시저가 성공적으로 삭제되었습니다.")
except Exception as e:
    print(f"오류 발생: {e}")
    conn.rollback()
finally:
    # 커서와 연결 종료
    cur.close()
    conn.close()
