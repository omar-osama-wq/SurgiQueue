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