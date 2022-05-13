import requests
import pytest


URL = "http://127.0.0.1:8888/"

def make_request(question: str) -> str:
    res = requests.post(URL, json={"question": question})
    return res.json()["answer"]


def test_model_answers():
        input_questions = [
            "What is the capital of Russia?",
            "What is the capital of Great Britain?",
            "How many countries are there?",
            "What is natural language processing?",
            "How many plays did Shakespeare write?",
            "Who is Winston Churchill?",
            "How did Baromir die?",
            "What is love?",
            "What was the name of Dumbledore's bird from Harry Potter?"
        ]

        gold_answers = [
            "Moscow",
            "London",
            "120",
            "a subfield of computer science, information engineering, and artificial intelligence",
            "Three",
            "unknown",
            "unconscious",
            "to will the good of another",
            "Professor Albus Percival Wulfric Brian"
        ]

        for question, answer in zip(input_questions, gold_answers):
            assert(make_request(question).lower() == answer.lower())

if __name__ == '__main__':
    test_model_answers()