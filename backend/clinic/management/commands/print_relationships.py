from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Print a clean relationship map for all models in the clinic app."

    def handle(self, *args, **options):
        app_config = apps.get_app_config("clinic")
        models = sorted(app_config.get_models(), key=lambda m: m.__name__)

        self.stdout.write(self.style.SUCCESS("Clinic Relationship Map"))
        self.stdout.write("=" * 24)

        for model in models:
            self.stdout.write(f"\n{model.__name__}")
            self.stdout.write("-" * len(model.__name__))

            relations_found = False
            for field in model._meta.get_fields():
                if not field.is_relation:
                    continue
                if getattr(field, "auto_created", False) and not field.concrete:
                    continue

                relation_type = field.__class__.__name__
                target_model = getattr(field.related_model, "__name__", "Unknown")
                self.stdout.write(f"  {field.name}: {relation_type} -> {target_model}")
                relations_found = True

            if not relations_found:
                self.stdout.write("  (no explicit relation fields)")
