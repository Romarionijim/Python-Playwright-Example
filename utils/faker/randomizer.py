from faker import Faker


class Randomizer:
    fake = Faker()

    @classmethod
    def get_random_full_name(cls) -> str:
        name = cls.fake.name()
        return name

    @classmethod
    def generate_Random_name(cls):
        fake_first_name = cls.fake.first_name()
        return fake_first_name

    @classmethod
    def generate_random_lastname(cls):
        fake_lastname = cls.fake.last_name()
        return fake_lastname

    @classmethod
    def get_random_number(cls) -> int:
        random_int = cls.fake.random_int(min=1, max=100)
        return random_int
