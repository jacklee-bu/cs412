# File: models.py
# Author: Jack Lee (jacklee@bu.edu)
# Date: October 2025
# Description: Models for voter_analytics app to handle Newton voter data

from django.db import models
import csv
from datetime import datetime

class Voter(models.Model):
    """Model representing a registered voter in Newton, MA."""

    # name fields
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)

    # address fields
    street_number = models.CharField(max_length=20)
    street_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=20, blank=True)
    zip_code = models.CharField(max_length=10)

    # voter information
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=2)  # note: 2 chars wide
    precinct_number = models.CharField(max_length=10)

    # voting history for recent elections
    v20state = models.BooleanField(default=False)  # 2020 state election
    v21town = models.BooleanField(default=False)   # 2021 town election
    v21primary = models.BooleanField(default=False)  # 2021 primary
    v22general = models.BooleanField(default=False)  # 2022 general election
    v23town = models.BooleanField(default=False)   # 2023 town election

    # voter participation score (0-5)
    voter_score = models.IntegerField()

    def __str__(self):
        """String representation of the voter."""
        return f"{self.first_name} {self.last_name} - Precinct {self.precinct_number}"

    @property
    def full_address(self):
        """Get the full street address for this voter."""
        # build the address string
        address = f"{self.street_number} {self.street_name}"
        if self.apartment_number:
            address += f" Apt {self.apartment_number}"
        address += f", Newton, MA {self.zip_code}"
        return address


def load_data():
    """Load voter data from the CSV file into the database."""

    # delete existing records to avoid duplicates
    Voter.objects.all().delete()

    # path to the csv file
    filename = 'voter_analytics/newton_voters.csv'

    # list to hold voter objects for bulk create
    voters_to_create = []

    # open and read the CSV file
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        # counter for progress tracking
        count = 0

        for row in reader:
            # parse the dates, handle invalid dates
            try:
                dob = datetime.strptime(row['Date of Birth'], '%Y-%m-%d').date()
            except ValueError:
                # handle invalid dates like 1900-01-00
                dob = datetime.strptime('1900-01-01', '%Y-%m-%d').date()

            try:
                reg_date = datetime.strptime(row['Date of Registration'], '%Y-%m-%d').date()
            except ValueError:
                # handle invalid dates, use a default date
                reg_date = datetime.strptime('1900-01-01', '%Y-%m-%d').date()

            # create voter object
            voter = Voter(
                last_name=row['Last Name'],
                first_name=row['First Name'],
                street_number=row['Residential Address - Street Number'],
                street_name=row['Residential Address - Street Name'],
                apartment_number=row['Residential Address - Apartment Number'],
                zip_code=row['Residential Address - Zip Code'],
                date_of_birth=dob,
                date_of_registration=reg_date,
                party_affiliation=row['Party Affiliation'],
                precinct_number=row['Precinct Number'],
                # convert TRUE/FALSE strings to boolean
                v20state=(row['v20state'] == 'TRUE'),
                v21town=(row['v21town'] == 'TRUE'),
                v21primary=(row['v21primary'] == 'TRUE'),
                v22general=(row['v22general'] == 'TRUE'),
                v23town=(row['v23town'] == 'TRUE'),
                voter_score=int(row['voter_score'])
            )

            # add to list for bulk creation
            voters_to_create.append(voter)

            count += 1
            # print progress every 5000 records
            if count % 5000 == 0:
                print(f"Processed {count} records...")

    # bulk create all voters at once for efficiency
    Voter.objects.bulk_create(voters_to_create)

    print(f"Successfully loaded {count} voter records.")