# Imports
import nameparser
import phonenumbers
import url_normalize
import validators
import geopy
import pycountry
import numpy as np

# Config
nameparser.config.CONSTANTS.string_format = "{first} {last}"
DEFAULT_COUNTRY_CODE = "AU"
NUMBER_FORMAT = phonenumbers.PhoneNumberFormat.INTERNATIONAL
LOCATION_CONFIDENCE_THRESHOLD = 99 # %

# Validation monads
def success(x): return (True, x)
def failure(x): return (False, x)

# Name cleaner
class NameCleaner:
	def clean(self, name):
		try:
			name_clean = name.lower()
			name_clean = nameparser.HumanName(name_clean)
			name_clean.capitalize()
			if name_clean != "":
				return success(name_clean)
			else:
				return failure(None)
		except:
			return failure(None)

	def parse(self, s):
		(name_valid, name_clean) = self.clean(s["name"])
		s["name_clean"] = name_clean
		s["name_valid"] = name_valid
		return s

# Email cleaner
class EmailCleaner:
	def clean(self, email):
		try:
			email_clean = email.lower()
			if self.validate(email_clean):
				return success(email_clean)
			else:
				return failure(None)
		except:
			return failure(None)

	def validate(self, email):
		is_valid = validators.email(email)
		result = True if is_valid else False
		return result

	def parse(self, s):
		(email_valid, email_clean) = self.clean(s["email"])
		s["email_clean"] = email_clean
		s["email_valid"] = email_valid
		return s

# URL cleaner
class UrlCleaner:
	def clean(self, url):
		try:
			url_clean = url_normalize.url_normalize(url)
			url_clean = url_clean.replace("www.", "")
			if self.validate(url_clean):
				return success(url_clean)
			else:
				return failure(None)
		except:
			return failure(None)

	def validate(self, url):
		is_valid = validators.url(url)
		result = True if is_valid else False
		return result

	def parse(self, s):
		(url_valid, url_clean) = self.clean(s["url"])
		s["url_clean"] = url_clean
		s["url_valid"] = url_valid
		return s

# Uses ArcGIS (API) for geocoding address
class AddressCleaner:
	def __init__(self):
		self.geolocator = geopy.geocoders.ArcGIS()
		self.iso_to_name = {c.alpha_3: c.name for c in pycountry.countries}
		self.iso_to_code = {c.alpha_3: c.alpha_2 for c in pycountry.countries}

	def geolocate(self, address):
		try:
			g = self.geolocator.geocode(address, out_fields="*").raw["attributes"]
			location = {
				"street": g["StAddr"],
				"suburb": g["Nbrhd"],
				"city": g["City"],
				"state": g["Region"],
				"post_code": g["Postal"],
				"country": self.iso_to_name[g["Country"]],
				"country_code": self.iso_to_code[g["Country"]]
			}
			# Confidence threshold
			if int(g["Score"]) >= LOCATION_CONFIDENCE_THRESHOLD:
				return success(location)
			else:
				return failure({})
		except:
			return failure({})

	def parse(self, s):
		(address_valid, location) = self.geolocate(s["address"])
		s["street"] = location.get("street")
		s["suburb"] = location.get("suburb")
		s["city"] = location.get("city")
		s["state"] = location.get("state")
		s["post_code"] = location.get("post_code")
		s["country"] = location.get("country")
		s["country_code"] = location.get("country_code")
		s["address_valid"] = address_valid
		return s

# Depends on AddressCleaner to extract country_code
class NumberCleaner:
	def clean(self, number, country_code=None):
		try:
			if country_code == None:
				country_code = DEFAULT_COUNTRY_CODE
			number_parsed = phonenumbers.parse(number, country_code)
			number_clean = phonenumbers.format_number(number_parsed, NUMBER_FORMAT)
			if self.validate(number_parsed):
				return success(number_clean)
			else:
				return failure(None)
		except:
			return failure(None)

	def validate(self, number_parsed):
		is_valid = phonenumbers.is_valid_number(number_parsed)
		return is_valid

	def parse(self, s):
		(number_valid, number_clean) = self.clean(s["number"], s["country_code"])
		s["number_clean"] = number_clean
		s["number_valid"] = number_valid
		return s