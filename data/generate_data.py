import csv
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = BASE_DIR / "data" / "maintenance_records.csv"

AC_CASES = [
    {
        "complaint": "AC is not cooling properly",
        "symptoms": "Room remains warm even after running AC for 30 minutes",
        "previous_action": "Checked thermostat and cleaned outer unit",
        "root_cause": "Clogged air filter",
        "resolution": "Cleaned and replaced the air filter",
        "cost": 500,
        "repair_time": "1 hour",
        "urgency": "Medium",
        "technician_notes": "Airflow improved after filter replacement",
    },
    {
        "complaint": "AC making unusual noise",
        "symptoms": "Loud rattling noise from indoor unit",
        "previous_action": "Inspected indoor unit and fan",
        "root_cause": "Loose fan component",
        "resolution": "Tightened fan assembly and checked mounting",
        "cost": 800,
        "repair_time": "1.5 hours",
        "urgency": "Medium",
        "technician_notes": "Noise stopped after tightening the fan assembly",
    },
    {
        "complaint": "AC leaking water",
        "symptoms": "Water dripping from indoor AC unit",
        "previous_action": "Checked drain pipe",
        "root_cause": "Blocked condensate drain",
        "resolution": "Flushed and cleaned the condensate drain pipe",
        "cost": 600,
        "repair_time": "1 hour",
        "urgency": "High",
        "technician_notes": "Drainage restored after cleaning",
    },
]
GENERATOR_CASES = [
    {
        "complaint": "Generator is not starting",
        "symptoms": "Generator cranks but does not start",
        "previous_action": "Checked fuel level and battery",
        "root_cause": "Weak battery",
        "resolution": "Charged and replaced the battery",
        "cost": 3500,
        "repair_time": "2 hours",
        "urgency": "High",
        "technician_notes": "Generator started normally after battery replacement",
    },
    {
        "complaint": "Generator shuts down during operation",
        "symptoms": "Generator stops after running for several minutes",
        "previous_action": "Checked fuel supply and engine temperature",
        "root_cause": "Engine overheating",
        "resolution": "Cleaned cooling system and checked coolant level",
        "cost": 2500,
        "repair_time": "2 hours",
        "urgency": "High",
        "technician_notes": "Temperature returned to normal after cooling system service",
    },
    {
        "complaint": "Generator producing unusual vibration",
        "symptoms": "Strong vibration and abnormal sound during operation",
        "previous_action": "Inspected engine mounting",
        "root_cause": "Loose engine mounting bolts",
        "resolution": "Tightened engine mounting bolts",
        "cost": 1000,
        "repair_time": "1 hour",
        "urgency": "Medium",
        "technician_notes": "Vibration reduced significantly after tightening",
    },
]
PUMP_CASES = [
    {
        "complaint": "Water pump is not working",
        "symptoms": "Pump does not start when switched on",
        "previous_action": "Checked power supply and control switch",
        "root_cause": "Electrical connection failure",
        "resolution": "Repaired the electrical connection",
        "cost": 1200,
        "repair_time": "1.5 hours",
        "urgency": "High",
        "technician_notes": "Pump started normally after electrical repair",
    },
    {
        "complaint": "Water pressure is very low",
        "symptoms": "Pump runs but water flow is weak",
        "previous_action": "Checked inlet pipe and valve",
        "root_cause": "Clogged inlet filter",
        "resolution": "Cleaned the inlet filter",
        "cost": 700,
        "repair_time": "1 hour",
        "urgency": "Medium",
        "technician_notes": "Water pressure improved after filter cleaning",
    },
    {
        "complaint": "Water pump making loud noise",
        "symptoms": "Grinding sound while pump is running",
        "previous_action": "Inspected pump motor and bearings",
        "root_cause": "Worn motor bearing",
        "resolution": "Replaced the damaged bearing",
        "cost": 1800,
        "repair_time": "2 hours",
        "urgency": "Medium",
        "technician_notes": "Noise disappeared after bearing replacement",
    },
]
ELEVATOR_CASES = [
    {
        "complaint": "Elevator doors are not closing",
        "symptoms": "Doors remain open or repeatedly reopen",
        "previous_action": "Checked door sensor and tracks",
        "root_cause": "Dirty door sensor",
        "resolution": "Cleaned and recalibrated the door sensor",
        "cost": 900,
        "repair_time": "1 hour",
        "urgency": "High",
        "technician_notes": "Doors operated normally after sensor cleaning",
    },
    {
        "complaint": "Elevator making unusual noise",
        "symptoms": "Grinding noise while elevator is moving",
        "previous_action": "Inspected guide rails and moving components",
        "root_cause": "Insufficient rail lubrication",
        "resolution": "Lubricated guide rails and checked alignment",
        "cost": 1500,
        "repair_time": "2 hours",
        "urgency": "Medium",
        "technician_notes": "Noise reduced after lubrication",
    },
    {
        "complaint": "Elevator stops between floors",
        "symptoms": "Elevator stops unexpectedly before reaching the selected floor",
        "previous_action": "Checked control panel and safety circuit",
        "root_cause": "Faulty door interlock sensor",
        "resolution": "Replaced the faulty door interlock sensor",
        "cost": 4500,
        "repair_time": "3 hours",
        "urgency": "Critical",
        "technician_notes": "Elevator tested across multiple floors after repair",
    },
]
EQUIPMENT_TYPES = [
    "AC",
    "Generator",
    "Water Pump",
    "Elevator",
]

LOCATIONS = [
    "Engineering Block",
    "Computer Science Block",
    "Library",
    "Administrative Block",
    "Hostel Block A",
    "Hostel Block B",
    "Main Auditorium",
    "Laboratory Building",
]
CASE_TEMPLATES = {
    "AC": AC_CASES,
    "Generator": GENERATOR_CASES,
    "Water Pump": PUMP_CASES,
    "Elevator": ELEVATOR_CASES,
}
def generate_records(number_of_records=250):
    records = []

    for index in range(1, number_of_records + 1):
        equipment_type = random.choice(EQUIPMENT_TYPES)
        template = random.choice(CASE_TEMPLATES[equipment_type])

        record = template.copy()
        record["case_id"] = f"CASE-{index:04d}"
        record["equipment_type"] = equipment_type
        record["equipment_id"] = f"{equipment_type.upper().replace(' ', '-')}-{random.randint(1, 20):02d}"
        record["location"] = random.choice(LOCATIONS)
        record["status"] = "Resolved"

        records.append(record)

    return records
def save_records(records):
    fieldnames = [
        "case_id",
        "equipment_type",
        "equipment_id",
        "location",
        "complaint",
        "symptoms",
        "previous_action",
        "root_cause",
        "resolution",
        "cost",
        "repair_time",
        "urgency",
        "technician_notes",
        "status",
    ]

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
if __name__ == "__main__":
    records = generate_records(250)
    save_records(records)
    print(f"Successfully generated {len(records)} maintenance records.")
    print(f"Saved to: {OUTPUT_FILE}")
