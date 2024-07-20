# Batchelor - Final Project

Back in 2019 I graduated in Computer Science at Polimi (Milan Politechnic).

This was my project for the final exam (a practice one).

## What is it

This is a project inspired from the library circuit in my hometown.

It's a software for handling books and borrowing across multiple libraries.

It aims also to provide some insights, like books suggested based on the read by other users based on the user readings.

## How it's structured

The project is made with Django as web framework and a Neo4j instance as database (it has a sqlite db just for user authentication).

Neo4j is a popular graph database; since I really like it, and think it's a more suitable database for highly interconnected data, I choose it over any SQL engine.

We have then four Django modules:

- authentication: to handle user login and registration
- backend: anything related to the database
- frontend: anything related to the web gui presented to the end user or the librarian
- external_api: external service to query for data for new books

Please note that this was something close to what should be a POC (proof of concept).

In my mind there should also been a delivery system (like mails) for notification, but due to time limit I wasn't able to implement it. There are also some few bugs, but time was limited and so they weren't fixed at the time.

Back in the days my code was also with less quality, so right now I don't think I would have done the same choiches and implementation.

## Won't you progress?

While I was tempted, in the following years I discovered microservices, and since my daily job is with those, I preferred to start from scratch, implementing the same project with microservices on a Kubernetes cluster.

The new repo for the probject is [Ferrea](https://github.com/Grimoldi/ferrea)
