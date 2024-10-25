MOODS = [
    "cold autumn day, seeking a film to warm the heart with my loved ones",
    "bright summer morning, in the mood for an adventure flick",
    "rainy afternoon, longing for a deep mystery or drama",
    "lively spring evening, craving a dance or musical film",
    "quiet winter night, ready for a classic or a heartfelt story",
    "sunny day, desiring a light-hearted comedy or romance",
    "misty dawn, setting the scene for a fantasy or epic tale",
    "back from the city, feeling a noir or thriller vibe",
    "lazy sunday afternoon, wanting a family or animated movie",
    "clear starry night, up for a sci-fi or otherworldly journey",
    "feeling the need for some old-school classics",
    "hoping for heartwarming tales with family",
    "seeking an edge-of-the-seat thriller night",
    "craving feel-good comedies and chuckles",
    "desiring epic adventures with grand battles",
    "looking for tales of star-crossed lovers",
    "intrigued by mysteries and detective sagas",
    "yearning for musicals with catchy tunes",
    "eager for animation and childhood wonders",
    "wanting a dive into deep, thought-provoking drama",
    "hankering for spine-chilling horror stories",
    "in the mood for travel and scenic world explorations",
]

ABOUT = """# About
Ever had one of those days where you're thinking, "I'm feeling so blue, a rom-com is just the thing," or "I'm on top of the world, bring on the action"? Well, Moodflix is here to save your movie night.
Get tailored recommendations based on your current feels. Say goodbye to endless scrolling and hello to the ideal movie match.
Whether you're in the mood for some drama, thrills, or romance, Moodflix is your new best cinema friend. Let's get those movie vibes going!

## The Data
The dataset provides metadata about the top 10,000 movies from **The Movie Database (TMDB)**. Encompassing a diverse set of attributes, details such as movie titles, release dates, runtime, genres, production companies, budget, and revenue are included. Key attributes highlighted are the unique identifier (`id`), movie title (`title`), associated genres (`genres`), the original production language (`original_language`), average user rating (`vote_average`), a popularity score based on user engagement (`popularity`), a brief synopsis (`overview`), the production budget in USD (`budget`), the movie's total revenue in USD (`revenue`), the movie's duration in minutes (`runtime`), and its promotional tagline (`tagline`). This data, sourced from TMDB, was retrieved from Kaggle and has been processed for enhanced quality and usability.

**Source:** [Top 10000 popular Movies TMDB](https://www.kaggle.com/datasets/ursmaheshj/top-10000-popular-movies-tmdb-05-2023)

## Indexing the movies
The ingestion pipelines processes the data and prepares it for similarity-based recommendations.
It utilizes the `sentence-t5-large` model from SentenceTransformers to convert textual information from movie titles, genres, overviews, and taglines into numerical embeddings.
These embeddings serve as condensed representations, capturing the content nuances of each film, facilitating efficient similarity comparisons.

To enable rapid similarity searches, the we use the `hnswlib` library to create a search index based on the HNSW (Hierarchical Navigable Small World) algorithm.
This indexing approach ensures fast and accurate retrieval, making it suitable for real-time movie recommendations.
Once processed, the structured movie details are stored, and the search index is saved, paving the way for subsequent recommendation operations.

## Searching for similar movies
Upon receiving the user's mood input, we encode the text into a numerical vector embedding.
This embedding is essentially a dense vector that captures the essence of the user's mood in a format conducive to similarity comparisons.
The generated embedding is then used as a search query in the `hnswlib` index to perform a k-nearest neighbors search.
This search retrieves movies with embeddings that are most similar to the mood embedding, ensuring that the movies align closely with the user's specified mood.

## Extras"""
