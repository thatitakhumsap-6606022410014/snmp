from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/interface_status', methods=['GET'])
def get_interface_status():
    # Mock data for interfaces. Replace with your SNMP code to fetch actual statuses.
    interfaces = [
        {'interface': 1, 'status': 'Up'},
        {'interface': 2, 'status': 'Down'},
        # Add more interfaces as needed
    ]
    return jsonify(interfaces)

@app.route('/api/update_interface', methods=['POST'])
def update_interface_status():
    data = request.get_json()
    oid = data['oid']
    status = data['status']

    # Add your SNMP code here to update the interface status based on `oid` and `status`
    # For example, use easysnmp or pysnmp to send SNMP commands.

    return jsonify({'message': 'Status updated successfully'})

if __name__ == '__main__':
    app.run(debug=True)
