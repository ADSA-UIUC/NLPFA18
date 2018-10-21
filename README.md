# NLP Healthcare Project

## Objective

Our goal is to use posts from mental health forums to identify people with similar 
backgrounds/concerns so they can identify with each other. We thought that this way, 
people undergoing depression/mental issues who simply need attention can receive 
attention from individuals who understand what the person is going through. We hope 
that this will eventually lead to support groups more tailored to what the a certain 
person is needing.

## Methods

We divided the project into two main groups: A group that can gather the required data 
to analyze and another group focusing on analyzing the data in order to figure out how
to group people together.

### Web Scraping Group

Our group is gathering the data from mental health forums. Our main focus is to gather 
posts and the usernames of those who wrote each post. Other useful information that we 
could collect includes dates, likes/hugs, and mentions within posts. Since forums are 
so large, we will be using a mix of Selenium and Beautiful Soup to move through pages 
and collect the relavent data.

### Algorithms Group

Our group is looking at unsupervised machine learning as a primary way to group people 
together. By using an algorithm such as KMeans, we think that we may be able to 
appropriately group specific people together. Our main objective of this project was 
to learn Natural Language Processing as well, and working with text data allows us to 
do so. We aim to be able to extract key words from the posts that might lead to a 
stronger link between two people (such as words relating to relationship problems or 
specific situations) and to be able to subtract slightly less meaningful parts of the 
post in order to cut down on computation requirements.


## Contributors

### Web Scraping Group
+ Anwesa Goswami
+ Aareana Reza
+ Areeba Ahmed
+ Danielle Curammeng

### Algorithms Group
+ Isa Dash
+ Kevin Zhang
+ Qi Yu Kang
+ Shaw Kagawa
