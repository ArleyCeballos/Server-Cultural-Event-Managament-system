from tortoise import Model, fields


class CloseEvent(Model):
    assistant_total = fields.IntField(null=True)
    started_on_time = fields.BooleanField(default=False)
    finished_on_time = fields.BooleanField(default=False)
    situations_with_the_organizer = fields.TextField(null=True)
    situations_with_the_public = fields.TextField(null=True)
    situations_with_ambulance = fields.TextField(null=True)
    inspections = fields.TextField(null=True)
    logistical_situations = fields.TextField(null=True)
    event = fields.ForeignKeyField("models.Event", related_name="close_event")
