import csv

NEEDCHECK = "needCheck.csv"
POSSIBILITIES = "possibilities.csv"


# adds any good possible inventory to possibilities.csv
def addToPossibilities(search, price, breakeven, url):
    with open(POSSIBILITIES, "a", newline="") as csv_file:
        # Create a CSV writer
        csv_writer = csv.writer(csv_file)

        # Write the new row
        csv_writer.writerow([search, price, breakeven, url])


# if a listing might be good but might also be a waste of time, add to needCheck.csv
def addToCheck(title, price, url):
    with open(NEEDCHECK, "a", newline="") as csv_file:
        # Create a CSV writer
        csv_writer = csv.writer(csv_file)

        # Write the new row
        csv_writer.writerow([title, price, url])
