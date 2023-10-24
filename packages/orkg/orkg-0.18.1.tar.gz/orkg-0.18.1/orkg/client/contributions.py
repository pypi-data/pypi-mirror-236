from ast import literal_eval
from collections import defaultdict
from typing import Dict, List, Optional, Tuple, Union
from urllib.parse import parse_qs, urlparse

import pandas as pd

from orkg.out import OrkgResponse
from orkg.utils import NamespacedClient, simcomp_available


class ContributionsClient(NamespacedClient):
    @simcomp_available
    def similar(self, cont_id: str) -> OrkgResponse:
        """
        Get contributions which are similar to a specified contribution.
        Returns contribution ID, contribution label, paper ID, and similarity score.

        :param cont_id: contribution ID
        :return: OrkgResponse object of similar contributions
        """
        self.client.simcomp._append_slash = True
        response = self.client.simcomp.similar(cont_id).GET()
        return self.client.wrap_response(response=response)

    @simcomp_available
    def compare(
        self, contributions: List[str], response_hash: str = None
    ) -> OrkgResponse:
        """
        Get comparison by list of contribution IDs.

        :param contributions: list of contribution IDs
        :param response_hash: hashed URL of contribution (optional)
        :return: OrkgResponse object of the comparison
        """
        self.client.simcomp._append_slash = False
        params = f'?contributions={",".join(contributions)}'
        if response_hash is not None:
            params = f"{params}&response_hash={response_hash}"
        response = self.client.simcomp.compare.GET(params)
        return self.client.wrap_response(response=response)

    def _get_contributions_from_comparison(
        self, comparison_id: str
    ) -> Tuple[List[str], Optional[str], List[str]]:
        """
        Get contribution IDs of a comparison.

        :param comparison_id: ID of comparison
        :return:
            - single string of all contribution IDs from the comparison
            - string of hashed URL of contribution or None
            - list of comparison properties displayed in the UI
        """
        resource = self.client.resources.by_id(comparison_id).content
        if "Comparison" not in resource["classes"]:
            raise ValueError("This id is not for a comparison")
        response = self.client.json.get_json(resource_id=comparison_id).content
        query_params = parse_qs(urlparse(response["data"]["url"]).query)
        return (
            query_params["contributions"][0].split(","),
            query_params["response_hash"][0],
            query_params["properties"][0].split(",")
            if "properties" in query_params
            else [],
        )

    @simcomp_available
    def compare_dataframe(
        self,
        contributions: List[str] = None,
        comparison_id: str = None,
        like_ui=True,
        include_meta=False,
    ) -> Union[pd.DataFrame, Tuple[pd.DataFrame, pd.DataFrame]]:
        """
        Convert an ORKG comparison into a DataFrame.
        Optional: create a second DataFrame of contribution metadata.
        Included metadata (when present): author, doi, publication month, publication year, url, research field, venue

        :param contributions: list of contribution IDs from a comparison
        :param comparison_id: ID of a comparison
        :param like_ui: true/false whether to match comparison df to its UI representation
        :param include_meta: true/false whether to return metadata df
        :return:
            - comparison DataFrame
            - metadata DataFrame (optional)
        """
        # check if valid request
        if contributions is None and comparison_id is None:
            raise ValueError("either provide the contributions, or the comparison ID")
        # get OrkgResponse object
        response, ui_props = self._get_response(comparison_id, contributions)
        if not response.succeeded:
            return pd.DataFrame()
        content = response.content
        # extract necessary components for making dataframe
        (
            columns,
            contribution_ids_and_titles,
            contributions_list,
            property_lookup,
        ) = self._extract_components(content)
        # create table representation of the data
        data = content["data"]
        indices, rows = self._get_data_rows_and_indices(data, property_lookup)
        # create data frame from table rows and indices
        df = pd.DataFrame(rows, columns=columns, index=indices)
        if like_ui and len(ui_props) > 0:
            df = self._make_df_like_ui(df, property_lookup, ui_props)
        if include_meta:
            return df, self._create_metadata_df(
                columns, contribution_ids_and_titles, contributions_list
            )
        return df

    def _get_response(
        self, comparison_id: Optional[str], contributions: Optional[List]
    ) -> Tuple[OrkgResponse, List]:
        """
        Get an OrkgResponse object for a comparison by comparison ID or list of contributions IDs.

        :param comparison_id: ID of a comparison
        :param contributions: list of contribution IDs from a comparison
        :return:
            - OrkgResponse object of the comparison
            - list of comparison properties displayed in the UI
        """
        response_hash = None
        ui_props = []
        if comparison_id is not None:
            (
                contributions,
                response_hash,
                ui_props,
            ) = self._get_contributions_from_comparison(comparison_id)
        response = self.compare(
            contributions=contributions, response_hash=response_hash
        )
        return response, ui_props

    @staticmethod
    def _extract_components(
        content: Dict[str, Union[List, Dict]]
    ) -> Tuple[List[str], Dict[str, str], List[Dict], Dict[str, str]]:
        """
        Get information about contributions; create lookup dictionary for property IDs to labels; create column headings.

        :param content: OrkgResponse content
        :return:
            - list of headings for df columns
            - dictionary of contribution IDs to headings: Paper Title/Contribution N (Contribution ID)
            - list of contribution dictionaries containing contribution label, ID, paper ID, title, and year
            - dictionary of property IDs to property labels
        """
        contributions_list = content["contributions"]
        contribution_ids_and_titles = {
            contribution[
                "id"
            ]: f"{contribution['title']}/{contribution['contributionLabel']} ({contribution['id']})"
            for contribution in contributions_list
        }
        columns = [
            contribution_ids_and_titles[contribution["id"]]
            for contribution in contributions_list
        ]
        properties_list = content["properties"]
        property_lookup = {prop["id"]: prop["label"] for prop in properties_list}
        return columns, contribution_ids_and_titles, contributions_list, property_lookup

    def _get_data_rows_and_indices(
        self, data: Dict[str, List], property_lookup: Dict[str, str]
    ) -> Tuple[List, List]:
        """
        Convert comparison data into lists representing rows and indices corresponding to table representation of comparison.

        :param data: OrkgResponse.content['data']
        :param property_lookup: dictionary of property IDs to property labels
        :return:
            - list of comparison properties for the index
            - list of rows, with each row as a list of cell values
        """
        indices = []
        rows = []
        for prop_id, values in data.items():
            indices.append(property_lookup[prop_id])
            row = []
            for index, value in enumerate(values):
                if not value[0]:
                    row.append("")
                else:
                    if len(value) == 1:
                        row.append(self._get_cell_value(value[0]))
                    else:
                        cell = []
                        # Rather than parsing it in a list comprehension that might fail
                        # Then the whole list will be typed as strings, we parse it one item at a time
                        for v in value:
                            cell.append(self._get_cell_value(v))
                        row.append(cell)
            rows.append(row)
        return indices, rows

    @staticmethod
    def _get_cell_value(
        cell_dict: Dict[str, Union[str, List]]
    ) -> Union[str, float, int, bool]:
        """
        Convert cell value to appropriate Python datatype.

        :param cell_dict: dictionary of info for each cell.
        :return: cell value as a string, float, int, or bool.
        """
        try:
            # Try parse each value by itself
            value = literal_eval(cell_dict["label"].capitalize())
        except (SyntaxError, ValueError):
            # If it fails, that means it is a string
            value = cell_dict["label"]
        return value

    @staticmethod
    def _make_df_like_ui(
        df: pd.DataFrame, property_lookup: Dict[str, str], ui_props: List[str]
    ) -> pd.DataFrame:
        """
        Make the comparison DataFrame match the comparison as it appears in the UI by removing properties that aren't displayed and putting the rows in the same order.

        :param df: comparison DataFrame
        :param property_lookup: dictionary of property IDs to property labels
        :param ui_props: list of comparison properties displayed in the UI
        :return: comparison DataFrame
        """
        # remove props that are not displayed
        df = df.drop(
            [p_lbl for p_id, p_lbl in property_lookup.items() if p_id not in ui_props]
        )
        # order df rows by ui props order
        df = df.reindex([property_lookup[p] for p in ui_props if p in property_lookup])
        return df

    def _create_metadata_df(
        self,
        columns: List[str],
        contribution_ids_and_titles: Dict[str, str],
        contributions_list: List[Dict],
    ) -> pd.DataFrame:
        """
        Create a metadata DataFrame containing the following properties (when available):
            author, doi, publication month, publication year, url, research field, venue
        Column headings are identical to the comparison DataFrame.

        :param columns: list of headings for df columns
        :param contribution_ids_and_titles: dictionary of contribution IDs to headings: Paper Title/Contribution N (Contribution ID)
        :param contributions_list: list of contribution dictionaries containing contribution label, ID, paper ID, title, and year
        :return: metadata DataFrame
        """
        paper_set = set(
            [f"{contribution['paperId']}" for contribution in contributions_list]
        )
        comparison_meta_data = {}
        # create dict of meta properties and values
        for paper in paper_set:
            contribution_ids, paper_meta_data = self._get_paper_metadata(
                contributions_list, paper
            )
            # add paper meta info for each contribution to comparison meta info
            for contribution_id in contribution_ids:
                column_name = contribution_ids_and_titles[contribution_id]
                paper_dict = paper_meta_data.copy()
                comparison_meta_data[column_name] = paper_dict
                comparison_meta_data[column_name]["contribution id"] = contribution_id
        # Make dataframe with same column order as comparison df and replace missing fields with empty string
        df_meta = pd.DataFrame.from_dict(comparison_meta_data)[columns].fillna("")
        return df_meta

    def _get_paper_metadata(
        self, contributions_list: List[Dict], paper: str
    ) -> Tuple[List, Dict]:
        """
        Get metadata info for a paper.

        :param contributions_list: list of contribution dictionaries containing contribution label, ID, paper ID, title, and year
        :param paper: ID of the paper
        :return:
            - list of IDs of contributions belonging to this paper
            - dictionary of (available) paper metadata properties to values
        """
        # author, doi, publication month, publication year, url, research field, venue
        meta_property_ids = ["P27", "P26", "P28", "P29", "url", "P30", "HAS_VENUE"]
        paper_meta_dict_of_lists = defaultdict(list)
        paper_statements = self.client.statements.get_by_subject_unpaginated(
            subject_id=paper
        )
        for statement in paper_statements.content:
            if statement["predicate"]["id"] in meta_property_ids:
                pred = statement["predicate"]["label"]
                obj = statement["object"]["label"]
                paper_meta_dict_of_lists[pred].append(obj)
        # make dict values strings if only one and list of strings if two or more
        paper_meta_data = {
            k: v.pop() if len(v) == 1 else v
            for k, v in paper_meta_dict_of_lists.items()
        }
        paper_meta_data["title"] = paper_statements.content[0]["subject"]["label"]
        paper_meta_data["paper id"] = paper
        # get IDs of all contributions from this paper which are included in the comparison
        contribution_ids = [
            str(contribution["id"])
            for contribution in contributions_list
            if contribution["paperId"] == paper
        ]
        return contribution_ids, paper_meta_data
