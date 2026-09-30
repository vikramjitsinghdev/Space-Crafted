from pathlib import Path

from data.collectors.ntrs import NTRSClient

from data.collectors.ntrs_parser import (
    extract_results,
    extract_citation_id,
    extract_title,
)

from data.collectors.document_ranker import (
    rank_documents,
    deduplicate_documents,
)

from data.collectors.download_parser import (
    find_downloads,
    choose_best_download,
)

from data.collectors.document_downloader import (
    DocumentDownloader,
)

from data.extraction.pdf_processor import (
    extract_pages,
)

from data.extraction.passage_extractor import (
    extract_passages,
)

from data.extraction.structured import (
    extract_structured,
)

from data.extraction.ollama import (
    extract_with_ollama,
)

from data.extraction.document_classifier import (
    is_simulation_useful,
)

from data.extraction.equipment_identity import (
    title_matches_equipment,
)

from data.extraction.evidence_scorer import (
    score_evidence,
)

from data.processing.calculations import (
    calculate_all,
)

from data.processing.validator import (
    validate_equipment_data,
)

from data.models.equipment import (
    Equipment,
    Source,
    Provenance,
)

from data.storage.json_store import (
    save_equipment,
)


class EquipmentPipeline:

    def __init__(self):
        self.ntrs = NTRSClient()
        self.downloader = DocumentDownloader()

    # ==========================================================
    # SEARCH
    # ==========================================================

    def search_documents(
        self,
        equipment_name,
        limit=10,
    ):
        print(
            f"\nSearching NASA NTRS for: "
            f"{equipment_name}"
        )

        from data.collectors.query_builder import (
            build_equipment_queries,
        )

        queries = build_equipment_queries(
            equipment_name
        )

        all_results = []

        print(
            "\nRunning targeted NASA searches:"
        )

        for query in queries:

            print(
                f"\n  → {query}"
            )

            try:

                response = self.ntrs.search(
                    query,
                    size=limit,
                )

                results = extract_results(
                    response
                )

                all_results.extend(
                    results
                )

            except Exception as exc:

                print(
                    f"Search failed for "
                    f"'{query}': {exc}"
                )

        ranked = rank_documents(
            all_results,
            extract_title,
            extract_citation_id,
        )

        ranked = deduplicate_documents(
            ranked
        )

        return ranked

    # ==========================================================
    # TEXT EXTRACTION
    # ==========================================================

    def extract_text_document(
        self,
        file_path,
    ):
        """
        Extract text from a plain-text document.
        """

        path = Path(file_path)

        with open(
            path,
            "r",
            encoding="utf-8",
            errors="replace",
        ) as file:

            text = file.read()

        return [
            {
                "page": 1,
                "text": text,
                "character_count": len(text),
            }
        ]

    # ==========================================================
    # DOCUMENT DOWNLOAD
    # ==========================================================

    def download_document(
        self,
        citation_id,
    ):
        """
        Try to retrieve a downloadable artifact
        for an NTRS citation.

        Returns None when no suitable document exists.
        """

        print(
            f"\nChecking downloads for "
            f"citation {citation_id}..."
        )

        citation = self.ntrs.get_citation(
            citation_id
        )

        downloads = self.ntrs.get_downloads(
            citation_id
        )

        candidates = find_downloads(
            downloads
        )

        if not candidates:

            print(
                "No downloadable files available."
            )

            return None

        selected = choose_best_download(
            candidates
        )

        if selected is None:

            print(
                "No suitable document format found."
            )

            return None

        score, download, url = selected

        filename = (
            download.get("name")
            or f"{citation_id}.pdf"
        )

        output_path = (
            Path("data/raw")
            / filename
        )

        download_result = (
            self.downloader.download(
                url,
                str(output_path),
            )
        )

        return {
            "citation": citation,
            "download": download,
            "url": url,
            "path": download_result["path"],
            "file_type": download_result["file_type"],
            "content_type": download_result["content_type"],
            "size_bytes": download_result["size_bytes"],
        }

    # ==========================================================
    # EVIDENCE EXTRACTION
    # ==========================================================

    def extract_evidence(
        self,
        file_path,
        file_type=None,
    ):
        """
        Extract pages/text from a downloaded document
        and find simulation-relevant passages.
        """

        if file_type == "pdf":

            pages = extract_pages(
                file_path
            )

        elif file_type == "txt":

            pages = self.extract_text_document(
                file_path
            )

        else:

            extension = (
                Path(file_path)
                .suffix
                .lower()
            )

            if extension == ".pdf":

                pages = extract_pages(
                    file_path
                )

            elif extension == ".txt":

                pages = self.extract_text_document(
                    file_path
                )

            else:

                raise RuntimeError(
                    f"Unsupported document type: "
                    f"{file_type}"
                )

        passages = extract_passages(
            pages
        )

        return pages, passages

    # ==========================================================
    # DATA EXTRACTION
    # ==========================================================

    def extract_data(
        self,
        passages,
        equipment_name,
    ):
        """
        Extract structured engineering data.

        Deterministic extraction is performed first.
        Ollama is then given the same evidence together with
        the canonical equipment name.
        """

        if not passages:

            return {
                "structured": {},
                "ai": {},
            }

        # Highest-scoring passages first.
        top_passages = passages[:8]

        combined_text = "\n\n".join(
            (
                f"[PAGE {p['page']}]\n"
                f"{p['text']}"
            )
            for p in top_passages
        )

        # ------------------------------------------------------
        # Deterministic extraction
        # ------------------------------------------------------

        print(
            "\nRunning deterministic extraction..."
        )

        structured = extract_structured(
            combined_text
        )

        # ------------------------------------------------------
        # Ollama extraction
        # ------------------------------------------------------

        print(
            "\nRunning Ollama semantic extraction..."
        )

        ai_data = extract_with_ollama(
            combined_text,
            equipment_name,
        )

        return {
            "structured": structured,
            "ai": ai_data,
        }

    # ==========================================================
    # MERGE DATA
    # ==========================================================

    def merge_data(
        self,
        equipment_name,
        document,
        extraction,
        passages,
    ):
        """
        Merge deterministic and AI extraction.

        IMPORTANT:
        equipment_name is always the canonical identity.

        Deterministic extraction gets priority over AI when
        both produce a value for the same field.
        """

        structured = extraction[
            "structured"
        ]

        ai = extraction[
            "ai"
        ]

        data = {}

        fields = [
            "description",
            "mission",
            "manufacturer",
            "category",

            "mass_kg",
            "length_m",
            "width_m",
            "height_m",
            "diameter_m",

            "power_w",
            "voltage_v",

            "operating_temperature_min_c",
            "operating_temperature_max_c",

            "materials",
            "specifications",
        ]

        # ------------------------------------------------------
        # Merge specification fields
        # ------------------------------------------------------

        for field in fields:

            deterministic_value = (
                structured.get(field)
            )

            if deterministic_value is not None:

                data[field] = deterministic_value

                continue

            ai_value = ai.get(field)

            if ai_value is not None:

                data[field] = ai_value

        # ------------------------------------------------------
        # CANONICAL IDENTITY
        # ------------------------------------------------------

        # NEVER take the equipment identity from Ollama.
        #
        # The user's requested name is authoritative.

        data["name"] = equipment_name

        # ------------------------------------------------------
        # Build equipment object
        # ------------------------------------------------------

        equipment = Equipment(

            name=equipment_name,

            description=data.get(
                "description"
            ),

            mission=data.get(
                "mission"
            ),

            manufacturer=data.get(
                "manufacturer"
            ),

            category=data.get(
                "category"
            ),

            mass_kg=data.get(
                "mass_kg"
            ),

            length_m=data.get(
                "length_m"
            ),

            width_m=data.get(
                "width_m"
            ),

            height_m=data.get(
                "height_m"
            ),

            diameter_m=data.get(
                "diameter_m"
            ),

            power_w=data.get(
                "power_w"
            ),

            voltage_v=data.get(
                "voltage_v"
            ),

            operating_temperature_min_c=data.get(
                "operating_temperature_min_c"
            ),

            operating_temperature_max_c=data.get(
                "operating_temperature_max_c"
            ),

            materials=data.get(
                "materials",
                [],
            ),

            specifications=data.get(
                "specifications",
                {},
            ),
        )

        # ------------------------------------------------------
        # Source
        # ------------------------------------------------------

        equipment.sources.append(
            Source(
                title=document["title"],
                citation_id=document[
                    "citation_id"
                ],
                url=document.get("url"),
                source_type="NASA_NTRS",
            )
        )

        # ------------------------------------------------------
        # Derived simulation values
        # ------------------------------------------------------

        equipment.calculated = (
            calculate_all(data)
        )

        # ------------------------------------------------------
        # Provenance
        # ------------------------------------------------------

        evidence = ai.get(
            "evidence",
            {},
        )

        for field, value in data.items():

            if value is None:
                continue

            # IMPORTANT:
            #
            # Check the actual value rather than merely checking
            # whether the key exists.
            #
            # Otherwise every field present in the structured
            # dictionary would incorrectly be labelled
            # deterministic even when its value is None.

            deterministic_value = (
                structured.get(field)
            )

            if deterministic_value is not None:

                source_type = (
                    "NASA_DOCUMENT"
                )

                method = (
                    "deterministic_extraction"
                )

            else:

                source_type = (
                    "AI_EXTRACTED"
                )

                method = (
                    "ollama_semantic_extraction"
                )

            equipment.provenance[field] = (
                Provenance(
                    value=value,
                    provenance_type=source_type,
                    source_title=document[
                        "title"
                    ],
                    source_url=document.get(
                        "url"
                    ),
                    page=None,
                    evidence=evidence.get(
                        field
                    ),
                )
            )

            if method not in equipment.extraction_methods:

                equipment.extraction_methods.append(
                    method
                )

        # ------------------------------------------------------
        # AI involvement
        # ------------------------------------------------------

        equipment.ai_extracted = bool(
            ai
        )

        return equipment

    # ==========================================================
    # MAIN PIPELINE
    # ==========================================================

    def run(
        self,
        equipment_name,
    ):

        print(
            "\n=============================="
        )

        print(
            "SPACECRAFTED EQUIPMENT PIPELINE"
        )

        print(
            "=============================="
        )

        # ======================================================
        # 1. SEARCH NASA NTRS
        # ======================================================

        ranked = self.search_documents(
            equipment_name
        )

        if not ranked:

            raise RuntimeError(
                "No NASA documents found."
            )

        # ======================================================
        # 2. FIND USEFUL DOCUMENT
        # ======================================================

        document = None
        pages = None
        passages = None

        print(
            "\nSearching ranked results for a "
            "downloadable AND simulation-useful "
            "document..."
        )

        for candidate in ranked:

            print(
                "\n--------------------------------"
            )

            print(
                "Evaluating candidate:"
            )

            print(
                candidate["title"]
            )

            print(
                "Score:",
                candidate["score"],
            )

            # --------------------------------------------------
            # Equipment identity check
            # --------------------------------------------------

            if not title_matches_equipment(
                equipment_name,
                candidate["title"],
            ):

                print(
                    "Document title does not identify "
                    "the requested equipment."
                )

                print(
                    "Trying next candidate..."
                )

                continue

            citation_id = candidate[
                "citation_id"
            ]

            if not citation_id:

                print(
                    "No citation ID. Skipping."
                )

                continue

            # --------------------------------------------------
            # Download
            # --------------------------------------------------

            document_info = (
                self.download_document(
                    citation_id
                )
            )

            if document_info is None:

                print(
                    "No downloadable document."
                )

                print(
                    "Trying next candidate..."
                )

                continue

            document = {
                **candidate,
                **document_info,
            }

            print(
                "\nDownloaded:"
            )

            print(
                document["path"]
            )

            # --------------------------------------------------
            # Extract text
            # --------------------------------------------------

            print(
                "\nExtracting document content..."
            )

            try:

                pages, candidate_passages = (
                    self.extract_evidence(
                        document["path"],
                        document.get(
                            "file_type"
                        ),
                    )
                )

            except Exception as exc:

                print(
                    "Document extraction failed:"
                )

                print(exc)

                print(
                    "Trying next candidate..."
                )

                document = None

                continue

            print(
                f"Document pages: "
                f"{len(pages)}"
            )

            print(
                f"Relevant passages: "
                f"{len(candidate_passages)}"
            )

            if not candidate_passages:

                print(
                    "No useful engineering passages."
                )

                print(
                    "Trying next candidate..."
                )

                document = None

                continue

            # --------------------------------------------------
            # Combine evidence
            # --------------------------------------------------

            evidence_text = "\n\n".join(
                passage["text"]
                for passage in candidate_passages
            )

            # --------------------------------------------------
            # Document classifier
            # --------------------------------------------------

            relevance = is_simulation_useful(
                candidate["title"],
                evidence_text,
                equipment_name,
            )

            print(
                "\nDocument classification:"
            )

            print(
                "Type:",
                relevance["document_type"],
            )

            print(
                "Score:",
                relevance["score"],
            )

            print(
                "Categories:",
                relevance["categories"],
            )

            if not relevance["useful"]:

                print(
                    "Document is not sufficiently "
                    "useful for simulation."
                )

                print(
                    "Trying next candidate..."
                )

                document = None

                continue

            # --------------------------------------------------
            # Evidence scorer
            # --------------------------------------------------

            evidence_score = score_evidence(
                evidence_text
            )

            print(
                "\nEvidence score:",
                evidence_score["score"],
            )

            print(
                "Numerical evidence:",
                evidence_score.get(
                    "numerical_evidence",
                    evidence_score.get(
                        "measurements",
                        [],
                    ),
                ),
            )

            if not evidence_score["useful"]:

                print(
                    "Insufficient simulation evidence."
                )

                print(
                    "Trying next candidate..."
                )

                document = None

                continue

            # --------------------------------------------------
            # SUCCESS
            # --------------------------------------------------

            passages = candidate_passages

            print(
                "\nSelected simulation-useful document:"
            )

            print(
                document["title"]
            )

            break

        # ======================================================
        # NO DOCUMENT FOUND
        # ======================================================

        if document is None:

            raise RuntimeError(
                "None of the ranked NASA documents "
                "contained sufficient downloadable "
                "simulation-useful evidence."
            )

        # ======================================================
        # 3. EXTRACT INFORMATION
        # ======================================================

        extraction = (
            self.extract_data(
                passages,
                equipment_name,
            )
        )

        # ======================================================
        # 4. BUILD EQUIPMENT OBJECT
        # ======================================================

        equipment = (
            self.merge_data(
                equipment_name,
                document,
                extraction,
                passages,
            )
        )

        # ======================================================
        # 5. VALIDATE
        # ======================================================

        warnings = (
            validate_equipment_data(
                equipment.to_dict()
            )
        )

        if warnings:

            print(
                "\nValidation warnings:"
            )

            for warning in warnings:

                print(
                    f"- {warning}"
                )

        else:

            print(
                "\nValidation passed."
            )

        # ======================================================
        # 6. SAVE
        # ======================================================

        output_path = save_equipment(
            equipment
        )

        print(
            "\nEquipment saved to:"
        )

        print(
            output_path
        )

        return equipment