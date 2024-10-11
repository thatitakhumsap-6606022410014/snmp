from flask import Flask, jsonify, request
from easysnmp import Session

app = Flask(__name__)

# ตั้งค่า session SNMP (เปลี่ยน IP และ community string ให้ตรงกับอุปกรณ์ของคุณ)
session = Session(hostname='192.168.116.137', community='public', version=2)

# ฟังก์ชันดึงข้อมูลสถานะของอินเทอร์เฟซ
def get_interface_status(interface_oid):
    interface_status = session.get(interface_oid)
    return 'Up' if int(interface_status.value) == 1 else 'Down'

# Endpoint สำหรับดึงสถานะของอินเทอร์เฟซ
@app.route('/api/interface_status', methods=['GET'])
def interface_status():
    interface_oids = [
        '1.3.6.1.2.1.2.2.1.7.1',  # เปลี่ยน OID ตามต้องการ
        '1.3.6.1.2.1.2.2.1.7.2',
        # เพิ่ม OIDs สำหรับอินเทอร์เฟซอื่นๆ
    ]
    statuses = [{'interface': i + 1, 'status': get_interface_status(oid)} for i, oid in enumerate(interface_oids)]
    return jsonify(statuses)

# Endpoint สำหรับอัพเดทสถานะอินเทอร์เฟซ
@app.route('/api/update_interface', methods=['POST'])
def update_interface():
    data = request.get_json()
    interface_oid = data.get('oid')
    new_status = data.get('status')
    session.set(interface_oid, 'i', 1 if new_status == 'Up' else 2)
    return jsonify({'message': 'Interface updated successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
