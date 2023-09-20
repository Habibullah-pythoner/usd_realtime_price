from django.db import models

# Create your models here.
class prices(models.Model):
    id = models.DecimalField(max_digits=20, decimal_places=0, primary_key=True)
    cur = models.CharField(max_length=20, null=True)
    sell = models.CharField(max_length=20)  # Assuming a reasonable max length for the sell value
    buy = models.CharField(max_length=20)   # Assuming a reasonable max length for the buy value
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ID: {self.id}, Currency: {self.cur}, Sell: {self.sell}, Buy: {self.buy}, Date Added: {self.date_added}"