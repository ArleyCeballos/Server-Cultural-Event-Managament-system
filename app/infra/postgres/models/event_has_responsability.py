from tortoise import Model, fields


class EventHasResponsability(Model):
    accomplishment = fields.ForeignKeyField(
        "models.Accomplishment", related_name="accomplishment"
    )
    responsability_by_mode = fields.ForeignKeyField(
        "models.ResponsabilityByMode", null=True
    )
    event = fields.ForeignKeyField("models.Event")
    specific_responsability = fields.ForeignKeyField(
        "models.SpecificResponsability",
        null=True,
        related_name="specific_responsability",
    )
