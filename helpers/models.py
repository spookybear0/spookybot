from tortoise import Model, fields

class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(50)
    osu_id = fields.IntField()
    rank = fields.IntField()

    def __str__(self):
        return f"{self.name} ({self.osu_id}, #{self.rank})"

    def __repr__(self):
        return f"<User {self.name} ({self.osu_id}, #{self.rank})>"