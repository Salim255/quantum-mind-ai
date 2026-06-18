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
from app.v1.modules.ingestion.dto.chunker_dto import ChunkDTO
from app.v1.modules.ingestion.dto.text_dto import ContentBlockDTO

class RAGChunker:
    @classmethod
    # ------------------------------------------------------------------
    # MAIN ENTRY POINT
    # ------------------------------------------------------------------
    def semantic_chunk_text(
        cls,
        extracted__sections_texts: list[ContentBlockDTO],
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
        chunks: list[ChunkDTO] = []
        paragraphs: list[ContentBlockDTO] = []

        for section_text in  extracted__sections_texts:

            # --------------------------------------------------------------
            # STEP 1:
            # Split into semantic paragraphs.
            # --------------------------------------------------------------
            paragraphs.extend(cls.split_into_paragraphs(section_text.content))
           
            # --------------------------------------------------------------
            # STEP 2:
            # Build semantic chunks from sentence groups.
            # --------------------------------------------------------------

            chunks.extend(cls.build_semantic_chunks(
                paragraphs,
                max_chars,
                overlap_sentences
            ))

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
    def split_into_paragraphs(content_block: ContentBlockDTO) -> List[ContentBlockDTO]:
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
        section_paragraphs: List[ContentBlockDTO] = []

        paragraphs: list[str] = re.split(r"\n\s*\n", content_block.content)

        for text in  paragraphs:
            cleaned = text.strip()

            if not cleaned:
                continue

            section_paragraphs.append(ContentBlockDTO(
                bookmark_title=content_block.bookmark_title,
                section_title=content_block.section_title,
                order=content_block.order,
                content=text,
                source_name=content_block.source_name
            ))
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
        return section_paragraphs

    # ------------------------------------------------------------------
    # SEMANTIC CHUNK CONSTRUCTION
    # ------------------------------------------------------------------
    @classmethod
    def build_semantic_chunks(
        cls,
        content_blocks: List[ContentBlockDTO],
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
        for content_block in content_blocks:

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
            sentences = sent_tokenize(content_block.content)

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
                        content_block,
                        current_chunk_sentences
                    )

                    # Never store empty chunks.
                    if chunk:
                        chunks.append(
                            ChunkDTO(
                                content=chunk,
                                concept=content_block.section_title,
                                bookmark_title=content_block.bookmark_title,
                                order=content_block.order,
                                length=len(chunk),
                                source_name=content_block.source_name
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
                    content=final_chunk,
                    concept=content_block.section_title,
                    length=len(final_chunk)
                )
            )

        return chunks


    # ------------------------------------------------------------------
    # FINAL CLEANUP
    # ------------------------------------------------------------------
    @staticmethod
    def cleanup_chunks(chunks: List["ChunkDTO"]) -> List["ChunkDTO"]:
        """
        FINAL QUALITY GATE FOR CHUNKS
        =============================

        PURPOSE
        -------
        Remove low-quality chunks before embedding.

        IMPORTANT DESIGN RULE
        ---------------------
        This step MUST NOT modify semantic structure.
        It only filters or lightly normalizes.
        """

        cleaned: List["ChunkDTO"] = []

        for chunk in chunks:

            text = chunk.text

            # --------------------------------------------------------
            # 1. LIGHT NORMALIZATION (SAFE ONLY)
            # --------------------------------------------------------
            # WHY:
            # Fix accidental spacing issues without destroying structure
            #
            # NOTE:
            # We do NOT collapse newlines fully here anymore
            text = re.sub(r"[ \t]+", " ", text)

            # --------------------------------------------------------
            # 2. LENGTH FILTER (QUALITY CONTROL)
            # --------------------------------------------------------
            # WHY THIS EXISTS:
            # Very small chunks:
            # - lack semantic context
            # - produce weak embeddings
            #
            # BUT WARNING:
            # threshold must be carefully tuned
            if len(text) < 60:
                continue

            # --------------------------------------------------------
            # 3. PRESERVE ORIGINAL METADATA
            # --------------------------------------------------------
            # WHY:
            # Avoid recomputation bugs and inconsistencies
            cleaned.append(
                ChunkDTO(
                    text=text,
                    concept=chunk.concept,
                    length=len(text)
                )
            )

        return cleaned
        
    # ------------------------------------------------------------------
    # CHUNK FINALIZATION
    # ------------------------------------------------------------------
    @staticmethod
    def finalize_chunk(
        length: int,
        content_block: ContentBlockDTO,
        sentences: List[str]
    ) -> ChunkDTO | None:
        """
        Convert sentence list into a final chunk string.
        """ 
        
        chunk =  " ".join(sentences).strip()

        if len(chunk) == 0:
            return None
        
        return ChunkDTO(
            content=chunk,
            concept=content_block.section_title,
            length=length,
            bookmark_title=content_block.bookmark_title,
            order=content_block.order,
            source_name=content_block.source_name
        )

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
