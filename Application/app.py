from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import os

app = Flask(__name__)
app.secret_key = 'insurance-qa-project-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///insurance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ─────────────────────────────────────────────
# DATABASE MODELS
# ─────────────────────────────────────────────

class Customer(db.Model):
    __tablename__ = 'customers'
    customer_id   = db.Column(db.Integer, primary_key=True)
    first_name    = db.Column(db.String(50), nullable=False)
    last_name     = db.Column(db.String(50), nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    phone         = db.Column(db.String(20))
    date_of_birth = db.Column(db.String(20))
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin      = db.Column(db.Boolean, default=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    policies      = db.relationship('Policy', backref='customer', lazy=True)
    quotes        = db.relationship('Quote',  backref='customer', lazy=True)

class Policy(db.Model):
    __tablename__ = 'policies'
    policy_id      = db.Column(db.Integer, primary_key=True)
    customer_id    = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    policy_type    = db.Column(db.String(50), nullable=False)   # Auto, Health, Life, Home
    coverage_amount= db.Column(db.Float, nullable=False)
    premium_amount = db.Column(db.Float, nullable=False)
    start_date     = db.Column(db.String(20), nullable=False)
    end_date       = db.Column(db.String(20), nullable=False)
    status         = db.Column(db.String(20), default='Active')  # Active, Expired, Cancelled
    created_at     = db.Column(db.DateTime, default=datetime.utcnow)
    claims         = db.relationship('Claim', backref='policy', lazy=True)

class Claim(db.Model):
    __tablename__ = 'claims'
    claim_id     = db.Column(db.Integer, primary_key=True)
    policy_id    = db.Column(db.Integer, db.ForeignKey('policies.policy_id'), nullable=False)
    claim_amount = db.Column(db.Float, nullable=False)
    claim_reason = db.Column(db.Text, nullable=False)
    status       = db.Column(db.String(20), default='Pending')  # Pending, Approved, Rejected
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at   = db.Column(db.DateTime, default=datetime.utcnow)

class Quote(db.Model):
    __tablename__ = 'quotes'
    quote_id       = db.Column(db.Integer, primary_key=True)
    customer_id    = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    policy_type    = db.Column(db.String(50), nullable=False)
    coverage_amount= db.Column(db.Float, nullable=False)
    quote_amount   = db.Column(db.Float, nullable=False)
    age            = db.Column(db.Integer)
    created_at     = db.Column(db.DateTime, default=datetime.utcnow)

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def calculate_premium(policy_type, coverage_amount, age):
    base_rates = {'Auto': 0.03, 'Health': 0.05, 'Life': 0.02, 'Home': 0.01}
    rate = base_rates.get(policy_type, 0.03)
    age_factor = 1 + (max(0, age - 25) * 0.01)
    return round(coverage_amount * rate * age_factor, 2)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'customer_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'customer_id' not in session or not session.get('is_admin'):
            flash('Admin access required.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# ─────────────────────────────────────────────
# AUTH ROUTES
# ─────────────────────────────────────────────

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name  = request.form.get('last_name',  '').strip()
        email      = request.form.get('email',      '').strip()
        phone      = request.form.get('phone',      '').strip()
        dob        = request.form.get('date_of_birth', '').strip()
        password   = request.form.get('password',   '')
        confirm    = request.form.get('confirm_password', '')

        if not all([first_name, last_name, email, password]):
            flash('All required fields must be filled.', 'danger')
            return render_template('register.html')
        if password != confirm:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')
        if len(password) < 8:
            flash('Password must be at least 8 characters.', 'danger')
            return render_template('register.html')
        if Customer.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return render_template('register.html')

        customer = Customer(
            first_name=first_name, last_name=last_name,
            email=email, phone=phone, date_of_birth=dob,
            password_hash=generate_password_hash(password)
        )
        db.session.add(customer)
        db.session.commit()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email',    '').strip()
        password = request.form.get('password', '')

        if not email or not password:
            flash('Email and password are required.', 'danger')
            return render_template('login.html')

        customer = Customer.query.filter_by(email=email).first()
        if not customer or not check_password_hash(customer.password_hash, password):
            flash('Invalid email or password.', 'danger')
            return render_template('login.html')

        session['customer_id'] = customer.customer_id
        session['name']        = customer.first_name
        session['is_admin']    = customer.is_admin

        if customer.is_admin:
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# ─────────────────────────────────────────────
# CUSTOMER ROUTES
# ─────────────────────────────────────────────

@app.route('/dashboard')
@login_required
def dashboard():
    customer = Customer.query.get(session['customer_id'])
    policies = Policy.query.filter_by(customer_id=customer.customer_id).all()
    claims   = []
    for p in policies:
        claims.extend(p.claims)
    return render_template('dashboard.html', customer=customer, policies=policies, claims=claims)

@app.route('/quote', methods=['GET', 'POST'])
@login_required
def quote():
    quote_result = None
    if request.method == 'POST':
        policy_type     = request.form.get('policy_type')
        coverage_amount = request.form.get('coverage_amount')
        age             = request.form.get('age')

        if not all([policy_type, coverage_amount, age]):
            flash('All fields are required.', 'danger')
            return render_template('quote.html')

        try:
            coverage_amount = float(coverage_amount)
            age             = int(age)
        except ValueError:
            flash('Invalid coverage amount or age.', 'danger')
            return render_template('quote.html')

        if coverage_amount <= 0:
            flash('Coverage amount must be greater than 0.', 'danger')
            return render_template('quote.html')
        if age < 18 or age > 100:
            flash('Age must be between 18 and 100.', 'danger')
            return render_template('quote.html')

        premium = calculate_premium(policy_type, coverage_amount, age)
        q = Quote(
            customer_id=session['customer_id'],
            policy_type=policy_type,
            coverage_amount=coverage_amount,
            quote_amount=premium,
            age=age
        )
        db.session.add(q)
        db.session.commit()
        quote_result = {'policy_type': policy_type, 'coverage': coverage_amount,
                        'premium': premium, 'age': age, 'quote_id': q.quote_id}

    return render_template('quote.html', quote_result=quote_result)

@app.route('/purchase/<int:quote_id>', methods=['GET', 'POST'])
@login_required
def purchase(quote_id):
    q = Quote.query.get_or_404(quote_id)
    if q.customer_id != session['customer_id']:
        flash('Unauthorized.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date   = request.form.get('end_date')

        if not start_date or not end_date:
            flash('Start and end dates are required.', 'danger')
            return render_template('purchase.html', quote=q)

        policy = Policy(
            customer_id=session['customer_id'],
            policy_type=q.policy_type,
            coverage_amount=q.coverage_amount,
            premium_amount=q.quote_amount,
            start_date=start_date,
            end_date=end_date,
            status='Active'
        )
        db.session.add(policy)
        db.session.commit()
        flash(f'Policy #{policy.policy_id} purchased successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('purchase.html', quote=q)

@app.route('/policies')
@login_required
def policies():
    customer_policies = Policy.query.filter_by(customer_id=session['customer_id']).all()
    return render_template('policies.html', policies=customer_policies)

@app.route('/claims', methods=['GET', 'POST'])
@login_required
def claims():
    customer_policies = Policy.query.filter_by(
        customer_id=session['customer_id'], status='Active').all()

    if request.method == 'POST':
        policy_id    = request.form.get('policy_id')
        claim_amount = request.form.get('claim_amount')
        claim_reason = request.form.get('claim_reason', '').strip()

        if not all([policy_id, claim_amount, claim_reason]):
            flash('All fields are required.', 'danger')
            return render_template('claims.html', policies=customer_policies)

        try:
            claim_amount = float(claim_amount)
            policy_id    = int(policy_id)
        except ValueError:
            flash('Invalid input.', 'danger')
            return render_template('claims.html', policies=customer_policies)

        policy = Policy.query.get(policy_id)
        if not policy or policy.customer_id != session['customer_id']:
            flash('Invalid policy selected.', 'danger')
            return render_template('claims.html', policies=customer_policies)
        if claim_amount <= 0:
            flash('Claim amount must be greater than 0.', 'danger')
            return render_template('claims.html', policies=customer_policies)
        if claim_amount > policy.coverage_amount:
            flash('Claim amount cannot exceed coverage amount.', 'danger')
            return render_template('claims.html', policies=customer_policies)
        if len(claim_reason) < 10:
            flash('Please provide a more detailed reason (at least 10 characters).', 'danger')
            return render_template('claims.html', policies=customer_policies)

        claim = Claim(policy_id=policy_id, claim_amount=claim_amount, claim_reason=claim_reason)
        db.session.add(claim)
        db.session.commit()
        flash(f'Claim #{claim.claim_id} submitted successfully!', 'success')
        return redirect(url_for('claim_tracking'))

    return render_template('claims.html', policies=customer_policies)

@app.route('/claim-tracking')
@login_required
def claim_tracking():
    customer_policies = Policy.query.filter_by(customer_id=session['customer_id']).all()
    all_claims = []
    for p in customer_policies:
        for c in p.claims:
            all_claims.append({'claim': c, 'policy': p})
    return render_template('claim_tracking.html', claims_data=all_claims)

# ─────────────────────────────────────────────
# ADMIN ROUTES
# ─────────────────────────────────────────────

@app.route('/admin')
@admin_required
def admin_dashboard():
    total_customers = Customer.query.filter_by(is_admin=False).count()
    total_policies  = Policy.query.count()
    total_claims    = Claim.query.count()
    pending_claims  = Claim.query.filter_by(status='Pending').count()
    recent_claims   = Claim.query.order_by(Claim.created_at.desc()).limit(5).all()
    return render_template('admin_dashboard.html',
        total_customers=total_customers, total_policies=total_policies,
        total_claims=total_claims, pending_claims=pending_claims,
        recent_claims=recent_claims)

@app.route('/admin/customers')
@admin_required
def admin_customers():
    customers = Customer.query.filter_by(is_admin=False).all()
    return render_template('admin_customers.html', customers=customers)

@app.route('/admin/claims')
@admin_required
def admin_claims():
    all_claims = Claim.query.order_by(Claim.created_at.desc()).all()
    return render_template('admin_claims.html', claims=all_claims)

@app.route('/admin/claims/<int:claim_id>/update', methods=['POST'])
@admin_required
def update_claim(claim_id):
    claim  = Claim.query.get_or_404(claim_id)
    status = request.form.get('status')
    if status in ['Approved', 'Rejected']:
        claim.status     = status
        claim.updated_at = datetime.utcnow()
        db.session.commit()
        flash(f'Claim #{claim_id} has been {status}.', 'success')
    return redirect(url_for('admin_claims'))

# ─────────────────────────────────────────────
# REST API ENDPOINTS  (for Postman testing)
# ─────────────────────────────────────────────

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    required = ['first_name', 'last_name', 'email', 'password']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    if Customer.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409
    if len(data['password']) < 8:
        return jsonify({'error': 'Password must be at least 8 characters'}), 400
    customer = Customer(
        first_name=data['first_name'], last_name=data['last_name'],
        email=data['email'], phone=data.get('phone', ''),
        password_hash=generate_password_hash(data['password'])
    )
    db.session.add(customer)
    db.session.commit()
    return jsonify({'message': 'Customer registered successfully', 'customer_id': customer.customer_id}), 201

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    email    = data.get('email', '')
    password = data.get('password', '')
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    customer = Customer.query.filter_by(email=email).first()
    if not customer or not check_password_hash(customer.password_hash, password):
        return jsonify({'error': 'Invalid email or password'}), 401
    return jsonify({'message': 'Login successful', 'customer_id': customer.customer_id,
                    'name': customer.first_name, 'is_admin': customer.is_admin}), 200

@app.route('/api/policies', methods=['GET'])
def api_policies():
    customer_id = request.args.get('customer_id')
    if customer_id:
        policies = Policy.query.filter_by(customer_id=customer_id).all()
    else:
        policies = Policy.query.all()
    return jsonify([{
        'policy_id': p.policy_id, 'customer_id': p.customer_id,
        'policy_type': p.policy_type, 'coverage_amount': p.coverage_amount,
        'premium_amount': p.premium_amount, 'start_date': p.start_date,
        'end_date': p.end_date, 'status': p.status
    } for p in policies]), 200

@app.route('/api/claim', methods=['POST'])
def api_claim():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    required = ['policy_id', 'claim_amount', 'claim_reason']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    policy = Policy.query.get(data['policy_id'])
    if not policy:
        return jsonify({'error': 'Policy not found'}), 404
    if float(data['claim_amount']) <= 0:
        return jsonify({'error': 'Claim amount must be greater than 0'}), 400
    if float(data['claim_amount']) > policy.coverage_amount:
        return jsonify({'error': 'Claim amount exceeds coverage amount'}), 400
    claim = Claim(policy_id=data['policy_id'],
                  claim_amount=float(data['claim_amount']),
                  claim_reason=data['claim_reason'])
    db.session.add(claim)
    db.session.commit()
    return jsonify({'message': 'Claim submitted successfully', 'claim_id': claim.claim_id}), 201

@app.route('/api/claim/<int:claim_id>', methods=['GET'])
def api_get_claim(claim_id):
    claim = Claim.query.get(claim_id)
    if not claim:
        return jsonify({'error': 'Claim not found'}), 404
    return jsonify({
        'claim_id': claim.claim_id, 'policy_id': claim.policy_id,
        'claim_amount': claim.claim_amount, 'claim_reason': claim.claim_reason,
        'status': claim.status, 'created_at': str(claim.created_at)
    }), 200

@app.route('/api/quote', methods=['POST'])
def api_quote():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    required = ['policy_type', 'coverage_amount', 'age']
    for field in required:
        if data.get(field) is None:
            return jsonify({'error': f'{field} is required'}), 400
    valid_types = ['Auto', 'Health', 'Life', 'Home']
    if data['policy_type'] not in valid_types:
        return jsonify({'error': f'policy_type must be one of {valid_types}'}), 400
    try:
        coverage = float(data['coverage_amount'])
        age      = int(data['age'])
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid coverage_amount or age'}), 400
    if coverage <= 0:
        return jsonify({'error': 'coverage_amount must be greater than 0'}), 400
    if age < 18 or age > 100:
        return jsonify({'error': 'age must be between 18 and 100'}), 400
    premium = calculate_premium(data['policy_type'], coverage, age)
    return jsonify({'policy_type': data['policy_type'], 'coverage_amount': coverage,
                    'age': age, 'estimated_premium': premium}), 200

# ─────────────────────────────────────────────
# INIT
# ─────────────────────────────────────────────

def create_admin():
    admin = Customer.query.filter_by(email='admin@insurance.com').first()
    if not admin:
        admin = Customer(
            first_name='Admin', last_name='User',
            email='admin@insurance.com', phone='555-0000',
            password_hash=generate_password_hash('Admin@1234'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin account created: admin@insurance.com / Admin@1234")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_admin()
    app.run(debug=True, port=5000)
