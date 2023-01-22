from tortoise import Model, fields

class Hidden: # type hint
    pass

class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(50)
    osu_id = fields.IntField()
    rank = fields.IntField()
    recommended_maps = fields.JSONField(default=[])
    language = fields.CharField(10, default="en")

    def __str__(self) -> str:
        return f"{self.name} ({self.osu_id}, #{self.rank})"

    def __repr__(self) -> str:
        return f"<User {self.name} ({self.osu_id}, #{self.rank})>"