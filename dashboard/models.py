from django.db import models

# Create your models here.
class Claim(models.Model):
    class ClaimStatus(models.TextChoices):
        DENIED="Denied",
        UNDER_REVIEW="Under Review",
        PAID="Paid",
    id = models.PositiveIntegerField(primary_key = True)
    patient_name = models.CharField(max_length = 30)
    billed_amount = models.PositiveBigIntegerField()
    paid_amount = models.PositiveBigIntegerField()
    status = models.CharField(
        max_length = 12,
        choices = ClaimStatus.choices,
        default = ClaimStatus.UNDER_REVIEW
        )
    insurer_name= models.CharField(max_length=50)
    discharge_date = models.DateField()
    def has_flag(self):
        return ClaimNote.objects.filter(claim_id = self.id, is_review_flag = True).exists()
            

class ClaimDetail(models.Model):
    claim = models.ForeignKey(to = Claim, on_delete = models.CASCADE)
    denial_reason = models.CharField(max_length = 100)
    cpt_codes = models.CharField(max_length = 50)
    def split_cpt_codes(self):
        return self.cpt_codes.split(',')

class ClaimNote(models.Model):
    claim = models.ForeignKey(to = Claim, on_delete=models.CASCADE)
    content = models.TextField()
    is_review_flag = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    # TODO Associated User ID
