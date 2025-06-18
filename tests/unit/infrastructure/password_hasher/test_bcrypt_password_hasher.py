from infrastrcuture.password_hasher.bcrypt_password_hasher import (
    BcryptPasswordHasher,
)


class TestBcryptPasswordHasher:
    def test_hash_and_verify_success(self):
        hasher = BcryptPasswordHasher()
        password = "s3cret!"
        hashed = hasher.hash(password)
        assert isinstance(hashed, str)
        assert hasher.verify(password, hashed)

    def test_verify_wrong_password(self):
        hasher = BcryptPasswordHasher()
        password = "s3cret!"
        hashed = hasher.hash(password)
        assert not hasher.verify("wrong", hashed)

    def test_hash_is_different_each_time(self):
        hasher = BcryptPasswordHasher()
        password = "s3cret!"
        hash1 = hasher.hash(password)
        hash2 = hasher.hash(password)
        assert hash1 != hash2
