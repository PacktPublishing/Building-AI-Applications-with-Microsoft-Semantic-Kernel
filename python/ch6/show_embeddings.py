from openai import OpenAI
from dotenv import load_dotenv
from typing import Tuple
import numpy as np
from numpy.linalg import norm
import os

def similarity(A: np.array, B: np.array) -> float:
    # compute cosine similarity
    cosine = np.dot(A,B)/(norm(A)*norm(B))
    return cosine

def get_embedding(text: str) -> Tuple[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

if __name__ == "__main__":
    load_dotenv()
    king = get_embedding("The king has been crowned")
    queen = get_embedding("The queen has been crowned")
    linkedin = get_embedding("LinkedIn is a social media platform for professionals")

    for i in range(0, 10):
        print(king[i])

    print(similarity(king, queen))
    print(similarity(king, linkedin))
    print(similarity(queen, linkedin))
