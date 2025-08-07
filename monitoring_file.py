from flask import Flask, request, jsonify, render_template
import json
from datetime import datetime
import sqlite3

app = Flask(__name__)

# Simple thresholds 
THRESHOLDS = {
    'failed_high': 5,    # Alert if more than 5 failed transactions
    'denied_high': 10,   # Alert if more than 10 denied transactions  
    'reversed_high': 5,  # Alert if more than 5 reversed transactions
    'approved_low': 90,  # Alert if less than 90 approved transactions
    'approved_high': 150 # Alert if more than 150 approved transactions
}

# Storing  recent transactions in memory 
recent_transactions = []

def check_anomalies(transaction):
    """Simple anomaly detection"""
    anomalies = []
    status = transaction['status']
    count = transaction['count']
    
    # Check failed transactions
    if status == 'failed' and count > THRESHOLDS['failed_high']:
        anomalies.append({
            'type': 'HIGH_FAILED_RATE',
            'message': f'Failed transactions ({count}) above normal threshold ({THRESHOLDS["failed_high"]})',
            'severity': 'HIGH'
        })
    
    # Check denied transactions
    elif status == 'denied' and count > THRESHOLDS['denied_high']:
        anomalies.append({
            'type': 'HIGH_DENIED_RATE', 
            'message': f'Denied transactions ({count}) above normal threshold ({THRESHOLDS["denied_high"]})',
            'severity': 'HIGH'
        })
    
    # Check reversed transactions
    elif status == 'reversed' and count > THRESHOLDS['reversed_high']:
        anomalies.append({
            'type': 'HIGH_REVERSED_RATE',
            'message': f'Reversed transactions ({count}) above normal threshold ({THRESHOLDS["reversed_high"]})',
            'severity': 'MEDIUM'
        })
    
    # Check approved transactions
    elif status == 'approved':
        if count < THRESHOLDS['approved_low']:
            anomalies.append({
                'type': 'LOW_APPROVED_VOLUME',
                'message': f'Approved transactions ({count}) below normal threshold ({THRESHOLDS["approved_low"]})',
                'severity': 'MEDIUM'
            })
        elif count > THRESHOLDS['approved_high']:
            anomalies.append({
                'type': 'HIGH_APPROVED_VOLUME',
                'message': f'Approved transactions ({count}) above normal threshold ({THRESHOLDS["approved_high"]})',
                'severity': 'LOW'
            })
    
    return anomalies

def send_alert(anomaly):
    """Simple alert system - prints to console"""
    print("\n" + "="*50)
    print("🚨 ALERT DETECTED!")
    print("="*50)
    print(f"Type: {anomaly['type']}")
    print(f"Message: {anomaly['message']}")
    print(f"Severity: {anomaly['severity']}")
    print(f"Time: {datetime.now()}")
    print("="*50 + "\n")

@app.route('/')
def dashboard():
    """Simple dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/transaction', methods=['POST'])
def receive_transaction():
    """Main endpoint - receives transaction data and checks for anomalies"""
    try:
        # Get transaction data
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ['timestamp', 'status', 'count']):
            return jsonify({'error': 'Missing required fields: timestamp, status, count'}), 400
        
        # Create transaction record
        transaction = {
            'timestamp': data['timestamp'],
            'status': data['status'],
            'count': int(data['count'])
        }
        
        # Store transaction
        recent_transactions.append(transaction)
        
        # Keep only last 100 transactions
        if len(recent_transactions) > 100:
            recent_transactions.pop(0)
        
        # Check for anomalies
        anomalies = check_anomalies(transaction)
        
        # Send alerts if anomalies found
        for anomaly in anomalies:
            send_alert(anomaly)
        
        # Return response
        return jsonify({
            'status': 'success',
            'message': 'Transaction processed successfully',
            'anomalies_found': len(anomalies),
            'anomalies': anomalies
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'total_transactions': len(recent_transactions)
    })

@app.route('/api/transactions')
def get_transactions():
    """Get recent transactions for dashboard"""
    return jsonify({
        'status': 'success',
        'data': recent_transactions[-20:]  # Last 20 transactions
    })

@app.route('/api/stats')
def get_stats():
    """Get simple statistics"""
    if not recent_transactions:
        return jsonify({'message': 'No transactions yet'})
    
    # Count by status
    status_counts = {}
    for t in recent_transactions:
        status = t['status']
        status_counts[status] = status_counts.get(status, 0) + 1
    
    return jsonify({
        'total_transactions': len(recent_transactions),
        'status_counts': status_counts,
        'thresholds': THRESHOLDS
    })

if __name__ == '__main__':
    print("🚀 Starting Simple Transaction Monitoring System...")
    print("📊 Dashboard available at: http://localhost:8080")
    print("📡 API endpoint: http://localhost:8080/api/transaction")
    print("🔍 Health check: http://localhost:8080/api/health")
    print("\n" + "="*50)
    app.run(debug=True, host='127.0.0.1', port=8080) 