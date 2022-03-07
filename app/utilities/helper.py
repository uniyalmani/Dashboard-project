from jose import JWTError, jwt
 #for creating and veryfing jwt tocken
from passlib.context import CryptContext 
#for hasing password
from datetime import datetime, timedelta
print("inside helper ")

passlib_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#for verify password
def verify_password(plain_password, hashed_password):
    return passlib_context.verify(plain_password, hashed_password)

#for hashing password   
def hash_password(password):
    return passlib_context.hash(password)

#for creating jwt token
def create_jwt_token(data, expire_time):
    to_encode = data.copy()
    expire_at = datetime.utcnow() + expire_time
    to_encode.update({"expire_at":expire_at})
    token = jwt.encode(to_encode, os.getenv(SECRET_KEY), algorithm=os.getenv(ALGORITHM))        
    return encoded_jwt

