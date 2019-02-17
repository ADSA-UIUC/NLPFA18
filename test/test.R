library(rjson)
library(tidyverse)
library(ggfortify)
library(autoplotly)

person_df <- read_csv("data/processed/people.csv")


#filtered_df <- person_df %>%
#        filter(username == "bulbie") %>%
#        select(`sentiments.Anger`:`sentiments.Tentative`)


unique_people <- data.frame(name=c("bulbie", "Starless"))
unique_people_df <- as_tibble(unique_people %>% mutate(username = name) %>%
                                      left_join(person_df, by = "username"))

kmeans_obj <- kmeans(unique_people_df, 10, nstart=25)
clusters <- kmeans_obj$cluster
centers <- kmeans_obj$centers
people.pca <- unique_people_df %>% prcomp(center=TRUE)

autoplotly(people.pca, 
         loadings = TRUE, loadings.label = TRUE,
         colour = clusters,
         data=unique_people_df)

