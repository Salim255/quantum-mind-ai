import PyPDF2


def load_pdf(path: str) -> str:
    """
    ROBUST PDF LOADER FOR RAG SYSTEMS
    ==================================

    PURPOSE:
    --------
    Extract text from PDFs in a way that preserves:
    - structure (critical for chunking)
    - traceability (debugging missing content)
    - stability (avoid silent data loss)

    WHY THIS MATTERS IN RAG:
    ------------------------
    If extraction is bad:
    → embeddings become incomplete
    → retrieval misses keywords
    → downstream AI appears "dumb"

    This layer is the FOUNDATION of your RAG system.
    """

    # ------------------------------------------------------------
    # Store extracted text page by page
    # ------------------------------------------------------------
    # WHY:
    # We do NOT flatten immediately because:
    # - page structure helps debugging
    # - helps detect missing or corrupted pages
    # - improves chunk alignment later
    pages_text = []

    # ------------------------------------------------------------
    # Open PDF file in binary mode
    # ------------------------------------------------------------
    # WHY:
    # PDFs are binary structured documents.
    # Reading in text mode would corrupt parsing.
    with open(path, "rb") as f:

        # --------------------------------------------------------
        # Create PDF reader object
        # --------------------------------------------------------
        # WHAT IT DOES:
        # Parses PDF structure and exposes pages
        #
        # IMPORTANCE:
        # This is the core parser of PyPDF2
        # Everything depends on this step
        reader = PyPDF2.PdfReader(f)

        # --------------------------------------------------------
        # Iterate through all pages in the PDF
        # --------------------------------------------------------
        # WHY PAGE LOOP IS CRITICAL:
        # - preserves logical document segmentation
        # - helps detect missing pages
        # - improves chunking consistency
        for page_index, page in enumerate(reader.pages):

            try:
                # ------------------------------------------------
                # Extract text from a single page
                # ------------------------------------------------
                # WHAT IT DOES:
                # Converts PDF layout into raw text
                #
                # PROBLEM:
                # - may lose layout
                # - may reorder text
                # - may drop characters in complex PDFs
                #
                # WHY WE STILL USE IT:
                # It is the simplest baseline extractor.
                text = page.extract_text()

                # ------------------------------------------------
                # HANDLE EMPTY EXTRACTION SAFELY
                # ------------------------------------------------
                # WHY:
                # Some PDFs return None or empty strings.
                # If we skip silently → we lose data without knowing.
                #
                # IMPACT IF REMOVED:
                # - silent missing content
                # - invisible retrieval failures
                if not text:
                    pages_text.append(
                        f"\n[PAGE_{page_index}_EMPTY]\n"
                    )
                    continue

                # ------------------------------------------------
                # ADD PAGE MARKER BEFORE TEXT
                # ------------------------------------------------
                # WHY THIS IS IMPORTANT:
                # - preserves document structure
                # - helps chunker avoid mixing pages
                # - improves traceability in debugging
                #
                # IMPACT IF REMOVED:
                # - harder to debug missing info
                # - chunks may merge unrelated pages
                pages_text.append(
                    f"\n[PAGE_{page_index}]\n{text}"
                )

            except Exception as e:
                # ------------------------------------------------
                # SAFE FAILURE HANDLING
                # ------------------------------------------------
                # WHY:
                # PDF parsing is fragile.
                # Some pages may crash extraction.
                #
                # IF WE DO NOTHING:
                # → pipeline fails silently OR crashes
                #
                # IF WE SKIP:
                # → we lose traceability
                #
                # BEST PRACTICE:
                # Keep explicit error marker
                print(f"The error====->: \n{e}")
                pages_text.append(
                    f"\n[PAGE_{page_index}_ERROR]\n"
                )


    # ------------------------------------------------------------
    # FINAL MERGE OF ALL PAGES
    # ------------------------------------------------------------
    # WHY:
    # We unify all pages into a single text stream for:
    # - cleaning stage
    # - chunking stage
    #
    # IMPORTANT:
    # We DO NOT clean here to avoid double-processing.
    #
    # CLEANING MUST BE A SEPARATE STAGE.
    return "\n".join(pages_text)