"""tweet_scraper.py: A simple script to scrape tweets via phrases/hashtag. """

import csv
import argparse
import os
import tweepy

def scrape(hashtags, n, consumer_keys, access_keys, file_name):
    """
    Scrapes tweet data from Twitter's API via tweepy module.

    Parameters:
        hashtags: string of hashtags or phrases to search for (e.g., "#SPACEX AND NASA")
        n: number of tweets to scrape
        consumer_keys: tuple where first element is consumer key and second is consumer secret key
        access_keys: tuple where first element is access token and second is access secret token

    Returns:
        Nothing. Tweets are written to a csv file.

    """

    # Create authentication object
    auth = tweepy.OAuthHandler(consumer_keys[0], consumer_keys[1])
    auth.set_access_token(access_keys[0], access_keys[1])

    # Create tweepy API object
    api = tweepy.API(auth)

    # Write data into the data directory
    os.chdir('.\data')

    print("Scraping...")
    with open(file_name, 'w', newline='', encoding='utf8') as file:
        file = csv.writer(file)

        # Headers
        file.writerow(['Timestamp', 'User', 'Num Followers', 'Hashtags', 'Tweet Text'])

        tweets = tweepy.Cursor(api.search, q=hashtags + '-filter:retweets', lang='en', tweet_mode='extended').items(n)

        try:
            for tweet in tweets:
                # Gather all the desired data
                timestamp = tweet.created_at
                user = tweet.user.screen_name
                num_followers = tweet.user.followers_count
                tags = [hashtag['text'] for hashtag in tweet._json['entities']['hashtags']]
                text = tweet.full_text.replace('\n', ' ')

                # Write this tweet to a row
                file.writerow([timestamp, user, num_followers, tags, text])

        except tweepy.TweepError as e:
            print(e.reason)

if __name__ == '__main__':
    # Create command-line argument parser and mandatory arguments
    parser = argparse.ArgumentParser(description="Scrape tweets using specified hashtags or phrases.")
    parser.add_argument('-n', '--num_tweets', type=int, metavar='', required=True, help="Number of tweets to scrape")
    parser.add_argument('-p', '--phrase', type=str, metavar='', required=True,
                        help="Hashtags/phrases to search for (e.g., \"#SPACEX AND elon musk\")")
    parser.add_argument('-f', '--file_name', type=str, metavar='', required=False, default="twitter_data.csv",
                        help="Name of CSV file to create. Default is twitter_data.csv")

    args = parser.parse_args()

    # The 4 API keys should be stored in environmental variables with these names
    key1 = os.environ.get("TWITTERCONSUMER")
    key2 = os.environ.get("TWITTERCONSUMER2")
    key3 = os.environ.get("TWITTERACCESS")
    key4 = os.environ.get("TWITTERACCESS2")

    # If keys weren't found in environments, request
    if key1 is None: key1 = input("Enter consumer API key: ")
    if key2 is None: key2 = input("Enter consumer secretAPI key: ")
    if key3 is None: key3 = input("Enter access API key: ")
    if key4 is None: key4 = input("Enter secret access API key: ")

    scrape(args.phrase, args.num_tweets, (key1, key2), (key3, key4), args.file_name)
