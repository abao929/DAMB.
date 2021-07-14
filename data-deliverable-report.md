# Data Deliverable Report - DAMB.

**Team members**: Dustin Wu, Alex Bao, Matthew Lee, and Beatrice Hoang

## Step 1

1. The task that we are currently thinking of pursuing is predicting a song's genre given a number of factors, from the instrumentality of the song to the dominant color of its album cover. The data we collected will aid us in accomplishing this task.

We first queried Spotify's API to determine what genres of songs Spotify defines, and then selected 15 genres that we felt were distinct and popular enough (according to [Wikipedia](https://en.wikipedia.org/wiki/List_of_popular_music_genres)) to classify. We searched Spotify for Spotify and user generated playlists pertaining to a specific genre (e.g. a pop playlist or a metal playlist), and then made requests to Spotify's API to get the songs of the playlist. For each song we extracted numerous Spotify API features, such as whether or not the song contains explicit language or whether the song is suitable for dancing. In addition, we downloaded the album cover of each song and identified the dominant color in HSV (hue, saturation, value) color scheme, of the image. We used k-means clustering to cluster the pixels of the image by their color values and picked the HSV of the centroid with the most pixels in it. After pulling around 400-700 songs per each of the 15 genres, totalling in around 10000 songs/data points, we then gathered the lyrics of each using a genius.com python library. We then processed the lyrics to get the most common words and the total word count of each song. All this data was stored in a CSV, then split 20-80 arbitrarily to form test and training sets.

2. Our data partially consists of user-created playlists, so part of our data relies on the classification decisions of Spotify users. However, we believe that these classifications are reputable, because 1) we selected highly popular playlists, so the playlists we selected have the backing of many users on the site who approve of the song choices and 2) the classification of genres as a whole has a lot to do with how listeners recognize specific traits in a song, and so user-generated playlists satisfy our goal of classifying genres. 

At first we had planned on getting genre labels from Spotify's API, since the documentation does list a genre attribute as a return value for the documentation. However, we found that the vast majority of songs were not labelled with a genre, so all we got was an empty string. Therefore, we decided that relying on playlists to obtain labels would both yield fairly accurate labels without having to spend siginifant labor on manually labelling each song.

## Step 2

While our dataset does not have an explicit primary key attribute, a tuple of (song name, artist name), each of which are strings, acts as the primary key; we assume that no artist has released two songs with the same name, and that no two artists share the same name and released songs with the same name.

Variables of interest include whether the song has explict lyrics or not (boolean), how popular the song is on a Spotify-defined score of 0-100 (integer), how suitable the song is for dancing, according to Spotify on a scale from 0 to 1 (float), and the valence, how positive or negative the song is. We have collected other variables from Spotify, but have speculated that these ones have the strongest predictive power for genre. In addition, we collected the dominant HSV, each of which are floats, of the album covers for each song because they add an interesting mix to our project, allowing us to pursue hypotheses that relate color to music.

Moving forward, we may decide to list the color values for all of the centroids that our K-means clustering algorithm finds, rather than just the most dominant one; this allows more of the image to be represented by these features.

Because we are not sure which variables we will want to use in our project, and because very few songs (less than ten out of the thousands we collected) were missing any of the variables, we decided to make all variables required and any songs that were missing variables were dropped.

## Step 3

1. From our data collection process, we gathered data for around 400 to 700 songs for each of the 15 genres that we selected. There were duplicates, because each song could appear in multiple playlists, but these were removed.

There are two primary issues with the data prior to cleaning, both relating to the sizes of the images. The first is that the images have quite high resolution, around 640 by 640 pixels, which is an excessive amount of information to feed into our K-means algorithm and perhaps a deep learning image-analyzing algorithm should we choose to use one; training on this size will be incredibly time consuming and could lead to overfitting. We don't need this many pixels because not every pixel is meaningful; a 256 x 256 pixel image, while appearing more grainy to the human eye, still contains the distinctive features that link the image to a genre.

An issue that could be problematic is that the names of songs occaisonally contained special characters, such as accented characters or symbolic characters like korean. However, we are primarily focused on relating images to genre labels, so while these characters have introduced some errors in our data collection and manipulation process, they will most likely not interfere with the actual training. One specific character that we ended up cleaning for is the "/" character, which would be confused for a directory were it not replaced.

We also noticed that a small number of album covers have "duplicates" in the sense that there are "deluxe" versions of other album covers. These album covers have different image names and in some cases the album cover images themselves are different, so it they are arguably different from their normal versions. In addition, there are relatively few instances of this relative to the number of covers in our dataset, so we decided that this will not substantially impact the results of our trained model.

