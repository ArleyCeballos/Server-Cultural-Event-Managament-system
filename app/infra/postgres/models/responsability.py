from tortoise import Model, fields


class Responsability(Model):
    name = fields.CharField(max_length=255)
    description = fields.TextField()
    active = fields.BooleanField(default=True)
    template_url = fields.CharField(max_length=255, null=True)
