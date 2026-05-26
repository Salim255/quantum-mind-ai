# rag/loader/chunker.py
# ------------------------------------------------------------------
# SEMANTIC CHUNKER FOR EDUCATIONAL RAG SYSTEMS
# ------------------------------------------------------------------
#
# PURPOSE
# -------
# This module transforms large educational text into smaller,
# semantically meaningful chunks.
#
# These chunks are later:
# - embedded into vectors
# - stored in the vector database
# - retrieved during semantic search
#
# WHY CHUNKING MATTERS
# --------------------
# Large language models and embedding models work best when text is:
#
# - coherent
# - focused
# - semantically meaningful
#
# BAD CHUNKS:
# - broken words
# - mixed topics
# - random character slices
# - isolated fragments
#
# GOOD CHUNKS:
# - one idea
# - one explanation
# - one concept
# - meaningful educational context
#
# This file implements a production-style semantic chunking pipeline.
# ------------------------------------------------------------------
from nltk.tokenize import sent_tokenize
import nltk
import re
# Python regular expression module.
# Used for:
# - whitespace normalization
# - sentence splitting
# - cleanup operations

from typing import List
# Type hint support for cleaner, safer code.


# Download the "punkt" model only once (NLTK sentence tokenizer data)
# This is a pre-trained model that helps NLTK understand where sentences start and end.
# It is NOT just splitting on ".", but uses language patterns (abbreviations, decimals, etc.).
nltk.download("punkt")
nltk.download("punkt_tab")

from app.v1.modules.rag.loader.concept_tagger import detect_concept
from app.v1.modules.rag.dto.chunk_dto import ChunkDTO

