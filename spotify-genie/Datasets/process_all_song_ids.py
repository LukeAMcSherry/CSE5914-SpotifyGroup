import csv

with open('output.csv', 'w', newline='') as writing_file:

    # Open the CSV file
    with open('/Users/alex/Documents/CSE-5914/CSE5914-SpotifyGroup/spotify-genie/Datasets/track_features.csv', 'r') as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file)

        # Create a CSV writer object
        csv_writer = csv.writer(writing_file)

        # Iterate over each row in the CSV file
        for row in csv_reader:
            # ignore empty lines
            if len(row) > 0:

                # Write the data to the CSV file
                csv_writer.writerow([row[0]])
                print(row[0])  # This will print the spotify song ID that we need

            # If you want to access specific elements within each row, you can do so by index
            # For example, if you want to access the first element in each row:
            # print(row[0])
