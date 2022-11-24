from tortoise import Model, fields

class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(50)