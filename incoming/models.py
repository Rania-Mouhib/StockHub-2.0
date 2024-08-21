from django.db import models


class Article(models.Model):
    TYPE_CHOICES = [
        ('Type1', 'Type1'),
        ('Type2', 'Type2'),
        # Add more types as needed
    ]

    PLANT_CHOICES = [
        ('BSK1', 'BSK1'),
        ('BSK2', 'BSK2'),
        ('BSK3', 'BSK3'),
        ('BSK4', 'BSK4'),
    ]

    RACK_CHOICES = [
        ('A1', 'A1'), ('A2', 'A2'), ('A3', 'A3'), ('A4', 'A4'), ('A5', 'A5'), ('A6', 'A6'),
        ('B1', 'B1'), ('B2', 'B2'), ('B3', 'B3'), ('B4', 'B4'), ('B5', 'B5'), ('B6', 'B6'),
        ('C1', 'C1'), ('C2', 'C2'), ('C3', 'C3'), ('C4', 'C4'), ('C5', 'C5'), ('C6', 'C6'),
        ('D1', 'D1'), ('D2', 'D2'), ('D3', 'D3'), ('D4', 'D4'), ('D5', 'D5'), ('D6', 'D6'),
        ('E1', 'E1'), ('E2', 'E2'), ('E3', 'E3'), ('E4', 'E4'), ('E5', 'E5'), ('E6', 'E6'),
        ('F1', 'F1'), ('F2', 'F2'), ('F3', 'F3'), ('F4', 'F4'), ('F5', 'F5'), ('F6', 'F6'),
        ('G1', 'G1'), ('G2', 'G2'), ('G3', 'G3'), ('G4', 'G4'), ('G5', 'G5'), ('G6', 'G6'),
        ('H1', 'H1'),
    ]

    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    model = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    vnc = models.BigIntegerField(blank=True, null=True) 
    bci = models.CharField(max_length=100, blank=True, null=True)
    plant = models.CharField(max_length=4, choices=PLANT_CHOICES)
    date_in = models.DateTimeField(auto_now_add=True)
    pilot = models.CharField(max_length=100, blank=True, null=True)
    rack = models.CharField(max_length=2, choices=RACK_CHOICES)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.model} ({self.type})"

