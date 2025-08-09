from django.core.management.base import BaseCommand, CommandError
from dashboard.models import Claim, ClaimDetail
import argparse;
import json;
# from dashboard.models.*;

class Command(BaseCommand):
    help = "Load claim data from JSON"
    def add_arguments(self, parser):
        parser.add_argument("claim_list", type=argparse.FileType('r'))
        parser.add_argument("claim_details", type=argparse.FileType('r'))

    def handle(self, *args, **options):
        self.stdout.write(
                'Loading...'
            )
        claims = json.load(options["claim_list"])
        details = json.load(options["claim_details"])
        updated = 0
        for claim in claims:
            (_, created) = Claim.objects.update_or_create(id=claim["id"], defaults=claim)
            if created:
                updated += 1
        for detail in details:
            (_, created) = ClaimDetail.objects.update_or_create(id=detail["id"], defaults=detail)
            if created:
                updated += 1
        if updated > 0:
            self.stdout.write(
                self.style.WARNING('%s claims or claim details were updated.' % updated)
            )
        self.stdout.write(
                self.style.SUCCESS('Successfully loaded claims.')
            )