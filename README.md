## New Movies - Scheduled Report

This script scrapes the 'In Theatres' page of IMDB.com to get summaries of new movie releases. After scraping, it will email you the output of the script in an easily readable format.

Using Amazon lambda, you can set up a cron job at any cadence for the script to run and send its results (e.g. send every Friday morning, when new movies are released).