class RAGChunker:
    @classmethod
    # ------------------------------------------------------------------
    # MAIN ENTRY POINT
    # ------------------------------------------------------------------
    def semantic_chunk_text(
        cls,
        normalized_text: str,
        max_chars: int = 600,
        overlap_sentences: int = 2
    ) -> List[ChunkDTO]:
        """
        Main semantic chunking pipeline.

        PARAMETERS
        ----------
        text : str
            The normalized educational text.

        max_chars : int
            Maximum approximate chunk size.

        overlap_sentences : int
            Number of sentences preserved between chunks.

        RETURNS
        -------
        List[str]
            List of semantic chunks.

        PIPELINE
        --------
        1. Normalize text
        2. Split into paragraphs
        3. Build semantic chunks
        4. Clean final chunks
        """

        # --------------------------------------------------------------
        # STEP 1:
        # Split into semantic paragraphs.
        # --------------------------------------------------------------
        paragraphs: List[str] = cls.split_into_paragraphs(normalized_text)

        # --------------------------------------------------------------
        # STEP 2:
        # Build semantic chunks from sentence groups.
        # --------------------------------------------------------------
        chunks = cls.build_semantic_chunks(
            paragraphs,
            max_chars,
            overlap_sentences
        )

        # --------------------------------------------------------------
        # STEP 4:
        # Final cleanup + noise filtering.
        # --------------------------------------------------------------
        return cls.cleanup_chunks(chunks)


        # ------------------------------------------------------------------
        # TEXT NORMALIZATION
        # ------------------------------------------------------------------

    @staticmethod
    def normalize_chunk_text(text: str) -> str:
        """
        Normalize whitespace while preserving semantic structure.

        IMPORTANT:
        We preserve paragraph boundaries because they help
        maintain semantic meaning during chunking.
        """

        # Replace repeated spaces/tabs with a single space.
        text = re.sub(r"[ \t]+", " ", text)

        # Normalize excessive empty lines.
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()


    # ------------------------------------------------------------------
    # PARAGRAPH SPLITTING
    # ------------------------------------------------------------------
    @staticmethod
    def split_into_paragraphs(text: str) -> List[str]:
        """
        PARAGRAPH SPLITTER FOR RAG PIPELINE
        ====================================

        PURPOSE
        -------
        Split cleaned text into paragraph-level semantic units.

        WHY THIS STEP EXISTS
        --------------------
        In RAG systems, paragraphs often represent:
        - a single idea
        - a single explanation
        - a coherent semantic unit

        This makes them ideal building blocks for chunking.

        IMPORTANT:
        This is NOT final chunking.
        It is only a semantic segmentation step.
        """

        # ------------------------------------------------------------
        # 1. SPLIT TEXT INTO PARAGRAPHS
        # ------------------------------------------------------------
        # WHY THIS EXISTS:
        # After cleaning, most PDFs use blank lines (\n\n)
        # to separate logical paragraphs.
        #
        # WHAT THIS DOES:
        # Splits text wherever there is a paragraph break.
        #
        # PATTERN EXPLANATION:
        # \n\s*\n means:
        # - newline
        # - optional spaces
        # - another newline
        #
        # WHY THIS IS BETTER THAN simple "\n\n":
        # - handles messy PDFs with spaces between newlines
        # - more robust to extraction noise
        #
        # WHAT HAPPENS IF REMOVED:
        # - no paragraph structure
        # - chunking becomes arbitrary
        # - embeddings lose semantic grouping
        paragraphs = re.split(r"\n\s*\n", text)

        # ------------------------------------------------------------
        # 2. CLEAN AND FILTER EMPTY PARAGRAPHS
        # ------------------------------------------------------------
        # WHY THIS EXISTS:
        # PDF extraction often produces:
        # - empty strings
        # - whitespace-only blocks
        # - noise from page formatting
        #
        # WHAT THIS DOES:
        # - removes empty paragraphs
        # - trims whitespace around text
        #
        # WHY STRIP IS IMPORTANT:
        # Without strip():
        # - you may keep "fake paragraphs"
        # - chunking becomes noisy
        #
        # WHAT HAPPENS IF REMOVED:
        # - empty chunks
        # - useless embeddings
        # - degraded retrieval quality
        return [
            p.strip()
            for p in paragraphs
            if len(p.strip()) > 0
        ]

    # ------------------------------------------------------------------
    # SEMANTIC CHUNK CONSTRUCTION
    # ------------------------------------------------------------------
    @classmethod
    def build_semantic_chunks(
        cls,
        paragraphs: List[str],
        max_chars: int,
        overlap_sentences: int
    ) -> List[ChunkDTO]:
        """
        Build coherent semantic chunks.

        STRATEGY
        --------
        We accumulate sentences until:
        - chunk size exceeds max_chars

        Then:
        - finalize the chunk
        - preserve overlap sentences
        - continue building the next chunk

        WHY OVERLAP MATTERS
        -------------------
        Overlap preserves context continuity between chunks.

        This improves:
        - embeddings
        - semantic retrieval
        - final RAG answer quality
        """

        # Final chunk storage.
        chunks: List[ChunkDTO] = []

        # Sentences currently being accumulated.
        current_chunk_sentences: List[str] = []

        # Current chunk size tracker.
        current_chunk_length = 0

        # --------------------------------------------------------------
        # Process every paragraph.
        # --------------------------------------------------------------
        for paragraph in paragraphs:

            # Split paragraph into sentences.
            # Split a long text into a list of clean sentences
            # Example:
            # "Dr. Smith went home. He was tired."
            # → ["Dr. Smith went home.", "He was tired."]
            #
            # Why this is important for RAG:
            # - Keeps semantic meaning intact
            # - Prevents breaking sentences in the middle
            # - Produces cleaner chunks for embedding and retrieval
            sentences = sent_tokenize(paragraph)

            # ----------------------------------------------------------
            # Process every sentence.
            # ----------------------------------------------------------
            for sentence in sentences:

                sentence_length = len(sentence)

                # ------------------------------------------------------
                # Determine if adding this sentence would exceed
                # the maximum chunk size.
                # ------------------------------------------------------
                exceeds_limit = (
                    current_chunk_length + sentence_length > max_chars
                )

                # ------------------------------------------------------
                # If chunk limit exceeded:
                # finalize current chunk.
                # ------------------------------------------------------
                if exceeds_limit and current_chunk_sentences:

                    chunk = cls.finalize_chunk(
                        current_chunk_sentences
                    )

                    # Never store empty chunks.
                    if chunk:
                        chunks.append(
                            ChunkDTO(
                                text=chunk,
                                concept=detect_concept(chunk),
                                length=len(chunk)
                                )
                            )

                    # --------------------------------------------------
                    # Create semantic overlap.
                    # --------------------------------------------------
                    current_chunk_sentences = cls.create_overlap(
                        current_chunk_sentences,
                        overlap_sentences
                    )

                    # Add current sentence to new chunk.
                    current_chunk_sentences.append(sentence)

                    # Recalculate chunk size.
                    current_chunk_length = cls.calculate_chunk_length(
                        current_chunk_sentences
                    )

                else:
                    # Continue accumulating semantic content.
                    current_chunk_sentences.append(sentence)

                    current_chunk_length += sentence_length

        # --------------------------------------------------------------
        # Add the final chunk.
        # --------------------------------------------------------------
        final_chunk = cls.finalize_chunk(current_chunk_sentences)

        if final_chunk:
            chunks.append(
                ChunkDTO(
                    text=final_chunk,
                    concept=detect_concept(final_chunk),
                    length=len(final_chunk)
                )
            )

        return chunks


    # ------------------------------------------------------------------
    # FINAL CLEANUP
    # ------------------------------------------------------------------
    @staticmethod
    def cleanup_chunks(chunks: List[ChunkDTO]) -> List[ChunkDTO]:
        """
        Final cleanup before embedding/storage.

        OPERATIONS
        ----------
        - normalize spaces
        - remove tiny/noisy chunks

        WHY REMOVE TINY CHUNKS?
        -----------------------
        Very small chunks often:
        - lack context
        - reduce retrieval quality
        - create noisy embeddings
        """

        cleaned: List[ChunkDTO] = []

        for chunk in chunks:

            # Normalize whitespace.
            text = re.sub(r"\s+", " ", chunk.text).strip()

            # Skip tiny chunks.
            if len(text) > 80:

                cleaned.append(
                    ChunkDTO(
                        text=text,
                        concept=chunk.concept,
                        length=len(text))
                    )

        return cleaned
    
    # ------------------------------------------------------------------
    # CHUNK FINALIZATION
    # ------------------------------------------------------------------
    @staticmethod
    def finalize_chunk(sentences: List[str]) -> str:
        """
        Convert sentence list into a final chunk string.
        """

        return " ".join(sentences).strip()


    # ------------------------------------------------------------------
    # SEMANTIC OVERLAP
    # ------------------------------------------------------------------
    @staticmethod
    def create_overlap(
        sentences: List[str],
        overlap_sentences: int
    ) -> List[str]:
        """
        Create semantic overlap between chunks.

        IMPORTANT:
        We overlap FULL sentences instead of raw characters.

        WHY?
        ----
        Character overlap can:
        - cut words
        - break semantics
        - damage embeddings

        Sentence overlap preserves meaning.
        """

        if overlap_sentences <= 0:
            return []

        return sentences[-overlap_sentences:]


    # ------------------------------------------------------------------
    # CHUNK LENGTH CALCULATION
    # ------------------------------------------------------------------
    @staticmethod
    def calculate_chunk_length(sentences: List[str]) -> int:
        """
        Calculate total chunk character length.
        """

        return sum(len(s) for s in sentences)
