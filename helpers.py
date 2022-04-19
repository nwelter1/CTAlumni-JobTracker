from fastapi import HTTPException
from sqlalchemy.orm import Session
import crud

def verify_token(db: Session, token: str, user_id: str):
    token = token.split(' ')[1]
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='user does not exist')
    elif token == db_user.token:
        return True
    elif token != db_user.token:
        raise HTTPException(status_code=401, detail="Token is not valid for this user")
    else:
        return False