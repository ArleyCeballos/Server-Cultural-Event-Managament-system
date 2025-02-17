from tortoise import Model, fields


class ContractualMode(Model):
    name = fields.CharField(max_length=255)
    active = fields.BooleanField(default=True)
