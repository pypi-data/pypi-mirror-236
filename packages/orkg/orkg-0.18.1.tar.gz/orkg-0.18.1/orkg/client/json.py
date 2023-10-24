from typing import Dict, List, Union

from orkg.out import OrkgResponse
from orkg.utils import NamespacedClient, simcomp_available


class JSONClient(NamespacedClient):
    @simcomp_available
    def save_json(
        self, resource_id: str, json_object: Union[Dict, List]
    ) -> OrkgResponse:
        return self.client.wrap_response(
            self.client.simcomp.visualization.POST(
                json={"resourceId": resource_id, "jsonData": json_object}
            )
        )

    @simcomp_available
    def get_json(self, resource_id: str) -> OrkgResponse:
        params = f"?resourceId={resource_id}"
        return self.client.wrap_response(self.client.simcomp.visualization.GET(params))
