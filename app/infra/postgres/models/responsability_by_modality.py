from tortoise import Model, fields


class ResponsabilityByMode(Model):
    applies = fields.BooleanField(default=True)
    responsability = fields.ForeignKeyField(
        "models.Responsability", related_name="responsability"
    )
    space = fields.ForeignKeyField("models.Space", related_name="space")
    mode = fields.ForeignKeyField("models.ContractualMode", related_name="mode")
