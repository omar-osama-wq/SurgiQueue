import json

class surgery_mangment:

    def __init__(self):
        self.patient_f = "patients.json"
        self.surgery_f = "surgeries.json"
        self.total_r = 5
        self.surgeries = self.load_data()


    def load_data(self):
        import os
        if not os.path.exists(self.surgery_f):
            return []
        with open(self.surgery_f, "r") as file:
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
            result+="Patient ID :"+ surgery["patient_id"]+"\n"
            result+="Patient :"+ surgery["patient_name"]+"\n"
            result+="Diagnosis :"+ surgery["diagnosis"]+"\n"
            result+="Urgency :"+ surgery["urgency_level"]+"\n"
            result+="Doctor :"+ surgery["doctor"]+"\n"
            result+="Surgery Type :"+ surgery["surgery_type"]+"\n"
            result+="Date :"+ surgery["date"]+"\n"
            result+="Room :"+ str(surgery["room"])+"\n"
            result+="Status :"+ surgery["status"]+"\n"
            result+="-" * 40
        return result


    def delete_surgery(self, patient_name):
        for surgery in self.surgeries:
            if surgery["patient_name"] == patient_name:
                self.surgeries.remove(surgery)
                self.save_data()
                return "Surgery Deleted Successfully"
        return "Surgery Not Found"

    def complete_surgery(self):
        id=input("Enter patient ID: ").strip().upper()
        for surgery in self.surgeries:
            if surgery["patient_id"]==id:
                surgery["status"] = "Completed"
                self.save_data()
                return"surgery completed successfully"
        return "surgery not found"

    def free_rooms(self):
        rooms=self.a_rooms()
        if len(rooms)==0:
            return"no rooms available"
        result="available rooms"

        for room in rooms:
            result+="Room "+str(room)+"\n"
        return result

    def change_rooms(self):
        self.total_rooms=int(input("Enter new number of rooms: "))
        return "number of rooms updated successfully"