# PURPOSE: 

This project uses Apache Airflow to implement an automated Data Pipeline which sets up a data warehouse to support easy-to-use optimized queries and data analysis for the Sparkify music streaming app, which stores all song and user activity data/metadata in JSON files. The pipeline uses AWS Redshift to extract the Sparkify data from these JSON files and place it in two staging tables. From there, Redshift is used to transform and load the staged data into a star schema useful for analytical queries. Airflow data quality checks are performed to help ensure integrity of the final tables. The overall table schema is defined as follows:

## Staging Tables (2)
staging_events : keys={artist, auth, firstname, gender, iteminsession, lastname, length, level, location, method, 
                       page, registration, sessionid, song, status, ts, useragent, userid}\
staging_songs : keys={artist_id, artist_latitude, artist_location, artist_longitude, artist_name, duration, 
                      num_songs, song_id, title, year}

## Fact Table: 
fact_songplay : keys={songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent}

## Dimension Tables (4) 
dim_users : keys={user_id, first_name, last_name, gender, level}\
dim_songs : keys={song_id, title, artist_id, year, duration}\
dim_artists : keys={artist_id, name, location, latitude, longitude}\
dim_time : keys={start_time, hour, day, week, month, year, weekday}

The justification for staging in this manner is that it takes the data/metadata for song and user activity exactly as generated and logged by existing Sparkify business processes and provides an intermediate Redshift storage point from which further transformation can be performed to generate fact and dimension tables more suitable for analytical queries. 

The justifications for the choice of a star schema for the analytical queries include:

a) Being denormalized, the join logic required for queries is much simpler than with a normalized schema.\
b) Simplified reporting logic for queries of business interest.\
c) Optimized query performance (especially for aggregations).
