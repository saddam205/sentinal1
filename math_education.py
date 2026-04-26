# math_education.py
# Standard library imports
import math
import random
from typing import List, Tuple, Dict, Any

class MathConceptExplainer:
    """
    Explains mathematical concepts related to cybersecurity and algorithms.
    Used for the educational modules in the CyberSec Lab.
    """
    def __init__(self):
        self.concepts = {
            "prime_numbers": (
                "Numbers greater than 1 with no divisors other than 1 and themselves. "
                "In RSA encryption, the security relies on the difficulty of factoring "
                "the product of two large prime numbers."
            ),
            "modulo": (
                "The remainder operation. In cryptography, modular arithmetic is used "
                "to keep numbers within a specific range, such as in Diffie-Hellman "
                "key exchange or hashing algorithms."
            ),
            "entropy": (
                "A measure of randomness or unpredictability. In cybersecurity, "
                "high entropy is essential for generating strong cryptographic keys "
                "and secure passwords."
            ),
            "rsa_algorithm": (
                "An asymmetric encryption algorithm that uses a public key for "
                "encryption and a private key for decryption. It relies on the "
                "mathematical properties of large prime numbers."
            )
        }

    def explain(self, concept_name: str) -> str:
        """Returns a string explanation of a given math concept."""
        return self.concepts.get(concept_name.lower(), "Concept not found in database.")

class MathProblemGenerator:
    """
    Generates practice problems for the AI Intelligence Engine.
    """
    def generate_problem(self, category: str = "arithmetic") -> Tuple[str, Any]:
        """
        Generates a problem and its solution based on the category.
        Returns: (problem_text, answer)
        """
        if category == "encryption":
            # Simple RSA-style product calculation
            p = random.choice([3, 5, 7, 11, 13])
            q = random.choice([17, 19, 23, 29])
            n = p * q
            return f"In an RSA scenario, if p={p} and q={q}, what is the modulus N?", n
        
        elif category == "modulo":
            a = random.randint(50, 200)
            b = random.randint(5, 20)
            return f"Calculate the result of {a} mod {b}.", a % b
            
        # Default simple arithmetic
        x, y = random.randint(1, 10), random.randint(1, 10)
        return f"Solve: {x} + {y}", x + y

class MathVisualization:
    """
    Provides coordinate data for rendering charts in the front-end (Chart.js).
    Used by the visualization layer in fast6.py.
    """
    def get_plot_points(self, function_type: str = "linear") -> List[Tuple[float, float]]:
        """
        Generates data points for mathematical functions.
        """
        points = []
        if function_type == "sine":
            for x in range(0, 21):
                # Scale x for better visualization
                val = x * 0.5
                points.append((val, round(math.sin(val), 4)))
        elif function_type == "exponential":
            for x in range(0, 11):
                points.append((x, round(math.exp(x / 5), 4)))
        else:
            # Default linear
            for x in range(0, 11):
                points.append((float(x), float(x)))
        
        return points

if __name__ == "__main__":
    # Internal self-test for debugging
    print("--- Math Education Module Test ---")
    explainer = MathConceptExplainer()
    print(f"Concept Check (Modulo): {explainer.explain('modulo')}")
    
    generator = MathProblemGenerator()
    prob, ans = generator.generate_problem("encryption")
    print(f"Problem: {prob} | Answer: {ans}")
    
    viz = MathVisualization()
    print(f"Sine Data Points (first 3): {viz.get_plot_points('sine')[:3]}")
    print("--- Test Complete ---")