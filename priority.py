import json
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
        self.priority_list.sort(key=lambda patient:patient["urgency_level"], reverse=False)
        return self.priority_list
    def choose_patients(self,available_rooms):
        selected_patients=[]
        for patient in self.priority_list:
            if len(selected_patients)<available_rooms:
                selected_patients.append(patient)
        return selected_patients



