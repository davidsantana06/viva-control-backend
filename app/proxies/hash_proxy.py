from werkzeug.security import check_password_hash, generate_password_hash


class HashProxy:
    @staticmethod
    def hash(password: str) -> str:
        return generate_password_hash(password, method="scrypt", salt_length=16)

    @staticmethod
    def check(password_hash: str, password: str) -> bool:
        return check_password_hash(password_hash, password)
