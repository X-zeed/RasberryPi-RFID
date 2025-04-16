from gpiozero import Button
from signal import pause
import time

# กำหนด GPIO สำหรับ D0 และ D1
D0_PIN = 17  # GPIO17
D1_PIN = 27  # GPIO27

# เก็บข้อมูลรหัสจาก reader
bits = []
last_bit_time = time.time()

# อ่านข้อมูลจาก Wiegand
def on_d0():
    global bits, last_bit_time
    bits.append('0')
    last_bit_time = time.time()

def on_d1():
    global bits, last_bit_time
    bits.append('1')
    last_bit_time = time.time()

# เช็คว่าข้อมูลครบแล้วหรือยัง (timeout)
def check_timeout():
    global bits, last_bit_time
    if len(bits) > 0 and time.time() - last_bit_time > 0.05:  # 50ms timeout
        card_id = int(''.join(bits)[1:-1], 2)  # เอาเฉพาะ data bits (ตัด parity bit)
        print(f"RFID Data: {card_id} (Binary: {''.join(bits)})")
        bits = []

# สร้างปุ่มรับสัญญาณ
d0 = Button(D0_PIN, pull_up=True)
d1 = Button(D1_PIN, pull_up=True)

d0.when_pressed = on_d0
d1.when_pressed = on_d1

print("Waiting for RFID card...")

try:
    while True:
        check_timeout()
        time.sleep(0.01)  # Sleep สั้น ๆ เพื่อลดการใช้ CPU
except KeyboardInterrupt:
    print("\nExiting.")

