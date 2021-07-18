# Imports
import pandas as pd
import numpy as np
from datetime import datetime
from cleaner import NameCleaner, EmailCleaner, UrlCleaner, AddressCleaner, NumberCleaner

# Config
pd.options.display.max_rows = None
pd.options.display.max_columns = None
pd.options.display.max_colwidth = None
pd.options.display.colheader_justify = "left"

# Instantiate cleaners
name_cleaner = NameCleaner()
email_cleaner = EmailCleaner()
url_cleaner = UrlCleaner()
address_cleaner = AddressCleaner()
number_cleaner = NumberCleaner()

# Read DataFrame
start_time = datetime.now()
df = pd.read_csv("data_raw.csv")

# Remove NaNs
df = df.replace(np.nan, "", regex=True)

# Map cleaners
df = df.apply(name_cleaner.parse, axis=1)
df = df.apply(email_cleaner.parse, axis=1)
df = df.apply(url_cleaner.parse, axis=1)
df = df.apply(address_cleaner.parse, axis=1)
df = df.apply(number_cleaner.parse, axis=1)

# Write DataFrame
columns = [
	"name",
	"name_clean",
	"email",
	"email_clean",
	"number",
	"number_clean",
	"url",
	"url_clean",
	"address",
	"street",
	"suburb",
	"city",
	"state",
	"post_code",
	"country",
	"country_code",
	"name_valid",
	"email_valid",
	"url_valid",
	"number_valid",
	"address_valid"
]
df = df[columns]
df.to_csv("data_clean.csv", index=False)

# Performance metrics
time_taken = (datetime.now() - start_time).total_seconds()
time_per_row = time_taken/df.shape[0]
print("Total run time (s):", time_taken)
print("Time per row (s):  ", time_per_row)


