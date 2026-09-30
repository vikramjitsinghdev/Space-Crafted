def extract_results(search_response):

    if not isinstance(search_response, dict):
        return []

    # NTRS responses can contain results in different
    # structures, so check the common possibilities.

    if "results" in search_response:
        return search_response["results"]

    if "items" in search_response:
        return search_response["items"]

    collection = search_response.get(
        "collection"
    )

    if isinstance(collection, dict):

        if "items" in collection:
            return collection["items"]

    return []


def extract_citation_id(result):

    if not isinstance(result, dict):
        return None

    possible_fields = [
        "id",
        "citation_id",
        "citationId",
        "ntrs_id",
        "nasa_id"
    ]

    for field in possible_fields:

        value = result.get(field)

        if value:
            return str(value)

    return None


def extract_title(result):

    if not isinstance(result, dict):
        return None

    for field in [
        "title",
        "document_title",
        "name"
    ]:

        value = result.get(field)

        if value:
            return value

    return None