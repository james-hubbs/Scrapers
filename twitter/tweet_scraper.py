"""tweet_scraper.py: A simple script to scrape tweets via phrases/hashtag. """

import csv
import re
import argparse
import os
import tweepy


def scrape(hashtags, n, consumer_keys, access_keys):
    """
    Scrapes tweet data from Twitter's API via tweepy module.

    Parameters:
        hashtags: string of hashtags or phrases to search for (e.g., "#SPACEX AND NASA")
        n: number of tweets to scrape
        consumer_keys: tuple where first element is consumer key and second is consumer secret key
        access_keys: tuple where first element is access token and second is access secret token

    Returns:
        A list of tweets, where each tweet is stored as a dictionary object.

    """
    results = []

    # Send request
    auth = tweepy.OAuthHandler(consumer_keys[0], consumer_keys[1])
    auth.set_access_token(access_keys[0], access_keys[1])

    # Create tweepy API object
    api = tweepy.API(auth)

    print("Scraping...")
    tweets = tweepy.Cursor(api.search, q=hashtags + '-filter:retweets', lang='en', tweet_mode='extended').items(n)
    try:
        for tweet in tweets:
            # Gather all the desired data
            timestamp = tweet.created_at
            user = tweet.user.screen_name
            num_followers = tweet.user.followers_count
            tags = [hashtag['text'] for hashtag in tweet._json['entities']['hashtags']]
            text = tweet.full_text.replace('\n', ' ')
            text = re.sub(r'[^\x00-\x7f]', r'', text)  # Remove non-ascii characters

            results.append({"time": timestamp, "user": user, "num_followers": num_followers, "hashtags": tags, "text": text})

    except tweepy.TweepError as e:
        print(e.reason)

    return results


def write_csv(tweets, file_name):
    """Writes liast of tweets to a csv file"""

    # Write data into the data directory
    if not os.path.exists('data/'):
        os.mkdir('data')
    os.chdir('.\data')

    with open(file_name, 'w', newline='', encoding='utf8') as file:
        file = csv.writer(file)

        file.writerow(['Timestamp', 'User', 'Num Followers', 'Hashtags', 'Tweet Text'])

        for tweet in tweets:
            file.writerow([tweet["time"], tweet["user"], tweet["num_followers"], tweet["hashtags"], tweet["text"]])

        print("Created {}".format(os.getcwd() + "\\" + file_name))

if __name__ == '__main__':
    # Create command-line argument parser and mandatory arguments
    parser = argparse.ArgumentParser(description="Scrape tweets using specified hashtags or phrases.")
    parser.add_argument('-n', '--num_tweets', type=int, metavar='', required=False, help="Number of tweets to scrape")
    parser.add_argument('-p', '--phrase', type=str, metavar='', required=False,
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

    if args.num_tweets is None:
        args.num_tweets = int(input("Enter the number of tweets to scrape:").strip())
    if args.phrase is None:
        args.phrase = input("Enter phrases/hashtags to search for:")

    tweets = scrape(args.phrase, args.num_tweets, (key1, key2), (key3, key4))
    print("{} Tweets scraped successfully.\n".format(len(tweets)))

    write = input("Write to CSV? (Y/N):").strip().lower()[0]
    if write == 'y':
        write_csv(tweets, args.file_name)