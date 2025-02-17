from tortoise import Model, fields


class SpecificResponsability(Model):
    name: str = fields.CharField(max_length=255)
    description: str = fields.TextField()
