from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("domain", "0019_remove_project_category_project_categories")]
    operations = [TrigramExtension()]
