import streamlit as st
import sqlite3
from datetime import datetime

# ---- DATABASE SETUP ----
conn = sqlite3.connect("fare_data.db", check_same_thread=False)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS fare_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    old_fare REAL,
    new_fare REAL,
    timestamp TEXT
)
""")
conn.commit()

# ---- STREAMLIT UI ----
st.title("A Web-Based Ghana Current Transport Fare Adjustment - 15% Decrease")

# Use a form to allow Enter key submission
with st.form("fare_form"):
    old_fare = st.number_input("Enter Old Fare", min_value=0.0, format="%.2f")
    submit = st.form_submit_button("Calculate New Fare")  # Submit with Enter key or button

# If form was submitted
if submit:
    new_fare = old_fare * 0.85  # 15% decrease
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Display result
    st.success(f"New Fare after 15% decrease: ₵{new_fare:.2f}")

    # Save to database
    cursor.execute("INSERT INTO fare_records (old_fare, new_fare, timestamp) VALUES (?, ?, ?)",
                   (old_fare, new_fare, timestamp))
    conn.commit()
    
# Display price history in collapsible section
with st.expander("📊 View Fare History"):
    cursor.execute("SELECT * FROM fare_records ORDER BY id DESC")
    rows = cursor.fetchall()

    if rows:
        for row in rows:
            st.write(f"🕒 {row[3]} | Old Fare: ₵{row[1]:.2f} ➡ New Fare: ₵{row[2]:.2f}")
        
        # Add Clear History button
        if st.button("🗑 Clear History"):
            cursor.execute("DELETE FROM fare_records")
            conn.commit()
            st.warning("All history records have been deleted. Please refresh the app.")
    else:
        st.info("No records yet.")
        
       
    