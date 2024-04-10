import csv

unique_album_names = set()

with open('/Users/alex/Documents/SpotifyFeatureExtractor/Spotify-Recommendation-System/1M_unique_processed_data.csv', 'r') as input_file:
    with open('unique_album_names_filtered.csv', 'w', newline='') as output_file:
        reader = csv.reader(input_file)
        writer = csv.writer(output_file)
        
        next(reader)
        
        for row in reader:
            # Extract the features we need
            artist_name = row[0].strip()
            album_name = row[6].strip()
            artist_popularity = row[-2].strip()
            artist_popularity = int(artist_popularity, base=10)
            track_popularity = row[-3].strip()
            track_popularity = int(track_popularity, base=10)
            
            if(artist_popularity >= 10):
                unique_album_names.add(artist_name +" - "+album_name)
            
        for album in unique_album_names:
            # Write the last element to the new CSV file
            writer.writerow([album])