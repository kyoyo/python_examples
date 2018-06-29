from peewee import *
from datetime import date

db = SqliteDatabase("person.db")


class Person(Model):
    name = CharField()
    birthday = DateField()

    class Meta:
        database = db

class Pet(Model):
    owner = ForeignKeyField(Person,backref='pets')
    name = CharField()
    animal_type = CharField()

    class Meta:
        database = db



db.connect()

if __name__ == '__main__':

    #drop tables
    db.drop_tables([Person,Pet])

    #create tables
    db.create_tables([Person,Pet])




    #===================insert single data
    # uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15))
    # uncle_bob.save() # bob is now stored in the database
    #
    # grandma = Person.create(name='Grandma', birthday=date(1935, 3, 1))
    # grandma.save()
    #
    # herb = Person.create(name='Herb', birthday=date(1950, 5, 5))
    # herb.save()
    #
    # bob_kitty = Pet.create(owner=uncle_bob, name='Kitty', animal_type='cat')
    # herb_fido = Pet.create(owner=herb, name='Fido', animal_type='dog')
    # herb_mittens = Pet.create(owner=herb, name='Mittens', animal_type='cat')
    # herb_mittens_jr = Pet.create(owner=herb, name='Mittens Jr', animal_type='cat')





    #===================insert many data   it's slow
    # data_source_person = [
    #                           {'name':'Bob','birthday':date(1960, 1, 15)},
    #                           {'name':'Grandma','birthday':date(1935, 3, 1)},
    #                           {'name':'Herb','birthday':date(1950, 5, 5)}
    #                       ]
    #
    # for person_dict in data_source_person:
    #     Person.create(**person_dict)
    #
    # uncle_bob = Person.select().where(Person.name == 'Bob').get()
    # herb = Person.select().where(Person.name == 'Herb').get()
    #
    # data_source_pet = [
    #                       {'owner':uncle_bob,'name': 'Kitty','animal_type':'cat'},
    #                       {'owner':herb,'name': 'Fido','animal_type':'dog'},
    #                       {'owner':herb,'name': 'Mittens','animal_type':'cat'},
    #                       {'owner':herb,'name': 'Mittens Jr','animal_type':'cat'}
    #                   ]
    #
    # for pet_dict in data_source_pet:
    #     Pet.create(**pet_dict)


    #===================insert many data   This is much faster.
    # data_source_person = [
    #     {'name':'Bob','birthday':date(1960, 1, 15)},
    #     {'name':'Grandma','birthday':date(1935, 3, 1)},
    #     {'name':'Herb','birthday':date(1950, 5, 5)}
    # ]
    #
    #
    # with db.atomic():
    #     for person_dict in data_source_person:
    #         Person.create(**person_dict)
    #
    # uncle_bob = Person.select().where(Person.name == 'Bob').get()
    # herb = Person.select().where(Person.name == 'Herb').get()
    #
    # data_source_pet = [
    #     {'owner':uncle_bob,'name': 'Kitty','animal_type':'cat'},
    #     {'owner':herb,'name': 'Fido','animal_type':'dog'},
    #     {'owner':herb,'name': 'Mittens','animal_type':'cat'},
    #     {'owner':herb,'name': 'Mittens Jr','animal_type':'cat'}
    # ]
    #
    # with db.atomic():
    #     for pet_dict in data_source_pet:
    #         Pet.create(**pet_dict)



    #===================insert many data   Fastest.
    # data_source_person = [
    #     {'name':'Bob','birthday':date(1960, 1, 15)},
    #     {'name':'Grandma','birthday':date(1935, 3, 1)},
    #     {'name':'Herb','birthday':date(1950, 5, 5)}
    # ]
    #
    #
    # Person.insert_many(data_source_person).execute()
    #
    # uncle_bob = Person.select().where(Person.name == 'Bob').get()
    # herb = Person.select().where(Person.name == 'Herb').get()
    #
    # data_source_pet = [
    #     {'owner':uncle_bob,'name': 'Kitty','animal_type':'cat'},
    #     {'owner':herb,'name': 'Fido','animal_type':'dog'},
    #     {'owner':herb,'name': 'Mittens','animal_type':'cat'},
    #     {'owner':herb,'name': 'Mittens Jr','animal_type':'cat'}
    # ]
    #
    # Pet.insert_many(data_source_pet).execute()

    #===================insert many data   using tuples.
    fields = [Person.name,Person.birthday]

    data  = [
        ('Bob',date(1960, 1, 15)),
        ('Grandma',date(1935, 3, 1)),
        ('Herb',date(1950, 5, 5)),
    ]

    Person.insert_many(data,fields=fields).execute()


    fields = [Pet.owner,Pet.name,Pet.animal_type]

    uncle_bob = Person.select().where(Person.name == 'Bob').get()
    herb = Person.select().where(Person.name == 'Herb').get()
    data  = [
        (uncle_bob,'Kitty','cat'),
        (herb,'Fido','dog'),
        (herb,'Mittens','cat'),
        (herb,'Mittens Jr','cat')
    ]

    Pet.insert_many(data,fields=fields).execute()




    db.close()