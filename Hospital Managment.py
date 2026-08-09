import json
import os
class PatientManagement:
    def add_patient(self, patient_id, name, age, diagnosis, urgency_level):
        patient = {
            "patient_id": patient_id,
            "name": name,
            "age": age,
            "diagnosis": diagnosis,
            "urgency_level": urgency_level
        }
        self.patients.append(patient)
        self.save_data()
        return "Patient added"
    def show_patients(self):
        return self.patients
    def update_patient(self, patient_id, name, age, diagnosis, urgency_level):
        for i in self.patients:
            if i["patient_id"] == patient_id:
                i["name"] = name
                i["age"] = age
                i["diagnosis"] = diagnosis
                i["urgency_level"] = urgency_level
                self.save_data()
                return "Patient updated"
        return "Patient not updated"
    def delete_patient(self, patient_id):
        for i in self.patients:
            if i["patient_id"] == patient_id:
                self.patients.remove(i)
                self.save_data()
                return "Patient deleted"
        return "Patient not deleted"
    def search_patient(self, query):
        result = []
        for i in self.patients:
            if query in i["patient_id"] or query in i["name"]:
                result.append(i)
        return result
    def __init__(self, filename="patients.json"):
        self.filename = filename
        self.patients = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                self.patients = json.load(file)
    def save_data(self):
        with open(self.filename, 'w') as file:
            json.dump(self.patients, file, indent=4)
class surgery_mangment:

    def __init__(self):
        self.patient_f = "patients.json"
        self.surgery_f = "surgeries.json"
        self.total_r = 5
        self.surgeries = self.load_data()


    def load_data(self):
        with open(self.surgery_f,"r") as file:
            return json.load(file)

    def save_data(self):
        with open(self.surgery_f,"w") as file:
            json.dump(self.surgeries,file,indent=4)

    def load_patient(self):
        with open(self.patient_f, "r") as file:
            return json.load(file)

    def a_rooms(self):
        busy_rooms=[]
        for surgery in self.surgeries:
            if surgery["status"] == "Scheduled":
                busy_rooms.append(surgery["room"])

        free_room=[]
        for room in range(1,self.total_r+1):
            if room not in busy_rooms:
                free_room.append(room)
        return free_room

    def add_surgery(self):
        id=input("enter patient ID: ").strip().upper()
        patients= self.load_patient()
        patient=0
        for p in patients:

            if p["patient_id"].strip()==id:
                patient = p
                break

        if patient == 0:
            return("Patient Not Found")


        rooms=self.a_rooms()
        if len(rooms)==0:
            return("No available operation rooms")

        room=rooms[0]
        surgery_type=input("Enter surgery type: ")
        doctor=input("Enter doctor name: ")
        date=input("Enter surgery date: ")
        surgery = {

            "patient_id": patient["patient_id"],

            "patient_name": patient["name"],

            "diagnosis": patient["diagnosis"],

            "urgency_level": patient["urgency_level"],

            "doctor": doctor,

            "surgery_type": surgery_type,

            "date": date,

            "room": room,

            "status": "Scheduled"

        }
        self.surgeries.append(surgery)
        self.save_data()
        return f"Surgery Added Successfully\nAssigned Room: {room}"

    def show_surgeries(self):
        if len(self.surgeries)==0:
            return("No surgeries found")


        result="Surgeries"
        for surgery in self.surgeries:
            result+="Patient ID :"+ surgery["patient_id"]
            result+="Patient :"+ surgery["patient_name"]
            result+="Diagnosis :"+ surgery["diagnosis"]
            result+="Urgency :"+ surgery["urgency_level"]
            result+="Doctor :"+ surgery["doctor"]
            result+="Surgery Type :"+ surgery["surgery_type"]
            result+="Date :"+ surgery["date"]
            result+="Room :"+ surgery["room"]
            result+="Status :"+ surgery["status"]
            result+="-" * 40
        return result


    def delete_surgery(self):
        id=input("Enter patient ID: ").strip().upper()
        for surgery in self.surgeries:
            if surgery["patient_id"]==id:
                self.surgeries.remove(surgery)
                self.save_data()
                return("surgery deleted successfully")
        return"surgery not found"

    def complete_surgery(self):
        id=input("Enter patient ID: ").strip().upper()
        for surgery in self.surgeries:
            if surgery["patient_id"]==id:
                surgery["status"] = "Completed"
                self.save_data()
                return"surgery completed successfully"


    def free_rooms(self):
        rooms=self.a_rooms()
        if len(rooms)==0:
            return"no rooms available"
        result="available rooms"

        for room in rooms:
            result+="Room "+str(room)
        return result

    def change_rooms(self):
        self.total_r=int(input("Enter new number of rooms: "))
        return "number of rooms updated successfully"
class priority_Management:
    def __init__(self):
        self.patients=[]
        self.priority_list=[]
    def load_patients(self):
        file=open("patients.json","r")
        self.patients=json.load(file)
        file.close()
    def sort_patients(self):
        self.priority_list=self.patients.copy()
        self.priority_list.sort(key=lambda patient:patient["urgency_level"], reverse=True)
        return self.priority_list
    def choose_patients(self,available_rooms):
        selected_patients=[]
        for patient in self.priority_list:
            if len(selected_patients)<available_rooms:
                selected_patients.append(patient)
        return selected_patients