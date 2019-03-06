#install.packages("rjson")
#install.packages("tidyverse")
#install.packages("ggfortify")
#install.packages("autoplotly")
library(rjson)
library(tidyverse)
library(ggfortify)
library(autoplotly)

person_df <- read_csv("/Users/areebaahmed/NLPFA18/data/processed/people.csv")


#filtered_df <- person_df %>%
#        filter(username == "bulbie") %>%
#        select(`sentiments.Anger`:`sentiments.Tentative`)


unique_people <- tibble(name=c("bulbie", "Starless", "ranger", "shrew", "Wiseowl", "Tatty", "AliceinWonderland", "madmark", "volnash", "apple", "rubyrose"))
unique_people_df <- unique_people %>% 
        mutate(username = name) %>%
        left_join(person_df, by = "username")

#kmeans_obj <- kmeans(unique_people_df, 10, nstart=25)
#clusters <- kmeans_obj$cluster
#centers <- kmeans_obj$centers
people.pca <- unique_people_df %>% 
        select(`sentiments.Anger`:`sentiments.Tentative`) %>%
<<<<<<< Updated upstream
        prcomp(center=TRUE, tol=0.7)
=======
        prcomp(center=TRUE)

people <- autoplotly(people.pca, 
         loadings = TRUE, loadings.label = TRUE,
         colour = as.numeric(as.factor(unique_people_df %>% pull(username))),
         data=unique_people_df)
people + labs(title = "Top User Behavior")
#people + labs()

# ranger has red
# bulbie is black 
# starless is green. 
# shrew is blue.
# Wiseowl is light blue
# y and x axis don't matter. To be honest the individual people don't really matter.
# Watson output (0 if polar in 1)
# Time line slider. Adding text to the labels.
# Selection of forum (one vs another)
>>>>>>> Stashed changes

autoplotly(people.pca,
           loadings = TRUE, loadings.label = TRUE,
           colour = as.numeric(as.factor(unique_people_df %>% pull(username))),
           data=unique_people_df)
