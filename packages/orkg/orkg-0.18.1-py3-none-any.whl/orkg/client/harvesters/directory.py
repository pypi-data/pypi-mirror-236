import json
import os
from typing import Any, List, Optional, Union

from orkg.client.harvesters.utils import process_contribution
from orkg.common import OID
from orkg.out import OrkgResponse


def harvest(
    orkg_client: Any,
    directory: str,
    research_field: Union[str, OID],
    title: str,
    doi: Optional[str] = None,
    authors: Optional[List[str]] = None,
    publication_year: Optional[int] = None,
    published_in: Optional[str] = None,
    **kwargs,
) -> OrkgResponse:
    # Check if the directory exists
    if not os.path.isdir(directory):
        raise ValueError(f"The directory {directory} does not exist.")

    # Check if the directory contains any json files
    if not any(file.endswith(".json") for file in os.listdir(directory)):
        raise ValueError(f"The directory {directory} does not contain any json files.")

    # Check if research field is valid
    if isinstance(research_field, str):
        rf_response = orkg_client.resources.get(q=research_field, exact=True, size=1)
        if not rf_response.succeeded or len(rf_response.content) == 0:
            raise ValueError(
                f"Unable to find the ORKG research field with the given string value {research_field}"
            )
        research_field = OID(rf_response.content[0]["id"])

    # Prepare the paper object
    paper_json = {"title": title, "researchField": f"{research_field.id}"}
    if doi is not None:
        paper_json["doi"] = doi
    if authors is not None:
        paper_json["authors"] = [
            {"label": author} for author in authors if isinstance(author, str)
        ]
    if publication_year is not None:
        paper_json["publicationYear"] = str(publication_year)
    if published_in is not None:
        paper_json["publishedIn"] = published_in
    if "contributions" not in paper_json:
        paper_json["contributions"] = []
    for key, value in kwargs.items():
        paper_json[key] = value

    # Read all json files in the directory
    contribution_content = []
    for file in os.listdir(directory):
        if not file.endswith(".json"):
            continue
        with open(os.path.join(directory, file)) as f:
            contribution_content.append(json.load(f))

    # Process the contribution content
    for contribution_json in contribution_content:
        orkg_contribution_json = {}
        global_ids = {}
        context = contribution_json.get("@context", {})
        process_contribution(
            contribution_json, orkg_contribution_json, global_ids, context
        )
        # replace the key "label" with "name"
        orkg_contribution_json["name"] = orkg_contribution_json.pop("label")
        paper_json["contributions"].append(orkg_contribution_json)

    # Now that we have everything, let's finalize the paper object and add it to the graph
    paper_json = {"paper": paper_json}
    return orkg_client.papers.add(paper_json)
