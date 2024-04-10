import csv
import sys
import time
from datetime import datetime
import re

# Now you can import the rym_scraper module
from rymscraper import rymscraper, RymUrl

def format_string(input_string):
    # Replace multiple whitespace characters with a single space
    formatted_string = re.sub(r'\s+', ' ', input_string)
    return formatted_string

# Function to extract review for an album
def extract_review(album_name, network):
    try:
        # Search for the album
        # results = network.get_album_infos(name= album_name)
        review = network.get_album_infos(name= album_name)

        
        # Select the first result
        # first_result = results[0]
        
        # Get the album object
        # album = Album(first_result['url'])
        
        # Get the review
        # review = album.get_review()
        
        return review if review else "Review not found"
    except Exception as e:
        return str(e)
    
# Function to process CSV file and extract reviews
def process_csv(csv_file, network, counter):
    with open(csv_file, 'r') as file:
        with open('output_album_reviews_'+str(datetime.now())+'.csv', 'w') as output:
            with open('/Users/alex/Documents/SpotifyFeatureExtractor/Spotify-Recommendation-System/unique_album_names_counter.csv', 'w') as counter_file_w:
                with open('/Users/alex/Documents/SpotifyFeatureExtractor/Spotify-Recommendation-System/unique_album_names_counter.csv', 'r') as counter_file_r:
 
                    reader = csv.reader(file)
                    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)

                    for bruh in range(counter):  # Skip the first n lines
                        next(reader)
                    for row in reader:
                        print('New row')
                        album_name = row[0]
                        review = extract_review(album_name, network)
                        print(review)

                        print("THE NUMBER:\t"+str(counter))
                        print(review)
                        print('\n')
                        if(review == 'Review not found' or review == 'list index out of range'):
                            writer.writerow(["Review not found for "+album_name])
                        else:
                            review_vals = [re.sub(r'\s+', ' ', str(value)) for value in list(review.values())] 
                            writer.writerow(["counter: "+str(counter)])
                            writer.writerow([review_vals])
                        counter += 1
                            
                        # reader_counter = csv.reader(counter_file_r)
                        # writer_counter = csv.writer(counter_file_w)
                        
                        # counter_existing_data = list(reader_counter)

                        # writer_counter.writerow(str(counter))
                        # # Write the existing data back
                        # writer_counter.writerows(counter_existing_data)
                        
                        # time.sleep(10.0)
                        # print(f"Album: {album_name}\nReview: {review}\n")

    # Main function
def main():
    counter = 0
    network = rymscraper.RymNetwork()
    
    # with open('/Users/alex/Documents/SpotifyFeatureExtractor/Spotify-Recommendation-System/unique_album_names_counter.csv', 'r') as counter_file:
    #     reader = csv.reader(counter_file)
    #     # counter = int(next(reader)[0])
    
    csv_file = '/Users/alex/Documents/SpotifyFeatureExtractor/Spotify-Recommendation-System/unique_album_names.csv'
    process_csv(csv_file, network, counter)

if __name__ == "__main__":
    main()
