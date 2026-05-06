from io import StringIO

from django.core.management import call_command
from django.test import TestCase


class PrintRelationshipsCommandTests(TestCase):
    def test_prints_relationship_map(self):
        out = StringIO()
        call_command("print_relationships", stdout=out)
        output = out.getvalue()
        self.assertIn("Clinic Relationship Map", output)
        self.assertIn("Patient", output)
        self.assertIn("Appointment", output)
        self.assertIn("Clinician", output)
        self.assertIn("ForeignKey", output)
        self.assertIn("ManyToManyField", output)
