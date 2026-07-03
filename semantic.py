import random
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from database import get_all_pairs
from config import SIMILARITY_THRESHOLD, MAX_REPLY_LENGTH

model = SentenceTransformer("all-MiniLM-L6-v2")


def find_best_reply(user_message):
    pairs = get_all_pairs()

    if not pairs:
        return None

    messages = [pair[0] for pair in pairs]
    replies = [pair[1] for pair in pairs]

    embeddings = model.encode(messages)
    query_embedding = model.encode([user_message])

    scores = cosine_similarity(query_embedding, embeddings)[0]

    valid_replies = []

    for i, score in enumerate(scores):
        if (
            score >= SIMILARITY_THRESHOLD
            and len(replies[i]) <= MAX_REPLY_LENGTH
            and replies[i].strip().lower() != user_message.strip().lower()
        ):
            valid_replies.append(replies[i])

    if not valid_replies:
        return None

    return random.choice(valid_replies)