from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='transaction_type',
            new_name='type',
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='transaction_date',
            new_name='date',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='title',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='updated_at',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='category',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['-date', '-created_at']},
        ),
    ]
