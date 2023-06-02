from fastapi import FastAPI, HTTPException,Query, Request
from models import Request, RequestCreate

app = FastAPI()

# Örnek veritabanı
requests_db = []

users = {
    "admin": {
        "username": "admin",
        "is_admin": True
    },
    "user1": {
        "username": "user1",
        "is_admin": False
    },
    "user2": {
        "username": "user2",
        "is_admin": False
    }
}


@app.get("/")
async def read_root():
    return {"message": "This is a request app"}

# Talep goruntuleme
# Ornek URL: http://localhost:8000/api/v1/requests?username=user2
@app.get("/api/v1/requests")
def get_all_requests(username: str = Query(...)):
    if not user_exists(username):
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")

    if is_admin == True:
        # Admins can see all requests
        return requests_db
    else:
        filtered_requests = [req for req in requests_db if req["created_by"] == username or req["status"] == "onaylandı"]
        return filtered_requests
    
"""""
-Yeni talep oluşturma
-Ornek URL: http://localhost:8000/api/v1/requests?username=user2
-Ornek JSON: {
  "title": "New Request",
  "description": "This is a new request created by user1",
  "created_by": "user1"
}
"""""
@app.post("/api/v1/requests")
def create_request(request: RequestCreate, username: str = Query(...)):
    if not user_exists(username):
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")

    if is_admin(username):
        raise HTTPException(status_code=403, detail="Yalnızca kullanıcılar yeni talepler oluşturabilir.")

    new_request = Request(
        id=len(requests_db) + 1,
        title=request.title,
        description=request.description,
        status="beklemede",
        created_by=username
    )
    requests_db.append(new_request.dict())
    return new_request




# Talep silme
# ornek URL : http://localhost:8000/api/v1/requests/2?username=admin
@app.delete("/api/v1/requests/{request_id}")
def delete_request(request_id: int, username: str = Query(...)):
    if not user_exists(username):
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")

    request = find_request(request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Talep bulunamadı.")

    if is_admin(username) or request["created_by"] == username:
        requests_db.remove(request)
        return {"message": "Talep silindi."}

    raise HTTPException(status_code=403, detail="Sadece admin veya talep sahibi talebi silebilir.")

"""""
 -Talep güncelleme



 """""
@app.put("/api/v1/requests{request_id}")
def update_request(request_id: int, updated_request: Request, username: str = Query(...)):
    if not user_exists(username):
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")

    request = find_request(request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Talep bulunamadı.")

    if request["created_by"] != username:
        raise HTTPException(status_code=403, detail="Sadece talep sahibi talebi güncelleyebilir.")

    request["title"] = updated_request.title
    request["description"] = updated_request.description

    return request

"""""
 -Talep durumu güncelleme
 -Ornek URL: http://localhost:8000/api/v1/requests/1/status?status=onaylandı&username=admin
 -Ornek JSON: {
  "title": "Updated Request Title",
  "description": "Updated description of the request"
}
"""""

@app.put("/api/v1/requests/{request_id}/status")
def update_request_status(request_id: int, status: str, username: str = Query(...)):
    if not user_exists(username):
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")

    if not is_admin(username):
        raise HTTPException(status_code=403, detail="Yalnızca admin talep durumunu güncelleyebilir.")

    request = find_request(request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Talep bulunamadı.")

    request["status"] = status
    return request

    
# Kullanıcı kontrol fonksiyonları
def user_exists(username):
    return username in users

def is_admin(username):
    return users[username]["is_admin"]

# Talep bulma fonksiyonu
def find_request(request_id):
    for request in requests_db:
        if request["id"] == request_id:
            return request
    return None
