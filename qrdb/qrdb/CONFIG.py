# Years for which students are allowed to write reviews, and corresponding year ints
# Must be in the form "(N-1)-N"
AVAILABLE_YEARS = ['2020-2021', '2019-2020', '2018-2019']

RATING_CHOICES = ['Awful', 'Poor', 'Adequate', 'Good', 'Amazing']
RATING_COLORS = {'Awful': '#e85252', 'Poor': "#e58e53", 'Adequate': "#e5da53", "Good": "#8acc44", "Amazing": "#6eb246"}

FLOOR_NAMES = [('G', 'Ground Floor'), ('1', '1st Floor'), ('2', '2nd Floor'), ('3', '3rd Floor'), ('4', '4th Floor')]

# Not used (they were in the incomplete form implementation)
GYP_FREQUENCY_CHOICES = ['Never', 'Rarely', 'Usually', 'Almost always', 'Always']
ENABLE_GYP_FREEZER_QUESTION = True
GYP_FREEZER_QUESTION_CHOICES = ['Yes (eg. fridge had a freezer compartment)', 'No', 'No, but I really wish I did']

CONTACT_EMAIL = 'jcr-accommodatio'

# Analytics, using plausible.js
USE_PLAUSIBLE = True
PLAUSIBLE_SRC = "https://stats.mxbi.net/js/pla.js"