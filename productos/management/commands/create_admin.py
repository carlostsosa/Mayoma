from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Crea el usuario admin por defecto"

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@mayoma.com", "admin123")
            self.stdout.write(self.style.SUCCESS("Usuario admin creado: admin / admin123"))
        else:
            self.stdout.write("El usuario admin ya existe")
