from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import re
import sys
import time
import random
from itertools import islice
import keyboard

def fetch_page(url):
    try:
        page = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
        return page
    except:
        return None

def get_sample_type(soup_page):
    #get the original song details
    header_title = soup_page.find(class_='section-header-title')
    header_title_text = header_title.get_text()
    return header_title_text

def get_ratings_for_samples(track_links):
    return_frame = pd.DataFrame()

    for link in track_links:
        time.sleep(random.uniform(0.5, 2.0))
        link_page = fetch_page(link)
        if( link_page is None):
            url_dict = {'url': link, 'issue': 'Failed to get ratings page'}
            url_row = pd.DataFrame(url_dict, index=[0])
            print("Error: couldn't get webpage for ratings: " + link)
            return None, url_row
        if(int(link_page.status_code) != 200):
            url_dict = {'url': link, 'issue': 'Failed to get ratings page'}
            url_row = pd.DataFrame(url_dict, index=[0])
            print("Error: couldn't get webpage for ratings: " + link)
            return None, url_row

        try:
            soup = BeautifulSoup(link_page.content, 'html.parser')
            #get the sample type
            sample_type = get_sample_type(soup)

            #get the original song details
            rating_count = soup.find(class_='ratingCount')
            rating_count = rating_count.get_text().split(" ", 1)[0]
            rating_value = soup.find(class_='ratingOverlay')
            rating_value = str(rating_value)
            rating_value = re.search('width:(.+?)px', rating_value).group(1)
            rating_value = round((float(rating_value) / 125) * 5, 1)
            ratings = {'rating':rating_value, 'votes':rating_count, 'sample link': link, 'sample type': sample_type}
            frame = pd.DataFrame(ratings, index=[0])
            return_frame = return_frame.append(frame)
        except Exception as e:
            ratings = {'rating':'NONE', 'votes':'NONE'}
            frame = pd.DataFrame(ratings, index=[0])
            return_frame = return_frame.append(frame)
    return return_frame, None

def get_sample_info(url):
    page = fetch_page(url)

    if( page is None):
        print("Error: couldn't get webpage for: " + url)
        url_dict = {'url': url, 'issue': 'Failed to get page'}
        url_row = pd.DataFrame(url_dict, index=[0])
        return None, url_row
    if(int(page.status_code) != 200):
        print("Error: couldn't get webpage for: " + url)
        str_error = 'Error code: ' + str(page.status_code)
        url_dict = {'url': url, 'issue': str_error}
        url_row = pd.DataFrame(url_dict, index=[0])
        return None, url_row

    try:
        soup = BeautifulSoup(page.content, 'html.parser')
        
        #get the original song details
        original_song = soup.find(class_='trackInfo')
        original_song_name = original_song.find("h1").get_text()
        original_artist = original_song.find("h2").get_text()
        try:
            original_album = original_song.find(class_="release-name").get_text()
        except:
            original_album = 'NONE'
        
        sections = soup.find_all('section')
        
        #search for the page section that contains the samples
        section_index = -1
        for idx,item in enumerate(sections):
            if item.find(text=re.compile(r'^Contains sample')):
                section_index = idx

        if section_index < 0:
            print("no samples found for song: " + original_song_name)
            d = {'url':url, 'song': original_song_name, 'artist': original_artist, 'album':original_album, 'sampled song':'NONE','sampled artist':'NONE', 'sample link': 'NONE'}
            frame = pd.DataFrame(d, index=[0])
            return frame, None

        else:
            #get track names from the samples
            track_name_items = sections[section_index].find_all(class_='trackName')
            track_names = [track.get_text() for track in track_name_items]
            
            #get the links to the page with youtube link for the sample
            track_link_extensions = [track.get('href') for track in track_name_items]
            track_links = ['https://www.whosampled.com' + extension for extension in track_link_extensions]
            ratings, fail_ratings = get_ratings_for_samples(track_links)

            if fail_ratings is not None:
                 fail_row = fail_ratings
            else:
                fail_row = None

            #get the artists for the sample tracks
            track_artist_items = sections[section_index].find_all(class_='trackArtist')
            track_artists = [track.get_text()[3:].replace('\n','').replace('\t','') for track in track_artist_items]
            
            #put it all in a frame
            d = {'url':url, 'song': original_song_name, 'artist': original_artist, 'album':original_album, 'sampled song':track_names,'sampled artist':track_artists, 'sample link': track_links}
            frame = pd.DataFrame(d)
            if ratings is not None:
                frame = frame.merge(ratings, on='sample link', sort=False )
            return frame, fail_row
    except Exception as e:
        if str(e) == "\'NoneType\' object has no attribute \'find\'":
            print("Error: Invalid URL for " + url)
            url_dict = {'url': url, 'issue': 'Invalid URL'}
            url_row = pd.DataFrame(url_dict, index=[0])
            return None, url_row
        url_dict = {'url': url, 'issue': 'Unknown Issue'}
        url_row = pd.DataFrame(url_dict, index=[0])
        return None, url_row

def main():
    """launcher"""
    csv_file = sys.argv[1] 
    url_list_df = pd.read_csv( csv_file,header=None )

    try:
        max_search = int(sys.argv[2])
    except:
        max_search = 99999

    try:
        start_index = int(sys.argv[3])
    except:
        start_index = 0

    #setup main dataframe for all the samples
    main_df = pd.DataFrame()
    bad_df = pd.DataFrame()
    counter = 0

    print("---Starting scraping at row " + str(start_index) + " of csv---")

    #loop through all those links
    for url in islice(url_list_df[0], start_index, None):
        time.sleep(random.uniform(5.0, 6.8))
        print("row: " + str(start_index + counter))
        sample_info, bad_info = get_sample_info(url)
        if sample_info is not None:
            main_df = main_df.append(sample_info)
        if bad_info is not None:
            bad_df = bad_df.append(bad_info)
        counter = counter + 1
        if(counter >= max_search):
            break
    
    bad_filename = "bad_url_links___"+str(start_index)+"_"+str(start_index+counter)+".csv"
    gud_filename = "scraped_samples_"+str(start_index)+"_"+str(start_index+counter)+".csv"
    
    bad_df.to_csv(bad_filename)
    main_df.to_csv(gud_filename)

    print("all done!")

if __name__ == '__main__':
    main()