# myapp/migrations/0010_alter_storead_options.py
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_chatmessage_reply_to_storead'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='storead',
            options={'managed': False},
        ),
        migrations.AlterModelTable(
            name='storead',
            table='store_ad',
        ),
    ]
