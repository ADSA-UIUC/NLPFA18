library(rjson)
library(tidyverse)
library(ggfortify)
library(autoplotly)

person_df <- read_csv("data/processed/people.csv")


filtered_df <- person_df %>%
        filter(username == "bulbie") %>%
        select(`sentiments.Anger`:`sentiments.Tentative`)

kmeans_obj <- kmeans(filtered_df, 10, nstart=25)
clusters <- kmeans_obj$cluster
centers <- kmeans_obj$centers
people.pca <- filtered_df %>% prcomp(center=TRUE)

autoplotly(people.pca, 
         loadings = TRUE, loadings.label = TRUE,
         colour = clusters,
         data=filtered_df)


