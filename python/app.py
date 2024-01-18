from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# Database connection parameters
db_params = {
    "dbname": "nginxDB",
    "user": "xavier",
    "password": "yourpassword",
    "host": "localhost",  # Change this if your database is on a different host
}


# Function to create the "pressed" table
def create_pressed_table():
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        # Check if a row exists in the "pressed" table
        cur.execute("SELECT 1 FROM pressed LIMIT 1;")
        if cur.fetchone() is None:
            # If no row exists, insert an initial row with count = 1
            cur.execute("INSERT INTO pressed (count) VALUES (1);")
        else:
            # If a row exists, increment the count
            cur.execute("UPDATE pressed SET count = count + 1;")
        conn.commit()
    except Exception as e:
        print(str(e))
    finally:
        if conn:
            conn.close()


# Function to get the count from the "pressed" table
def get_pressed_count():
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        # Retrieve the count from the "pressed" table
        cur.execute("SELECT count FROM pressed;")
        count = cur.fetchone()[0] if cur.rowcount > 0 else 0
        return count
    except Exception as e:
        print(str(e))
        return 0
    finally:
        if conn:
            conn.close()


# Define a route to get the status
@app.route("/api/get-status", methods=["GET"])
def get_status():
    # Get the count from the "pressed" table
    count = get_pressed_count()
    return jsonify({"count": count})


# Define a route to increment the "pressed" table
@app.route("/api/pressed", methods=["GET"])
def increment_pressed():
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        # Increment the "pressed" table
        cur.execute("UPDATE pressed SET count = count + 1;")
        conn.commit()
        # Get the updated count
        count = get_pressed_count()
        return jsonify({"count": count})
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    # Create the "pressed" table if it doesn't exist
    create_pressed_table()
    app.run(host="0.0.0.0", port=5000)  # Replace with your preferred host and port
