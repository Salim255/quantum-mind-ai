from rapidfuzz import process


class SpellCorrector:

    @staticmethod
    def correct(query: str) -> str:

        words = query.split()

        vocabulary = set()

        for concept in CONCEPTS.values():
            vocabulary.update(concept["anchors"])

        corrected_words = []

        for word in words:

            match = process.extractOne(
                word.lower(),
                vocabulary,
                score_cutoff=80
            )

            if match:
                corrected_words.append(match[0])
            else:
                corrected_words.append(word)

        return " ".join(corrected_words)