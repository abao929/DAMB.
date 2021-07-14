# Data Deliverable Report - DAMB.

**Team members**: Dustin Wu, Alex Bao, Matthew Lee, and Beatrice Hoang **[edit this]**

## Step 1

1. We first queried Spotify's API to determine what genres of songs Spotify defines, and then selected 15 genres that we felt were distinct and popular enough to classify. We searched Spotify for Spotify-generated and user-generated playlists pertaining to a specific genre (e.g. a pop music playlist or a metal music playlist), and saved the Spotify ids of these playlists. We then made requests to Spotify's API to get the songs of the playlist, and then for each song we extracted numerous Spotify API features, such as whether the song contains explicit language or whether the song is suitable for dancing. In addition, we downloaded the album cover of each song and identified the dominant hue, saturation, and value of the image.

2. Our data partially consists of user-created playlists, so part of our data relies on the classifications of Spotify users. However, we believe that these classifications are reputable, because 1) we selected highly popular playlists, so the playlists we selected have the backing of many users on the site who approve of the song choices and 2) the classification of genres as a whole has a lot to do with how listeners recognize specific  traits in a song, and so user-generated playlists satisfy our goal of classifying genres. 

At first we had planned on getting genre labels from Spotify's API, since the documentation does list a genre attribute as a return value for the documentation. However, we found that the vast majority of songs were not labelled with a genre, so all we got was an empty string. Therefore, we decided that relying on playlists to obtain labels would both yield fairly accurate labels without having to spend siginifant labor on manually labelling each song.

## Step 2

While our dataset does not have an explicit primary key attribute, a tuple of (song name, artist name), each of which are strings, acts as the primary key; we assume that no artist has released two songs with the same name.  

Variables of interest include whether the song has explict lyrics or not (boolean), how popular the song is on a Spotify-defined score of 0-100 (integer), how suitable the song is for dancing, according to Spotify on a scale from 0 to 1 (float), and the valence, how positive or negative the song is. We have collected other variables from spoityf

## Step 3

1. From our data collection process, we gathered around 400 to 700 album covers for each of the 15 genres that we selected. There were duplicates, because each song could appear in multiple playlists, but these were removed.

There are two primary issues with the data prior to cleaning, both relating to the sizes of the images. The first is that the images have quite high resolution, 640 by 640 pixels, which is an excessive amount of information to feed into a machine learning model; training on this size will be incredibly time consuming and could lead to overfitting. We don't need this many pixels because not every pixel is meaningful; a 160 x 160 pixel image, while appearing more grainy to the human eye, still contains the distinctive features that link the image to a genre.

The second issue is that not all images are square; we need every image to be square for homogeny; namely, so that the model can expect to see the same size of input for every data sample. So we will have to resize each image to be square.

An issue that could be problematic is that the names of songs occaisonally contained special characters, such as accented characters or symbolic characters like korean. However, we are primarily focused on relating images to genre labels, so while these characters have introduced some errors in our data collection and manipulation process, they will most likely not interfere with the actual training.

Lastly, we noticed that a small number of album covers have "duplicates" in the sense that there are "deluxe" versions of other album covers. These album covers have different image names and in some cases the album cover images themselves are different, so it they are arguably different from their normal versions. In addition, there are relatively few instances of this relative to the number of covers in our dataset, so we decided that this will not substantially impact the results of our trained model.

2. We dealt with the issues raised above by resizing the images to 160 x 160 pixels. This was done in a manner that preserves the information in each image; the images were scaled down rather than simply cropping a 160 x 160 square out of the full-sized image. We did not find any anomalous traits that required us to eliminate any data.

## Step 4

We constructed our held out test set by randomly shuffling the list of album covers and designating the first 20% of the list as test data for each genre, and moving these files into a separate test data directory. Thus, we used random sampling to select our test set. We believe that this is the correct choice because any attempt to select a test set based on the specific qualities of the images would require needlessly complex image processing and/or tedious labor. Furthermore, trying to select a specific category or type of images to go into the testing set would create a bias in the training set against that category or type. Simply put, random sampling is both the simplest and most unbiased way of constructing our test set.

The rest of the data is used as the training data. The training data for each of the 15 genres consists of around 320 to 560 album covers, and the test data consists of around 80 to 140 album covers per genre.

## Step 5

The people represented in the dataset are the graphic designers of the album covers that we use as data. Our project could potentially impact the community of artists/designers by dictating what styles of cover fit best in a specific genre. This might negatively impact the innovation and creativity of album cover design by suggesting that the features of an album cover must dictate whether it is a good fit for a specific genre.

Some of the album covers in our training data contain peoples' faces, which could be an ethical gray area if the people on these covers did not intend for their faces to be used in this manner. However, the intent of an album cover is to been seen by and attract the public, so it is unlikely that our data infringes on anyone's privacy. Furthermore, the Spotify users who created some of the playlists that we use probably did not intend for their playlists to be analyzed, but because they are widely popular and intended for public consumption we also do not see many ethical problems that could arise in this regard.

Certain genres could have album covers that mostly feature people of a specific demographic, and our model could pick up on these biases and mirror them in its predictions. The only way to counteract these biases is to introduce a diverse range of album covers to the model. We can do this by continually feeding the model new album covers as they release; the hope is that over time the expression of music in album covers diversifies. However, we believe that our current data set has diversity because it incorporates the classification behaviors of mulitple users on the site.

## Step 6

The biggest techinical challenge that we anticipate is building and training a machine learning model that works with images. While there are plenty of resources on the interent that go into this (specifically convolutional neural networks, which we currently plan to use) and plenty of libraries/frameworks for us to build on top of, we have not had any prior exposure to this type of machine learning in the course.

In particular, we anticipate that training the models will be fairly time-consuming, since even though we have scaled down our images, they are still very dense compared to a vector of at most several variables. 

We divided data collection by assigning genres among our members to collect. We also all collaborated on creating a standardized data collection method and train test split. We also all worked on writing this report together, incorporating feedback and opinions from all members of the group.