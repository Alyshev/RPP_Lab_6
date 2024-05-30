from peewee import *

# Подключение к базе данных
db = SqliteDatabase('my_db.db')


# Определение моделей
class Standard(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db


class FullName(Standard):
    lastName = CharField()
    name = CharField()
    middleName = CharField()

    class Meta:
        db_table = "FullName"


class Characteristics(Standard):
    position = CharField()
    workExperience = IntegerField()

    class Meta:
        db_table = "positions"


def get_fields(table):
    return table._meta.fields.keys()


def table_getter(table):
    match table:
        case "FullName":
            return FullName
        case "Characteristics":
            return Characteristics



TABLES = [FullName, Characteristics]
db.create_tables(TABLES)
