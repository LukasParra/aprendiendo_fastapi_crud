from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["Users"])

class User(BaseModel):
    id : int
    name : str
    surname : str
    age : int

user_list = [User(id=1, name="David", surname="Larrael", age=32),
             User(id=2, name="Luis", surname="Castro", age=22), 
             User(id=3, name="Marisol", surname="Hernandez", age=28)]


def search_user(id : int):
    user = filter(lambda user : user.id == id, user_list)
    try:
        return list(user)[0]
    except IndexError:
        None
    

@router.get("/", response_model=list[User])
async def mostrar_user():
    return list(user_list)

@router.get("/{id}", response_model=User)
async def mostrar_id_user(id : int):
    if search_user(id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="El usuario no existe")
    
    return search_user(id)
    

@router.post("/", response_model=User)
async def create_user(user : User):
    if search_user(user.id) is not None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="El usuario ya existe")
    
    user_list.append(user)
    return user
    
@router.put("/", response_model=User)
async def update_user(user : User):

    found = False

    for index, saved_user in enumerate(user_list):
        if saved_user.id == user.id:
            user_list[index] = user
            found = True
            break
        

    if not found:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="El usuario no existe")
    
    return user

@router.delete("/{id}", response_model=User)
async def delete_user(id : int):

    found = False

    for index, saved_user in enumerate(user_list):
        if saved_user.id == id:
            del user_list[index]
            found = True
            return {"message" : "Usuario eliminado"}
    
    if not found:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="El usuario no existe")