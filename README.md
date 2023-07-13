# Music Sample Utility Scraper

## Intro ##
This is a web scraping utility created using Python and Beautiful Soup that queries the popular sample music database "WhoSampled". 

## Usage ## 
```
python whosampled.py YOUR_FILENAME.csv a
```
- YOUR_FILENAME.csv - list of WhoSampled URLs to scrape for samples
- a [optional] - max number of samples to scrape. If no number input, it scrapes the whole file

## Methodology ##
- def fetch_page(url): uses requests library to return page for given url
- def get_sample_type(soup_page): get sample type from section-header-title element
- def get_ratings_for_sample (track_links): for each sampled song, create BeautifulSoup Object and get the rating count and number of votes
- def get_sample_info(url): get original song and sampled song information (song name, artist, etc)


## Output ##
- For each song:
    - List of original songs that were sampled (Song Name, Artist, Year Released)
    - Sample rating, Sample votes and Sample

## Analysis ##
Using the utility, a popular song that was sampled by many others was queried. This song, called "Impeach the President", created by the band The Honeydrippers, contains an iconic drum line used in many hip-hop, rnb, and pop songs to this day. Let's have a look at some insights from all of the songs that sampled this song.


### Cumulative Number of Songs Sampled ###
The original sample was relegated to vinyl obscurity until it was unearthed by DJ Marley Marl and MC Shan, who used it as the backing of the song "The Bridge", which became a local NY anthem referencing Queensbridge as the birthplace of hip-hop. 

It is interesting to see the sample's popularity explode shortly after that point, hitting a huge point of growth in the 90s, and over 802 cumulative songs sampled to this day.

![Cumulative Songs](/Cumulative.png)

![By Decade](/ByDecade.png)

### Most Popular Sampled Songs ####
Using the sample votes column, we can see which songs have the most votes from users. This is an indicator of the songs popularity as it relates to its sampling. Interesting to note that all of these songs are hip-hop/rap. 

| sampled_artist          | sampled_song                        | sample_type            | sample_votes | Votes | rating_value | sampled_album                                 |
| ----------------------- | ----------------------------------- | ---------------------- | ------------ | ----- | ------------ | --------------------------------------------- |
| Audio Two               | Top Billin'                         | Direct Sample of Drums | 58 Votes     | 58    | 5            | What More Can I Say?                          |
| J. Cole                 | Wet Dreamz                          | Direct Sample of Drums | 27 Votes     | 27    | 5            | 2014 Forest Hills Drive                       |
| Nas                     | I Can                               | Direct Sample of Drums | 18 Votes     | 18    | 5            | God's Son                                     |
| The Notorious B.I.G.    | Unbelievable                        | Direct Sample of Drums | 17 Votes     | 17    | 5            | Ready to Die                                  |
| Kris Kross              | Jump                                | Direct Sample of Drums | 17 Votes     | 17    | 5            | Totally Krossed Out                           |
| MC Shan                 | The Bridge                          | Direct Sample of Drums | 15 Votes     | 15    | 5            | Down by Law                                   |
| Digable Planets         | Rebirth of Slick (Cool Like Dat)    | Direct Sample of Drums | 11 Votes     | 11    | 5            | Reachin' (A New Refutation of Time and Space) |
| INI                     | Fakin Jax                           | Direct Sample of Drums | 11 Votes     | 11    | 5            | Fakin Jax                                     |
| Boogie Down Productions | The Bridge Is Over                  | Direct Sample of Drums | 11 Votes     | 11    | 5            | Criminal Minded                               |
| Nas                     | The Message                         | Direct Sample of Drums | 10 Votes     | 10    | 5            | It Was Written                                |
| LL Cool J               | Around the Way Girl                 | Direct Sample of Drums | 10 Votes     | 10    | 5            | Mama Said Knock You Out                       |
| Biz Markie              | Make the Music With Your Mouth, Biz | Direct Sample of Drums | 10 Votes     | 10    | 5            | Goin' Off                                     |

 
