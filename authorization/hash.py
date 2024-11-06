from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated='auto')

class Hash:
    @staticmethod
    def bcrypt_context(password: str) -> str:
        return pwd_cxt.hash(password)
    
    @staticmethod
    def verify(plain_password: str, hash_password: str) -> bool:
        return pwd_cxt.verify(plain_password, hash_password)
