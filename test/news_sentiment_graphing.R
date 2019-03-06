library(rjson)
library(tidyverse)
library(ggfortify)
library(autoplotly)

locale <- locale(encoding = 'UTF-8')

bus_df <- read_csv("src/preparation/sentiments/business_doclevelsentiments.csv",
                   locale = locale) %>% 
        mutate(type="business")
ent_df <- read_csv("src/preparation/sentiments/entertainment_doclevelsentiments.csv",
                   locale = locale) %>% 
        mutate(type="entertainment")
gen_df <- read_csv("src/preparation/sentiments/general_doclevelsentiments.csv",
                   locale = locale) %>%
        mutate(type="general")
hea_df <- read_csv("src/preparation/sentiments/health_doclevelsentiments.csv",
                   locale = locale) %>%
        mutate(type="health")
sci_df <- read_csv("src/preparation/sentiments/science_doclevelsentiments.csv",
                   locale = locale) %>%
        mutate(type="science")
spo_df <- read_csv("src/preparation/sentiments/sports_doclevelsentiments.csv",
                   locale = locale) %>%
        mutate(type="sports")
tec_df <- read_csv("src/preparation/sentiments/technology_doclevelsentiments.csv",
                   locale = locale) %>%
        mutate(type="technology")

big_df <- rbind(bus_df, ent_df, gen_df, hea_df, sci_df, spo_df, tec_df)

# grab all articles which have a headline confidence level in one emotion of at least THRESHOLD
THRESHOLD <- 0.7
filtered_df <- big_df %>% 
        mutate(max = apply(select(., `Anger`:`Tentative`), 1, max)) %>%
        filter(max > THRESHOLD) %>%
        arrange(desc(max))

pca <- filtered_df %>% 
        select(`Anger`:`Tentative`) %>%
        prcomp(center=TRUE, tol=0.7)

autoplot(pca,
         loadings = TRUE, loadings.label = TRUE,
         colour = as.numeric(as.factor(filtered_df %>% pull(type))),
         data=filtered_df,
         legend=TRUE)
