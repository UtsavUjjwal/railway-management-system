from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3

import random
import string
from datetime import datetime
import os

app = Flask(__name__, static_folder='static')
CORS(app)

DB_PATH = 'railway.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    with open('schema.sql', 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

def generate_pnr():
    return ''.join(random.choices(string.digits, k=10))

# ─── Serve Frontend ───────────────────────────────────────────────────────────

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/booking')
def booking_page():
    return send_from_directory('static', 'booking.html')

@app.route('/seat-availability')
def seat_page():
    return send_from_directory('static', 'seats.html')

# ─── Train Search ─────────────────────────────────────────────────────────────

@app.route('/api/trains/search', methods=['GET'])
def search_trains():
    source = request.args.get('source', '').strip()
    destination = request.args.get('destination', '').strip()
    journey_date = request.args.get('date', '').strip()

    if not source or not destination:
        return jsonify({'error': 'Source and destination are required'}), 400

    # Map date to day of week
    day_filter = ''
    if journey_date:
        try:
            d = datetime.strptime(journey_date, '%Y-%m-%d')
            day_abbr = d.strftime('%a')  # Mon, Tue, etc.
            day_filter = day_abbr
        except ValueError:
            pass

    conn = get_db()
    query = """
        SELECT * FROM trains
        WHERE LOWER(source) LIKE LOWER(?)
          AND LOWER(destination) LIKE LOWER(?)
    """
    params = [f'%{source}%', f'%{destination}%']

    rows = conn.execute(query, params).fetchall()
    conn.close()

    trains = []
    for row in rows:
        t = dict(row)
        if day_filter and day_filter not in t['days_of_operation']:
            continue
        trains.append(t)

    return jsonify({'trains': trains, 'count': len(trains)})

@app.route('/api/trains', methods=['GET'])
def get_all_trains():
    conn = get_db()
    rows = conn.execute('SELECT * FROM trains ORDER BY train_number').fetchall()
    conn.close()
    return jsonify({'trains': [dict(r) for r in rows]})

@app.route('/api/trains/<int:train_id>', methods=['GET'])
def get_train(train_id):
    conn = get_db()
    row = conn.execute('SELECT * FROM trains WHERE id = ?', (train_id,)).fetchone()
    conn.close()
    if not row:
        return jsonify({'error': 'Train not found'}), 404
    return jsonify(dict(row))

# ─── Seat Availability ────────────────────────────────────────────────────────

@app.route('/api/seats/<int:train_id>', methods=['GET'])
def seat_availability(train_id):
    journey_date = request.args.get('date', datetime.today().strftime('%Y-%m-%d'))

    conn = get_db()
    train = conn.execute('SELECT * FROM trains WHERE id = ?', (train_id,)).fetchone()
    if not train:
        conn.close()
        return jsonify({'error': 'Train not found'}), 404

    # Get booked seats for this date
    booked = conn.execute(
        "SELECT seat_number FROM bookings WHERE train_id=? AND journey_date=? AND status='CONFIRMED'",
        (train_id, journey_date)
    ).fetchall()
    conn.close()

    booked_seats = {r['seat_number'] for r in booked}
    total = train['total_seats']

    # Generate seat map (coaches A, B, C each with rows)
    coaches = []
    seats_per_coach = total // 3
    coach_labels = ['A', 'B', 'C']
    for ci, label in enumerate(coach_labels):
        seats = []
        for s in range(1, seats_per_coach + 1):
            seat_id = f"{label}{s}"
            seats.append({
                'id': seat_id,
                'available': seat_id not in booked_seats
            })
        coaches.append({'coach': label, 'seats': seats})

    return jsonify({
        'train': dict(train),
        'journey_date': journey_date,
        'total_seats': total,
        'available_seats': total - len(booked_seats),
        'booked_seats': len(booked_seats),
        'coaches': coaches
    })

