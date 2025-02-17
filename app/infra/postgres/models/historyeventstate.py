from tortoise import Model, fields


class HistoryEventState(Model):
    justification = fields.TextField()
    user_email = fields.CharField(max_length=255)
    state = fields.ForeignKeyField("models.State", related_name="state")
    event = fields.ForeignKeyField("models.Event")
    created_at = fields.DatetimeField(auto_now_add=True)
