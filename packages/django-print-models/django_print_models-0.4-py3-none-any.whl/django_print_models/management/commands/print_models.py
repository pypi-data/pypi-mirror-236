from django.core.management.base import BaseCommand
from django.db import models
from importlib import import_module


def print_model_fields(model):
    """
    Prints model definition with *just* the model fields.
    """
    print(f"class {model.__name__}(models.Model):")
    for field in model._meta.get_fields():
        if isinstance(field, models.fields.Field):
            # Add any other field options you care about here
            preserve_opts = (
                "max_length",
                "null",
                "blank",
                "db_index",
                "on_delete",
                "related_name",
            )
            opts = {}
            for opt in preserve_opts:
                if hasattr(field, opt):
                    attr = getattr(field, opt)
                    if attr is not None:
                        opts[opt] = attr

            related_model = None

            # Check if the field has related model (ForeignKey, OneToOneField, ManyToManyField)
            if hasattr(field, "related_model") and field.related_model is not None:
                related_model = field.related_model.__name__

            opts_str = ", ".join(f"{k}={repr(v)}" for k, v in opts.items())
            args_str = f'"{related_model}", ' if related_model else ""
            print(
                f"    {field.name} = models.{type(field).__name__}({args_str}{opts_str})"
            )


class Command(BaseCommand):
    help = """
        Print model definitions with *just* the model fields, no
        other methods etc.
        """

    def add_arguments(self, parser):
        parser.add_argument(
            "app_name", type=str, help="Name of the Django app containing the models."
        )
        parser.add_argument(
            "model_names", nargs="+", type=str, help="Names of the models to print."
        )

    def handle(self, *args, **options):
        app_name = options["app_name"]
        model_names = options["model_names"]

        try:
            models_module = import_module(f"{app_name}.models")
        except ImportError:
            self.stderr.write(f"Models module for app '{app_name}' not found.")
            return

        first = True
        for model_name in model_names:
            model = getattr(models_module, model_name, None)
            if model is None:
                self.stderr.write(f"Model {model_name} not found.")
                continue

            if not first:
                print("")
            first = False

            print_model_fields(model)
