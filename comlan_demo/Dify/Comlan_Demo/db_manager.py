import psycopg2
import streamlit as st

class DatabaseManager:
    # 数据库连接配置
    DB_CONFIG = {
        "host": "c-cosmos-pg-comlan.yca6d4g7qznr6b.postgres.cosmos.azure.com",
        "port": 5432,
        "database": "citus",
        "user": "citus",
        "password": "!@#qwe123qwe"
    }

    def __init__(self):
        self.config = self.DB_CONFIG
    
    def get_connection(self):
        try:
            conn = psycopg2.connect(**self.config)
            return conn
        except Exception as e:
            st.error(f"数据库连接失败: {str(e)}")
            return None
    
    def init_db(self):
        conn = self.get_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        password VARCHAR(256) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
            finally:
                cur.close()
                conn.close()
    
    def register_user(self, username, hashed_password):
        conn = self.get_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO users (username, password) VALUES (%s, %s)",
                    (username, hashed_password)
                )
                conn.commit()
                return True
            except Exception as e:
                st.error(f"注册失败: {str(e)}")
                return False
            finally:
                cur.close()
                conn.close()
    
    def verify_user(self, username, hashed_password):
        conn = self.get_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    "SELECT * FROM users WHERE username = %s AND password = %s",
                    (username, hashed_password)
                )
                user = cur.fetchone()
                return user is not None
            except Exception as e:
                st.error(f"登录失败: {str(e)}")
                return False
            finally:
                cur.close()
                conn.close()