from tortoise import Model, fields


class EventState(Model):
    justification = fields.TextField()
    event = fields.ForeignKeyField("models.Event")
    state = fields.ForeignKeyField("models.State")
    created_at = fields.DatetimeField(auto_now_add=True)
