from database.db_connection import get_db_connection

class DBOperations:

    # ------------------ GET ALL TRAINS ------------------
    def get_all_trains(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT train_id, train_name FROM trains"
        cursor.execute(query)
        trains = cursor.fetchall()

        cursor.close()
        conn.close()

        return trains


    # ------------------ INSERT BOOKING ------------------
    def insert_booking(self, passenger_name, email, train_id, journey_date, seat_number, travel_class, fare):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO bookings 
                (passenger_name, email, train_id, journey_date, seat_number, class, fare)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                passenger_name,
                email,
                train_id,
                journey_date,
                seat_number,
                travel_class,
                fare
            )

            cursor.execute(query, values)
            conn.commit()

            cursor.close()
            conn.close()

            return True

        except Exception as e:
            print("❌ Booking Insert Error:", e)
            return False


    # ------------------ GET TRAIN STATUS ------------------
    def get_train_status(self, train_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM trains WHERE train_id = %s"
        cursor.execute(query, (train_id,))
        train = cursor.fetchone()

        cursor.close()
        conn.close()

        return train


    # ------------------ GET ALL STATIONS ------------------
    def get_all_stations(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT station_name FROM stations"
        cursor.execute(query)
        stations = cursor.fetchall()

        cursor.close()
        conn.close()

        return stations
