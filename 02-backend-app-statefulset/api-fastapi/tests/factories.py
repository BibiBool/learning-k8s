"""
UserFactory class using FactoryBoy
"""
import factory
from factory.Factory import FuzzyChoice, FuzzyDate
from src.main import User

class UserFactory(factory.Factory):
    """ Creates fake users """

    class Meta:
        model = User
    
    id = factory.Sequece(lambda n: n)
    name = factory.Faker('name')
    email = factory.Faker('email')
