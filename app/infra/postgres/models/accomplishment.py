from tortoise import Model, fields


class Accomplishment(Model):
    date = fields.DatetimeField(auto_now_add=True)
    compliment_date = fields.DatetimeField(null=True)
    file_url = fields.CharField(max_length=255, null=True)
    text = fields.TextField(null=True)
    check = fields.BooleanField(default=False)
