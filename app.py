from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import date
import mysql.connector

# Database imports
from database.db_operations import DBOperations
from database.db_connection import get_db_connection

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for flash messages

# Create a single instance of DBOperations
db = DBOperations()

# ------------------ Home Page ------------------
@app.route('/')
def index():
    return render_template('index.html')


# ------------------ Booking Page ------------------
@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        try:
            # Debug: Print received form data
            print("\n📌 [DEBUG] Form Data Received:")
            print(request.form)

            passenger_name = request.form['passenger_name']
            email = request.form['email']
            train_id = request.form['train_id']
            journey_date = request.form['journey_date']
            travel_class = request.form['class']
            seat_number = request.form['seat_number']
            fare = 500  # Fixed fare

            print("\n📌 [DEBUG] Inserting Booking Data:")
            print(passenger_name, email, train_id, journey_date, travel_class, seat_number, fare)

            success = db.insert_booking(
                passenger_name,
                email,
                train_id,
                journey_date,
                seat_number,
                travel_class,
                fare
            )

            if success:
                flash("✅ Booking Successful!", "success")
            else:
                flash("❌ Booking Failed. Try Again.", "danger")

        except Exception as e:
            print("❌ ERROR:", e)
            flash(f"❌ Error: {str(e)}", "danger")

        return redirect(url_for('booking'))

    # GET request
    trains = db.get_all_trains()
    return render_template('booking.html', trains=trains)


# ------------------ Feedback Page ------------------
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        passenger_name = request.form['passenger_name']
        train_id = request.form['train_id']
        rating = request.form['rating']
        comments = request.form['comments']
        today = date.today()

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO feedback (passenger_name, Train_ID, Rating, Comments, Date)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (passenger_name, train_id, rating, comments, today))
            conn.commit()

            cursor.close()
            conn.close()

            flash("✅ Feedback submitted successfully!", "success")
            return redirect(url_for('feedback'))

        except mysql.connector.Error as err:
            print("❌ Database Error:", err)
            flash(f"❌ Database error: {err}", "danger")
            return redirect(url_for('feedback'))

    return render_template('feedback.html')


# ------------------ Train Status Page ------------------
@app.route('/train_status', methods=['GET', 'POST'])
def train_status():
    train_data = None

    if request.method == 'POST':
        try:
            train_id = request.form['train_id']
            train_data = db.get_train_status(train_id)

            if not train_data:
                flash("❌ Train not found or no data available!", "danger")

        except Exception as e:
            flash(f"❌ Error: {str(e)}", "danger")

    return render_template('train_status.html', train_data=train_data)


# ------------------ API: Train Status (JSON) ------------------
@app.route('/api/train_status/<train_id>', methods=['GET'])
def api_train_status(train_id):
    try:
        status = db.get_train_status(train_id)
        if status:
            return jsonify(status)
        return jsonify({"error": "Train not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ------------------ API: All Stations ------------------
@app.route('/api/stations', methods=['GET'])
def api_stations():
    try:
        stations = db.get_all_stations()
        return jsonify(stations)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ------------------ Run Flask App ------------------
if __name__ == '__main__':
    app.run(debug=True)
