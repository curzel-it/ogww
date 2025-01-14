import sqlite3
import uuid
import time
import random
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
def generate_uuid():
    return str(uuid.uuid4())

def insert_user(conn, username, email, password, is_admin):
    sql = """
    INSERT INTO users (id, username, email, hashed_password, is_admin)
    VALUES (?, ?, ?, ?, ?)
    """
    uuid = generate_uuid()
    hashed_password = pwd_context.hash(password)
    data = (uuid, username, email, hashed_password, is_admin)
    conn.execute(sql, data)
    conn.commit()
    return uuid

def insert_hero(conn, name):
    sql = """
    INSERT INTO heroes (id, name)
    VALUES (?, ?)
    """
    uuid = generate_uuid()
    data = (uuid, name)
    conn.execute(sql, data)
    conn.commit()
    return uuid

def insert_user_hero_relationship(conn, user_id, hero_id, level, settings):
    sql = """
    INSERT INTO user_hero_relationships (id, user_id, hero_id, level, settings)
    VALUES (?, ?, ?, ?, ?)
    """
    uuid = generate_uuid()
    data = (uuid, user_id, hero_id, level, settings)
    conn.execute(sql, data)
    conn.commit()
    return uuid

def insert_site(conn, owner_id, name, x, y, z):
    sql = """
    INSERT INTO sites (id, owner_id, name, x, y, z, available_metal, available_crystals, available_deuterium, beans_factory_level, mana_extraction_plan_level, gotcha_temple_level, cannon_meat_farm_level, metal_stock_level, crystal_stock_level, deuterium_stock_level)
    VALUES (?, ?, ?, ?, ?, ?, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    """
    uuid = generate_uuid()
    data = (uuid, owner_id, name, x, y, z)
    conn.execute(sql, data)
    conn.commit()
    return uuid

def insert_army(conn, owner_id, starting_site_id, departure_time, starlight_sprinter, nebula_noodle_hauler):
    sql = """
    INSERT INTO armies (id, owner_id, starting_site_id, departure_time, starlight_sprinter, nebula_noodle_hauler)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    uuid = generate_uuid()
    data = (uuid, owner_id, starting_site_id, departure_time, starlight_sprinter, nebula_noodle_hauler)
    conn.execute(sql, data)
    conn.commit()
    return uuid

def main():
    db_file = "backend/game.db"
    conn = sqlite3.connect(db_file)
    
    conn.execute("DELETE FROM armies")
    conn.execute("DELETE FROM sites")
    conn.execute("DELETE FROM user_hero_relationships")
    conn.execute("DELETE FROM heroes")
    conn.execute("DELETE FROM users")
    conn.commit()
    
    try:
        admin_id = insert_user(conn, "hiddenmugs", "saffo.montesi@gmail.com", "notsecure", True)
        user1_id = insert_user(conn, "user1", "user1@example.com", "notsecure", False)
        user2_id = insert_user(conn, "user2", "user2@example.com", "notsecure", False)
        insert_hero(conn, "Hero1")
        insert_hero(conn, "Hero2")
        insert_hero(conn, "Hero3")
        insert_hero(conn, "Hero4")
        
        for z in range(1):
            for y in range(255):
                for x in range(random.randint(5, 15)):
                    insert_site(conn, None, f"Planet {x} {y} {z}", x, y, z)

        conn.execute("UPDATE sites SET owner_id = ? WHERE y = 0", [admin_id])
        conn.execute("UPDATE sites SET owner_id = ? WHERE y = 1 AND x > 4", [user1_id])
        conn.execute("UPDATE sites SET owner_id = ? WHERE y = 2 AND x < 5", [user2_id])
        conn.commit()

        print("Default data inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
