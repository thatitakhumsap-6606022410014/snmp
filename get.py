from easysnmp import Session
import time
import schedule

# สร้างเซสชัน SNMP
session = Session(hostname='192.168.116.137', community='public', version=2)

# ฟังก์ชันดึงข้อมูลทราฟฟิก
def get_traffic():
    # ดึงข้อมูลทราฟฟิกเข้าและออก
    in_octets = session.get('.1.3.6.1.2.1.2.2.1.10.1')
    out_octets = session.get('.1.3.6.1.2.1.2.2.1.16.1')
    
    # แปลงค่าเป็น integer
    in_traffic = int(in_octets.value)
    out_traffic = int(out_octets.value)
    
    # แสดงผลข้อมูลทราฟฟิก
    print(f"Incoming traffic: {in_traffic} octets")
    print(f"Outgoing traffic: {out_traffic} octets")

# กำหนดให้ทำการตรวจสอบในช่วงเวลาต่าง ๆ
schedule.every(1).minute.do(get_traffic)  # ทุก 1 นาที
schedule.every(15).minutes.do(get_traffic)  # ทุก 15 นาที
schedule.every(30).minutes.do(get_traffic)  # ทุก 30 นาที
schedule.every(1).hour.do(get_traffic)  # ทุก 1 ชั่วโมง
schedule.every(1).day.do(get_traffic)  # ทุก 1 วัน

# รันการตรวจสอบตามที่กำหนด
while True:
    schedule.run_pending()
    time.sleep(1)
