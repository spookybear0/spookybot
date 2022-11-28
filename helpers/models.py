from tortoise import Model, fields

class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(50)
    osu_id = fields.IntField()
    recent_map_id = fields.IntField()