from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import hashlib
import datetime

app = Flask(__name__)
CORS(app)  # Allows frontend HTML to talk to this backend

DATABASE = 'helpdesk.db'

# ─────────────────────────────────────────
# HELPER — connect to database
# ─────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # return rows as dictionaries
    return conn

# ─────────────────────────────────────────
# HELPER — hash password
# ─────────────────────────────────────────
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ─────────────────────────────────────────
# CREATE TABLES on first run
# ─────────────────────────────────────────
def create_tables():
    conn = get_db()
    cursor = conn.cursor()

    # USERS table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            name       TEXT    NOT NULL,
            email      TEXT    UNIQUE NOT NULL,
            password   TEXT    NOT NULL,
            department TEXT,
            role       TEXT    DEFAULT 'employee',
            created_at TEXT    DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # TICKETS table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT    NOT NULL,
            description TEXT    NOT NULL,
            category    TEXT    NOT NULL,
            department  TEXT,
            priority    TEXT    DEFAULT 'Medium',
            status      TEXT    DEFAULT 'Open',
            deadline    TEXT,
            contact     TEXT,
            user_id     INTEGER,
            created_at  TEXT    DEFAULT CURRENT_TIMESTAMP,
            updated_at  TEXT    DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()
    print("[OK] Tables created successfully!")

# ═══════════════════════════════════════════
#  AUTH ROUTES
# ═══════════════════════════════════════════

# ── REGISTER ──
@app.route('/api/register', methods=['POST'])
def register():
    data     = request.get_json()
    name     = data.get('name')
    email    = data.get('email')
    password = data.get('password')
    dept     = data.get('department', '')

    if not name or not email or not password:
        return jsonify({'success': False, 'message': 'Name, email and password are required'}), 400

    try:
        conn   = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (name, email, password, department) VALUES (?, ?, ?, ?)',
            (name, email, hash_password(password), dept)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return jsonify({'success': True, 'message': 'Account created successfully!', 'user_id': user_id}), 201

    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'message': 'Email already registered'}), 409


# ── LOGIN ──
@app.route('/api/login', methods=['POST'])
def login():
    data     = request.get_json()
    email    = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required'}), 400

    conn   = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM users WHERE email = ? AND password = ?',
        (email, hash_password(password))
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({
            'success': True,
            'message': 'Login successful!',
            'user': {
                'id':         user['id'],
                'name':       user['name'],
                'email':      user['email'],
                'department': user['department'],
                'role':       user['role']
            }
        }), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid email or password'}), 401


# ═══════════════════════════════════════════
#  TICKET ROUTES
# ═══════════════════════════════════════════

# ── CREATE TICKET ──
@app.route('/api/tickets', methods=['POST'])
def create_ticket():
    data = request.get_json()

    title       = data.get('title')
    description = data.get('description')
    category    = data.get('category')
    department  = data.get('department', '')
    priority    = data.get('priority', 'Medium')
    status      = data.get('status', 'Open')
    deadline    = data.get('deadline', '')
    contact     = data.get('contact', '')
    user_id     = data.get('user_id', 1)

    if not title or not description or not category:
        return jsonify({'success': False, 'message': 'Title, description and category are required'}), 400

    conn   = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tickets
        (title, description, category, department, priority, status, deadline, contact, user_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (title, description, category, department, priority, status, deadline, contact, user_id))
    conn.commit()
    ticket_id = cursor.lastrowid
    conn.close()

    return jsonify({
        'success':   True,
        'message':   'Ticket created successfully!',
        'ticket_id': ticket_id
    }), 201


# ── GET ALL TICKETS ──
@app.route('/api/tickets', methods=['GET'])
def get_tickets():
    status   = request.args.get('status', '')
    priority = request.args.get('priority', '')
    user_id  = request.args.get('user_id', '')

    conn   = get_db()
    cursor = conn.cursor()

    query  = 'SELECT * FROM tickets WHERE 1=1'
    params = []

    if status:
        query += ' AND status = ?'
        params.append(status)
    if priority:
        query += ' AND priority = ?'
        params.append(priority)
    if user_id:
        query += ' AND user_id = ?'
        params.append(user_id)

    query += ' ORDER BY created_at DESC'
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    tickets = [dict(row) for row in rows]
    return jsonify({'success': True, 'tickets': tickets, 'total': len(tickets)}), 200


# ── GET SINGLE TICKET ──
@app.route('/api/tickets/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    conn   = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tickets WHERE id = ?', (ticket_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return jsonify({'success': True, 'ticket': dict(row)}), 200
    else:
        return jsonify({'success': False, 'message': 'Ticket not found'}), 404


# ── UPDATE TICKET STATUS ──
@app.route('/api/tickets/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    data       = request.get_json()
    status     = data.get('status')
    priority   = data.get('priority')
    updated_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn   = get_db()
    cursor = conn.cursor()

    if status and priority:
        cursor.execute(
            'UPDATE tickets SET status=?, priority=?, updated_at=? WHERE id=?',
            (status, priority, updated_at, ticket_id)
        )
    elif status:
        cursor.execute(
            'UPDATE tickets SET status=?, updated_at=? WHERE id=?',
            (status, updated_at, ticket_id)
        )
    elif priority:
        cursor.execute(
            'UPDATE tickets SET priority=?, updated_at=? WHERE id=?',
            (priority, updated_at, ticket_id)
        )

    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Ticket updated successfully!'}), 200


# ── DELETE TICKET ──
@app.route('/api/tickets/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    conn   = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tickets WHERE id = ?', (ticket_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Ticket deleted successfully!'}), 200


# ── DASHBOARD STATS ──
@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn   = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) as total FROM tickets')
    total = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) as cnt FROM tickets WHERE status='Open'")
    open_count = cursor.fetchone()['cnt']

    cursor.execute("SELECT COUNT(*) as cnt FROM tickets WHERE status='Solved'")
    solved_count = cursor.fetchone()['cnt']

    cursor.execute("SELECT COUNT(*) as cnt FROM tickets WHERE status='In Progress'")
    progress_count = cursor.fetchone()['cnt']

    cursor.execute("SELECT COUNT(*) as cnt FROM tickets WHERE status='Not Viewed'")
    notview_count = cursor.fetchone()['cnt']

    cursor.execute('SELECT COUNT(*) as cnt FROM users')
    user_count = cursor.fetchone()['cnt']

    conn.close()

    ai_rate = round((solved_count / total * 100)) if total > 0 else 0

    return jsonify({
        'success':        True,
        'total':          total,
        'open':           open_count,
        'solved':         solved_count,
        'in_progress':    progress_count,
        'not_viewed':     notview_count,
        'total_users':    user_count,
        'ai_resolution':  f'{ai_rate}%'
    }), 200


# ── HISTORY — all tickets with filters ──
@app.route('/api/history', methods=['GET'])
def get_history():
    conn   = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tickets ORDER BY created_at DESC')
    rows = cursor.fetchall()
    conn.close()
    tickets = [dict(row) for row in rows]
    return jsonify({'success': True, 'history': tickets, 'total': len(tickets)}), 200


# ─────────────────────────────────────────
# RUN APP
# ─────────────────────────────────────────
if __name__ == '__main__':
    create_tables()
    print("[START] Smart Helpdesk Backend is running!")
    print("[URL] Open: http://127.0.0.1:5000")
    app.run(debug=True)
