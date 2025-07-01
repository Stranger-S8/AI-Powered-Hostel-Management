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
        id = self.db.collection(col_name.strip()).where(key.strip(), '==', value).get()[0].id
        
        return id
        
    def count_users(self):
        user_ref = self.db.collection('users')
        count_query = user_ref.count()
        result = count_query.get()
        count = result[0][0].value

        return int(count)
    
    def validate_email(self, input_str):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        
        return re.match(pattern, input_str) is not None
            
    def user_exists(self, username=None, email=None):
        if username is not None:
            users = self.db.collection('users').where('username', '==', username.strip()).get()
        
        if email is not None:
            users = self.db.collection('users').where('email', '==', email.strip()).get()
            
        return len(users) > 0
    
    def get_field(self, collection, key, value, required):
        field = self.db.collection(collection).where(key, "==", value).get()[0]
        
        return field.to_dict().get(required)
    
    def change_user_password(self, password, username=None, email=None):
        print(username, email, password)

        if username is not None:
            doc_id = self.get_doc_id("users", "username", username.strip())
            if doc_id:
                self.db.collection("users").document(doc_id).update({
                    "password": password
                })

        if email is not None:
            doc_id = self.get_doc_id("users", "email", email.strip())
            if doc_id:
                self.db.collection("users").document(doc_id).update({
                    "password": password
                })

        print("Password Changed Successfully")

    def add_user(self, name, email, password):
        count = self.count_users()
        self.db.collection('users').document(f"user_{count + 1}").set(
            {
             "username" : f"{name.strip()}",
             "email" : f"{email.strip()}",
             "password" : f"{password.strip()}"
            }
        )
        
        print(f"User_{count + 1} Added")

    def login_user(self, name, password):
        result = self.db.collection("users") \
            .where("username", "==", name.strip()) \
            .where("password", "==", password.strip()) \
            .get()
        
        if result:
            return True
        else:
            return False
    
    def count_tenants(self):
        ten_ref = self.db.collection('tenants')
        count_query = ten_ref.count()
        result = count_query.get()
        count = result[0][0].value

        return int(count)
    
    def add_tenant(self, id, name, t_type, email, phone, date, ac, sleep, smoking, room):
        count = self.count_tenants()
        self.db.collection('tenants').document(f"ten_{count + 1}").set(
            {
            "id" : int(id),
            "name" : f"{name.strip()}",
            "type" : f"{t_type.strip()}",
            "email" : f"{email.strip()}",
            "phone" : f"{phone.strip()}",
            "room" : f"{room.strip()}",
            "date" : f"{date.strip()}",
            "ac" : f"{ac.strip()}",
            "sleep_time" : f"{sleep.strip()}",
            "smoking" : f"{smoking.strip()}",
            "status" : "active"
            }
        )
        
        print(f"Tenant_{count + 1} Added")
    
    def get_tenant_s_details(self, ten_id, key=None):
        ten_doc = self.get_doc_id("tenants", "id", int(ten_id))
        doc_ref = self.db.collection("tenants").document(ten_doc).get()
        
        if doc_ref:
            doc = doc_ref.to_dict()
            
        if key is not None:
            return doc.get(key.strip())
        else:
            return doc
    
    def room_exists(self, room):
        rooms = self.db.collection('rooms').where('room_no', '==', room).get()
        
        return len(rooms) > 0
    
    def count_rooms(self, d_board=False):
        if not d_board:
            room_ref = self.db.collection('rooms')
        else:
            room_ref = self.db.collection('rooms').where("status", "==", "Occupied")
        count_query = room_ref.count()
        result = count_query.get()
        count = result[0][0].value
            
        return int(count)
    
    def add_room(self, room_no, floor, capacity, ac, status):
        count = self.count_rooms()
        self.db.collection('rooms').document(f"room_{count + 1}").set({
            "room_no" : room_no.strip(),
            "floor" : floor.strip(),
            "capacity" : int(capacity),
            "ac" : ac,
            "status" : status.strip()
            }
        )
        
        print(f"Room_{count + 1} Added")
    
    def get_rooms(self):
        room_refs = self.db.collection('rooms')
        rooms = room_refs.stream()
        
        available = [
            doc.to_dict().get('room_no')
            for doc in rooms
            if doc.to_dict().get('status') not in ["Occupied", "Under Maintenance"]
        ]
        
        return available
    
    def get_tenants_details(self, ten_id=None, one_tenant=False):
        
        tenant_refs = self.db.collection('tenants')
        
        if not one_tenant:
            tenants = tenant_refs.stream()
            
            tenants_data = []
            
            for doc in tenants:
                data = doc.to_dict()
                info = (data.get('id'), 
                        data.get('name'),
                        data.get('room'),
                        data.get('type'),
                        data.get('date'),
                        data.get('status')
                        )
            
                tenants_data.append(info)
        
        else:
            data = self.db.collection('tenants').where("id", "==", int(ten_id.strip())).get()[0].to_dict()
            
            tenants_data = (data.get('id'), 
                        data.get('name'),
                        data.get('room'),
                        data.get('type'),
                        data.get('status'),
                        data.get('phone'),
                        data.get('email'),
                        data.get('date'),
                        data.get('ac'),
                        data.get('sleep_time'),
                        data.get('smoking')
                        )
            
        return tenants_data
    
    def get_rooms_details(self, room_no=None, edit=False):
        if not edit:
            room_refs = self.db.collection('rooms')
            rooms = room_refs.stream()
            
            rooms_data = []
            
            for doc in rooms:
                data = doc.to_dict()
                info = (data.get('room_no'), 
                        data.get('floor'),
                        data.get('capacity'),
                        data.get('ac'),
                        data.get('status')
                        )
            
                rooms_data.append(info)
        else:
            rooms_data = self.db.collection('rooms').where('room_no', '==', room_no.strip()).get()[0].to_dict()
            rooms_data = (rooms_data.get('room_no'), 
                          rooms_data.get('floor'),
                          rooms_data.get('capacity'),
                          rooms_data.get('ac'),
                          rooms_data.get('status')
                        )
            
        return rooms_data
    
    def delete_document(self, collection, key, value):
        try:
            result = self.db.collection(collection).where(key.strip(), '==', value).get()
            self.db.collection(collection).document(result[0].id).delete()
            print(f"Document '{result[0].id}' deleted successfully from {collection} ")
            return True
        except Exception as e:
            print("Error Deleting Document", e)
            return False
    
    def update_room_details(self, doc_id, room_no, floor, capacity, ac, status):
        self.db.collection('rooms').document(doc_id.strip()).set({
            "room_no" : room_no.strip(),
            "floor" : floor.strip(),
            "capacity" : int(capacity),
            "ac" :  ac,
            "status" : status.strip()
        }
        )
        
        print(f"Room Data with {doc_id} is updated")
    
    def save_mess_menu(self, week_menu):
        self.db.collection("mess").document("strange_menu").set(week_menu)
        
        print("Menu Saved Successfully")
    
    def get_mess_data(self):
        today_date = str(date.today())
        
        doc = self.db.collection("messAttendance").document(today_date).get()
        mess_data = doc.to_dict() or {} 
        
        new_list = []

        for ten_id, attendance in mess_data.items():
            try:
                ten_name = self.get_tenant_s_details(ten_id, "name")
            except Exception as e:
                ten_name = f"Unknown ({ten_id})"
                print(f"Error fetching tenant name: {e}")

            new_list.append({
                "name": ten_name,
                "attendance": attendance
            })

        return new_list
    
    
    
    
        
        
        
        
        
        
            
              
if __name__ == "__main__":
    app = Database()
    app.get_rooms_details("Z1", True)



