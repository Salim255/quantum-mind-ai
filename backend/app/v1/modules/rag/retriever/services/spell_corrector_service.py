from dataclasses import dataclass
from typing import Set

from symspellpy import SymSpell, Verbosity

from app.v1.modules.rag.loader.concept_tagger import CONCEPTS


@dataclass(slots=True)
class SpellCorrectionResult:
    """
    Result returned by the spell correction service.

    Attributes
    ----------
    corrected_query : str
        Query after correction.

    was_corrected : bool
        Indicates whether any correction occurred.

    needs_clarification : bool
        Indicates whether the query is too ambiguous
        to safely process.

    clarification_message : str | None
        Message that can be shown to the user when
        clarification is required.
    """

    corrected_query: str
    was_corrected: bool
    needs_clarification: bool
    clarification_message: str | None = None


class SpellCorrectorService:
    """
    DOMAIN-AWARE SPELL CORRECTION SERVICE
    ====================================

    PURPOSE
    -------
    Correct misspelled quantum-computing terminology before
    concept tagging and retrieval occur.

    WHY SYMSPELL
    ------------
    RapidFuzz is a fuzzy matcher.

    SymSpell is a true spell-correction engine based on
    edit distance and dictionary lookup.

    Example:

        entangelment
            -> entanglement

        teleportaion
            -> teleportation

        hadmard
            -> hadamard

        spn
            -> spin

    while avoiding unstable matches such as:

        spn -> p
    """

    # ------------------------------------------------------------
    # CONFIGURATION
    # ------------------------------------------------------------
    MIN_QUERY_LENGTH = 2

    MIN_TERM_LENGTH = 3

    MAX_EDIT_DISTANCE = 2

    # ------------------------------------------------------------
    # BUILD DOMAIN VOCABULARY
    # ------------------------------------------------------------
    # We build a clean dictionary from:
    #
    #   - anchors
    #   - keywords_soft
    #
    # Single-character terms are excluded from
    # spell correction because they produce unstable
    # results.
    # ------------------------------------------------------------
    _VOCABULARY: Set[str] = set()

    for concept in CONCEPTS.values():

        for term in concept.get("anchors", []):

            if (
                isinstance(term, str)
                and len(term.strip()) >= MIN_TERM_LENGTH
            ):
                _VOCABULARY.add(term.strip().lower())

        for term in concept.get("keywords_soft", []):

            if (
                isinstance(term, str)
                and len(term.strip()) >= MIN_TERM_LENGTH
            ):
                _VOCABULARY.add(term.strip().lower())

    # ------------------------------------------------------------
    # BUILD SYMSPELL DICTIONARY
    # ------------------------------------------------------------
    _SYMSPELL = SymSpell(
        max_dictionary_edit_distance=MAX_EDIT_DISTANCE,
        prefix_length=7,
    )

    for term in _VOCABULARY:

        # Frequency value is required by SymSpell.
        #
        # Since we have no corpus frequencies,
        # every concept receives the same weight.
        _SYMSPELL.create_dictionary_entry(term, 1)

    @classmethod
    def correct(
        cls,
        query: str,
    ) -> SpellCorrectionResult:
        """
        Correct a user query.

        Parameters
        ----------
        query : str
            Original user query.

        Returns
        -------
        SpellCorrectionResult
        """

        # --------------------------------------------------------
        # STEP 1: BASIC VALIDATION
        # --------------------------------------------------------
        query = query.strip()

        if not query:

            return SpellCorrectionResult(
                corrected_query=query,
                was_corrected=False,
                needs_clarification=True,
                clarification_message=(
                    "Please provide a question."
                ),
            )

        # --------------------------------------------------------
        # STEP 2: SINGLE CHARACTER QUERIES
        # --------------------------------------------------------
        # Examples:
        #
        #   s
        #   x
        #   ?
        #
        # These should never enter retrieval.
        # --------------------------------------------------------
        if len(query) <= cls.MIN_QUERY_LENGTH:

            return SpellCorrectionResult(
                corrected_query=query,
                was_corrected=False,
                needs_clarification=True,
                clarification_message=(
                    "Could you provide more details "
                    "about your question?"
                ),
            )

        # --------------------------------------------------------
        # STEP 3: TOKENIZE QUERY
        # --------------------------------------------------------
        words = query.split()

        corrected_words: list[str] = []

        was_corrected = False

        # --------------------------------------------------------
        # STEP 4: CORRECT UNKNOWN WORDS
        # --------------------------------------------------------
        for word in words:

            normalized_word = word.lower()

            # ----------------------------------------------------
            # KEEP KNOWN TERMS
            # ----------------------------------------------------
            if normalized_word in cls._VOCABULARY:

                corrected_words.append(word)

                continue

            # ----------------------------------------------------
            # SKIP VERY SHORT TOKENS
            # ----------------------------------------------------
            if len(normalized_word) < cls.MIN_TERM_LENGTH:

                corrected_words.append(word)

                continue

            # ----------------------------------------------------
            # SYMSPELL LOOKUP
            # ----------------------------------------------------
            suggestions = cls._SYMSPELL.lookup(
                normalized_word,
                Verbosity.TOP,
                max_edit_distance=cls.MAX_EDIT_DISTANCE,
            )

            # ----------------------------------------------------
            # NO CORRECTION FOUND
            # ----------------------------------------------------
            if not suggestions:

                corrected_words.append(word)

                continue

            best_match = suggestions[0]

            corrected_term = best_match.term

            if corrected_term != normalized_word:

                corrected_words.append(corrected_term)

                was_corrected = True

            else:

                corrected_words.append(word)

        # --------------------------------------------------------
        # STEP 5: REBUILD QUERY
        # --------------------------------------------------------
        corrected_query = " ".join(corrected_words)

        return SpellCorrectionResult(
            corrected_query=corrected_query,
            was_corrected=was_corrected,
            needs_clarification=False,
        )