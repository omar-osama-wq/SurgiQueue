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
        priority_map = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}
        def get_priority_value(patient):
            val = patient.get("urgency_level", 1)
            if isinstance(val, int) or (isinstance(val, str) and val.isdigit()):
                return int(val)
            return priority_map.get(str(val).capitalize(), 1)
        self.priority_list = self.patients.copy()
        self.priority_list.sort(key=get_priority_value, reverse=True)
        return self.priority_list
    def choose_patients(self,available_rooms):
        selected_patients=[]
        for patient in self.priority_list:
            if len(selected_patients)<available_rooms:
                selected_patients.append(patient)
        return selected_patients


