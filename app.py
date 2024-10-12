from flask import Flask, render_template, request
from pysnmp.hlapi import *

app = Flask(__name__)

# Function to set port status using SNMP
def set_port_status(port, status):
    # Example of SNMP SET function
    # Adjust ifAdminStatus (1: up, 2: down) for each port
    # Replace 'oid_ifAdminStatus' with the correct OID
    g = setCmd(SnmpEngine(),
               CommunityData('public', mpModel=0),
               UdpTransportTarget(('192.168.1.197', 161)),  # Replace target_ip with the actual IP
               ContextData(),
               ObjectType(ObjectIdentity('oid_ifAdminStatus.{}'.format(port)), Integer(status)))
    
    errorIndication, errorStatus, errorIndex, varBinds = next(g)
    
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print(f'{errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex) - 1][0] or "?"}')
    else:
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))

@app.route('/')
def index():
    # Display the switch and router UI for the ports
    return render_template('index.html', ports=8)

@app.route('/toggle_port', methods=['POST'])
def toggle_port():
    port = int(request.form['port'])
    status = int(request.form['status'])  # 1 for up, 2 for down

    # Toggle the port status using SNMP
    set_port_status(port, status)
    
    return {'status': 'success', 'new_status': 1 if status == 2 else 2}

if __name__ == '__main__':
    app.run(debug=False)
