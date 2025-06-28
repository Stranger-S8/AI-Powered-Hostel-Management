import firebase_admin
from firebase_admin import credentials, firestore
import warnings
import re
from datetime import date

warnings.filterwarnings(
    "ignore",
    message="Detected filter using positional arguments",
    category=UserWarning
)

class Database:
    def __init__(self):
        if not firebase_admin._apps:
            creds = credentials.Certificate("data/keys/firebase_config.json")
            firebase_admin.initialize_app(creds)
        self.db = firestore.client()
    
    def get_doc_id(self, col_name, key, value):
        id = self.db.collection(col_name.strip()).where(key.strip(), '==', value).get()
        
        if not id:
            return None
        
        return id[0].id
    
    def validate_tenant(self, ten_id):
        tenant = self.db.collection('tenants').where("id", "==", int(ten_id)).stream()
        tenant = list(tenant)
        
        return len(tenant) > 0
    
    def signup_tenant(self, ten_id, password):
        doc_id = self.get_doc_id("tenants", "id", ten_id)
        
        if doc_id:
            print(doc_id)  
            tenant_ref = self.db.collection("tenants").document(doc_id)
            tenant_ref.update({
                "password" : password.strip()
            })
            
            return True
        else:
            return False
    
    def login_tenant(self, ten_id, password):
        tenants = self.db.collection("tenants")\
            .where("id", "==", ten_id)\
            .where("password", "==", password.strip())\
            .get()
            
        return len(tenants) > 0
    
    def get_tenant_details(self, ten_id, key=None):
        ten_doc = self.get_doc_id("tenants", "id", int(ten_id))
        doc_ref = self.db.collection("tenants").document(ten_doc).get()
        
        if doc_ref:
            doc = doc_ref.to_dict()
            
        if key is not None:
            return doc.get(key.strip())
        else:
            return doc
    
    def get_all_room_details(self, room_no):
        doc_id = self.get_doc_id("rooms", "room_no", room_no)
        rooms_data = self.db.collection("rooms").document(doc_id).get()
        
        if rooms_data:
            doc = rooms_data.to_dict()
            return doc
    
    def get_room_details(self, ten_id):
        room = self.get_tenant_details(ten_id, "room")
        room_data = self.get_all_room_details(room)
        
        return room_data
    
    def get_room_tenant_details(self, ten_id, room):
        tenants = self.db.collection("tenants")\
            .where("id", "==", int(ten_id))\
            .where("room", "==", room)\
            .get()
            
        data = []
        
        if tenants:
            for i in tenants:
                doc = i.to_dict()
                data.append(
                (doc.get("id"),
                doc.get("name"),
                doc.get("phone"),
                doc.get("type")
                )
                )
        
        return data
    
    def get_menu_data(self):
        data = self.db.collection("mess").document("strange_menu").get()
        
        if data:
            data = data.to_dict()
        
        day_order = ["monday", "tuesday", "wednesday", "thursday", "friday"]
        new_dict = {day.capitalize() : data[day] for day in day_order if day in data}
        
        return new_dict
    
    def save_tenant_attendance(self, ten_id, bf, ln, dn):
        today_date = str(date.today())
        
        data = self.db.collection("messAttendance").document(today_date).get()
        
        if not data.exists:
            self.db.collection("messAttendance").document(today_date).set({
                f"{ten_id}" : {"breakfast" : bf, "lunch" : ln, "dinner" : dn}
            })
        else:
            data = data.to_dict()
            
            if ten_id not in data:
                self.db.collection("messAttendance").document(today_date).set({
                    f"{ten_id}" : {"breakfast" : bf, "lunch" : ln, "dinner" : dn}
                })
            
        print(f"{today_date} Attendance is Saved")
        
    
    
        
        
        
        
            
            
            
        
        
        
         
            
    
    