The features that came from Spotify's API did not appear to have issues beyond rarely being missing, and as mentioned above the song was eliminated in this case.

2. We dealt with the issues raised above by resizing the images to 256 x 256 pixels. This was done in a manner that preserves the information in each image; the images were scaled down rather than simply cropping a 256 x 256 square out of the full-sized image. We did not find any anomalous traits that required us to eliminate any data beyond removing songs that had missing values.

During the exploratory analysis phase of the project, we may choose to remove a certain features if they either have a low correlation with genre (or whatever variable we end up aiming to predict) or if they have a high correlation with another variable. We may also remove an entire genre of music (for example heavy metal or metal) if we find that they are being classified similarly. Depending on the task that we choose, it may be necessary to convert string labels into numerical categories (for example, converting 'pop' to 0 and 'rock' to 1 and so on). Finally, we may also want to normalize the data so that high-magintude variables don't overshadow low-magnitude ones. However, because we have not yet commited on a task, we do not know how we want to normalize this data and have decided to leave this for a future stage of the project.

Our data involved the joining of two sources of data; the first is the song traits provided by Spotify's API, and the second is the dominant hue, saturation, and value of the song's album cover's image, which we used K-Means clustering to identify. These sources were joined by matching albums; the color attributes of the album color were joined with the song contained in the album.

## Step 4

We constructed our held out test set by randomly shuffling the list of songs and designating the first 20% of the list as test data for each genre, and moving these files into a separate test data directory. Thus, we used random sampling to select our test set. We believe that this is the correct choice because any attempt to select a test set based on the specific qualities of the images would require needlessly complex image processing and/or tedious labor. Furthermore, trying to select a specific category or type of images to go into the testing set would create a bias in the training set against that category or type. Simply put, random sampling is both the simplest and most unbiased way of constructing our test set.

Because we have a fairly large amount of samples (over 10,000 across all genres), we can be reasonably confident that the train and test splits have a distribution of variables that is fairly similar to that of the original dataset.

The rest of the data is used as the training data. The training data for each of the 15 songs consists of around 320 to 560 album covers, and the test data consists of around 80 to 140 songs per genre.

## Step 5

The people represented in the dataset are the creators behind both the songs and the album covers of those songs. Our project could potentially impact the community of artists/designers by dictating what traits within a song or an album cover fit best in a specific genre. This might negatively impact the innovation and creativity of album cover design by suggesting that a genre restricts the kinds of music and designs within it, rather than the truth which is that the music and covers in a genre are constantly evolving.

Some of the album covers in our training data contain peoples' faces, which could be an ethical gray area if the people on these covers did not intend for their faces to be used in this manner. However, the intent of an album cover is to been seen by and attract the public, so it is unlikely that our data infringes on anyone's privacy. Furthermore, the Spotify users who created some of the playlists that we use probably did not intend for their playlists to be analyzed, but because they are widely popular and intended for public consumption we also do not see many ethical problems that could arise in this regard.

Certain genres could have album covers that mostly feature people of a specific demographic or tend towards traits such as having more explicit language, and our model could pick up on these biases and mirror them in its predictions. In the worst case, this could mean that the model would pick up on and make predictions based on negative stereotypes towards certain genres. The only way to counteract these biases is to introduce a diverse range of songs to the model. We can do this by continually feeding the model new album covers as they release; the hope is that over time the expression of music in any given genre diversifies. However, we believe that our current data set has diversity because by using user-created playlists, it incorporates the classification decisions and tastes of mulitple users on the site.

## Step 6

The biggest techinical challenge that we anticipate is determining which features will prove most valuable, considering that we have collected quite a few. Statistical analysis such as t-tests will help us with this, but it will ultimately be up to our judgement and rationale to decide what direction we want to take.

One direction we could explore is building and training a machine learning model that works with images. However, this might prove to be a challenge; while there are plenty of resources on the interent that go into this (specifically convolutional neural networks, which we currently plan to use) and plenty of libraries/frameworks for us to build on top of, we have not had any prior exposure to this type of machine learning in the course.

In either case, we imagine that training our models will be a time-consuming process, and this will especially be the case if we decide to change direction and/or want to try training on multiple sets of features to see what works best. None of us have top-of-the-line computing resources, so we may have to rely on cloud computing to complete training in a reasonable timeframe.

With regards to group work division, we found that trying to split up and work on separate portions of the project awkward, so instead we met often and worked together on the same components. We divided data collection by assigning genres among our members to collect; each group member searched for playlists related to 3-4 genres. We also all collaborated on creating a standardized data collection method and train test split. We also all worked on writing this report together, incorporating opinions and insights from all members of the group.