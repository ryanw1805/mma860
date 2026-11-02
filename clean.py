"""Clean the listings dataset while keeping the analysis columns."""

import csv
from pathlib import Path


KEEP_COLUMNS = [
	"id",
	"listing_url",
	"scrape_id",
	"last_scraped",
	"source",
	"host_id",
	"host_name",
	"host_is_superhost",
	"host_identity_verified",
	"host_location",
	"host_about",
	"hosts_time_as_host_years",
	"host_listings_count",
	"calculated_host_listings_count",
	"neighbourhood_cleansed",
	"latitude",
	"longitude",
	"property_type",
	"room_type",
	"accommodates",
	"bedrooms",
	"beds",
	"bathrooms_text",
	"amenities",
	"price",
	"minimum_nights",
	"maximum_nights",
	"has_availability",
	"number_of_reviews",
	"number_of_reviews_ltm",
	"number_of_reviews_l30d",
	"number_of_reviews_ly",
	"first_review",
	"last_review",
	"reviews_per_month",
	"review_scores_rating",
	"review_scores_accuracy",
	"review_scores_cleanliness",
	"review_scores_checkin",
	"review_scores_communication",
	"review_scores_location",
	"review_scores_value",
]

BOOLEAN_COLUMNS = {
	"host_is_superhost",
	"host_identity_verified",
	"has_availability",
}


def clean_listings(
	input_path: str | Path = "listings.csv",
	output_path: str | Path = "listings_clean.csv",
) -> Path:
	"""Write a cleaned listings CSV containing only the selected columns.

	Columns kept:
		id, listing_url, scrape_id, last_scraped, source,
		host_id, host_name, host_is_superhost, host_identity_verified,
		host_location, host_about, hosts_time_as_host_years,
		host_listings_count, calculated_host_listings_count,
		neighbourhood_cleansed, latitude, longitude,
		property_type, room_type, accommodates, bedrooms, beds,
		bathrooms_text, amenities, price, minimum_nights, maximum_nights,
		has_availability, number_of_reviews, number_of_reviews_ltm,
		number_of_reviews_l30d, number_of_reviews_ly, first_review,
		last_review, reviews_per_month, and the 7 review_scores_* columns.

	Raises:
		ValueError: If the input CSV does not contain every required column.
	"""
	input_path = Path(input_path)
	output_path = Path(output_path)

	with input_path.open("r", encoding="utf-8-sig", newline="") as source_file:
		reader = csv.DictReader(source_file)
		input_columns = reader.fieldnames or []
		missing_columns = [
			column for column in KEEP_COLUMNS if column not in input_columns
		]
		if missing_columns:
			raise ValueError(
				"Input CSV is missing required columns: "
				+ ", ".join(missing_columns)
			)

		with output_path.open("w", encoding="utf-8", newline="") as cleaned_file:
			writer = csv.DictWriter(cleaned_file, fieldnames=KEEP_COLUMNS)
			writer.writeheader()
			for row in reader:
				cleaned_row = {column: row[column] for column in KEEP_COLUMNS}
				for column in BOOLEAN_COLUMNS:
					if cleaned_row[column] in {"t", "f"}:
						cleaned_row[column] = "1" if cleaned_row[column] == "t" else "0"
				writer.writerow(cleaned_row)

	return output_path


if __name__ == "__main__":
	clean_listings()