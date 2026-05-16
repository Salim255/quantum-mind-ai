import re
# re = Python regular expressions module.
# We use it to search/remove unwanted patterns from raw PDF text.


def clean_text(text: str) -> str:
    """
    Clean raw PDF text before chunking + embeddings.

    WHY THIS MATTERS
    ----------------
    PDFs usually contain a lot of noise:
    - page numbers
    - repeated headers
    - copyright text
    - acknowledgements
    - LaTeX equations
    - broken formatting

    If we store this noisy text in the vector database,
    retrieval quality becomes poor.

    Good RAG systems depend heavily on clean chunks.
    """

    # -------------------------------------------------------------------------
    # 1. Remove LaTeX math blocks
    # -------------------------------------------------------------------------
    # Removes:
    #   $x^2 + y^2$
    #   $$E = mc^2$$
    #
    # flags=re.DOTALL allows matching across multiple lines.
    text = re.sub(
        r'\${1,2}.*?\${1,2}',
        ' ',
        text,
        flags=re.DOTALL
    )

    # -------------------------------------------------------------------------
    # 2. Remove citation patterns
    # -------------------------------------------------------------------------
    # Removes:
    #   [1]
    #   [42]
    #
    # These are common in academic books/papers and add noise.
    text = re.sub(r'\[\d+\]', ' ', text)

    # -------------------------------------------------------------------------
    # 3. Remove isolated page numbers
    # -------------------------------------------------------------------------
    # Removes lines like:
    #
    #   12
    #
    # or:
    #
    #      87
    #
    # These often appear between pages after PDF extraction.
    text = re.sub(
        r'\n\s*\d+\s*\n',
        '\n',
        text
    )

    # -------------------------------------------------------------------------
    # 4. Remove common PDF/book noise
    # -------------------------------------------------------------------------
    # These patterns are not useful for semantic search.
    #
    # Examples:
    #   "All Rights Reserved"
    #   "Table of Contents"
    #   repeated introduction headers
    #
    # IMPORTANT:
    # Add more patterns over time as you discover noisy text.
    noise_patterns = [

        r'All Rights Reserved',

        r'Table of Contents',

        r'Introduction Introduction Introduction',

        r'Acknowledg(e)?ments?',
    ]

    # Loop through every pattern and remove it.
    for pattern in noise_patterns:

        text = re.sub(
            pattern,
            ' ',
            text,
            flags=re.IGNORECASE
        )

    # -------------------------------------------------------------------------
    # 5. Normalize spaces WITHOUT destroying paragraphs
    # -------------------------------------------------------------------------
    # VERY IMPORTANT:
    #
    # We only normalize spaces/tabs.
    #
    # We DO NOT remove all newlines,
    # because paragraph structure helps semantic chunking.
    #
    # BAD:
    #   re.sub(r'\s+', ' ', text)
    #
    # That destroys all paragraph boundaries.
    text = re.sub(r'[ \t]+', ' ', text)

    # -------------------------------------------------------------------------
    # 6. Normalize excessive empty lines
    # -------------------------------------------------------------------------
    # Converts:
    #
    #   \n\n\n\n\n
    #
    # into:
    #
    #   \n\n
    #
    # This keeps readable paragraph separation.
    text = re.sub(
        r'\n{3,}',
        '\n\n',
        text
    )

    # -------------------------------------------------------------------------
    # 7. Final cleanup
    # -------------------------------------------------------------------------
    # strip() removes leading/trailing whitespace.
    return text.strip()