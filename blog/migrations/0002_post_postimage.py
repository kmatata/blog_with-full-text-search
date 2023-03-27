# Generated by Django 4.1 on 2023-03-25 09:12

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="postImage",
            field=models.ImageField(
                blank=True,
                default=None,
                null=True,
                upload_to=blog.models.blog_image_dir_path,
            ),
        ),
    ]
