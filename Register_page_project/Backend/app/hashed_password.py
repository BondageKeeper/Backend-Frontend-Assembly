import bcrypt
def hash_password(password: str):
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes,salt)
    return hashed_password.decode("utf-8")

def verify_password(written_password: str,found_password: str):
    db_email = found_password.encode("utf-8")
    current_email = written_password.encode("utf-8")
    is_coincide = bcrypt.checkpw(current_email,db_email)
                           #clean_password     #hash-cipher - sequence is crucial
    return is_coincide
