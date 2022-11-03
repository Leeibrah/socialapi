from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password with Bcrypt
def hash_password(password: str):

    return pwd_context.hash(password)

# Compare plain and hashed passwords with bcrypt
def verify_hash(plain_password, hashed_password):

    return pwd_context.verify(plain_password, hashed_password)