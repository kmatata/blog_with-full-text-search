# Blog with live search functionality

# included
- recomendation(simple) engine based on taggit model instances
- pagination
- live-search with either options:
    1. Trigram similarity (based on postgres pg_trgm ext)
    2. Stemmed and ranked results based on django.postgres module's SearchRank, SearchQuery and SearchVector classes
    3. Weighted queries from searchvector class
- alpinejs and vanilla js for nice interactivity
- tailwind styling