# ─── Booking ──────────────────────────────────────────────────────────────────

@app.route('/api/book', methods=['POST'])
def book_ticket():
    data = request.get_json()

    required = ['train_id', 'journey_date', 'passenger_name', 'passenger_age',
                'passenger_gender', 'passenger_email', 'passenger_phone']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400

    conn = get_db()
    train = conn.execute('SELECT * FROM trains WHERE id = ?', (data['train_id'],)).fetchone()
    if not train:
        conn.close()
        return jsonify({'error': 'Train not found'}), 404

    if train['available_seats'] <= 0:
        conn.close()
        return jsonify({'error': 'No seats available'}), 400

    # Find a free seat
    booked = conn.execute(
        "SELECT seat_number FROM bookings WHERE train_id=? AND journey_date=? AND status='CONFIRMED'",
        (data['train_id'], data['journey_date'])
    ).fetchall()
    booked_set = {r['seat_number'] for r in booked}

    seat_number = None
    coaches = ['A', 'B', 'C']
    for c in coaches:
        for s in range(1, (train['total_seats'] // 3) + 1):
            sid = f"{c}{s}"
            if sid not in booked_set:
                seat_number = sid
                break
        if seat_number:
            break

    if not seat_number:
        conn.close()
        return jsonify({'error': 'No seats available'}), 400

    # Insert passenger
    cur = conn.execute(
        'INSERT INTO passengers (name, age, gender, email, phone) VALUES (?,?,?,?,?)',
        (data['passenger_name'], data['passenger_age'], data['passenger_gender'],
         data['passenger_email'], data['passenger_phone'])
    )
    passenger_id = cur.lastrowid

    # Generate unique PNR
    pnr = generate_pnr()
    while conn.execute('SELECT id FROM bookings WHERE pnr=?', (pnr,)).fetchone():
        pnr = generate_pnr()

    booking_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn.execute(
        '''INSERT INTO bookings (pnr, train_id, passenger_id, journey_date, seat_number, booking_date, total_fare)
           VALUES (?,?,?,?,?,?,?)''',
        (pnr, data['train_id'], passenger_id, data['journey_date'],
         seat_number, booking_date, train['fare'])
    )

    conn.execute(
        'UPDATE trains SET available_seats = available_seats - 1 WHERE id = ?',
        (data['train_id'],)
    )

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'pnr': pnr,
        'seat_number': seat_number,
        'train_name': train['train_name'],
        'train_number': train['train_number'],
        'source': train['source'],
        'destination': train['destination'],
        'departure_time': train['departure_time'],
        'arrival_time': train['arrival_time'],
        'journey_date': data['journey_date'],
        'passenger_name': data['passenger_name'],
        'fare': train['fare']
    }), 201

@app.route('/api/bookings/<pnr>', methods=['GET'])
def get_booking(pnr):
    conn = get_db()
    row = conn.execute('''
        SELECT b.*, t.train_name, t.train_number, t.source, t.destination,
               t.departure_time, t.arrival_time,
               p.name as passenger_name, p.age, p.gender, p.email, p.phone
        FROM bookings b
        JOIN trains t ON b.train_id = t.id
        JOIN passengers p ON b.passenger_id = p.id
        WHERE b.pnr = ?
    ''', (pnr,)).fetchone()
    conn.close()
    if not row:
        return jsonify({'error': 'Booking not found'}), 404
    return jsonify(dict(row))

# ─── Stations (for autocomplete) ─────────────────────────────────────────────

@app.route('/api/stations', methods=['GET'])
def get_stations():
    conn = get_db()
    sources = conn.execute('SELECT DISTINCT source as station FROM trains').fetchall()
    dests = conn.execute('SELECT DISTINCT destination as station FROM trains').fetchall()
    conn.close()
    stations = list({r['station'] for r in sources} | {r['station'] for r in dests})
    stations.sort()
    return jsonify({'stations': stations})

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
