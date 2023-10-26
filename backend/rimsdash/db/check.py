#quick check for connection to db
#returns version of postgres - should be 12
import psycopg2
import rimsdash.config as config

conn = psycopg2.connect(
    host=f"{config.get('database', 'host')}",
    database=f"{config.get('database', 'name')}",
    user=f"{config.get('database', 'username')}",
    password=f"{config.get('database', 'password')}",
    port=f"{config.get('database', 'port')}"
)

cur = conn.cursor()
cur.execute("SELECT version();")
print(cur.fetchone())
cur.close()
conn.close()