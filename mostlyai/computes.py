from typing import Any

from mostlyai.base import DELETE, GET, POST, _MostlyBaseClient, PATCH
from mostlyai.model import (
    Compute,
)


class _MostlyComputesClient(_MostlyBaseClient):
    SECTION = ["computes"]

    # PUBLIC METHODS #

    def list(self) -> list[Compute]:
        """
        List the available computes, sorted by order index. The first returned compute is the default compute.

        :return: List the available computes
        """
        response = self.request(verb=GET, path=[])
        response = [Compute(**compute) for compute in response]
        return response

    def create(
        self,
        config: dict[str, Any],
    ) -> Compute:
        """
        Create a compute. Only accessible for SuperAdmins.
        The structures of the config and secrets parameters depend on the compute type.
          ```yaml
          - type: KUBERNETES
            config:
              toleration: string
          - type: DATABRICKS
            config:
              instanceURL: string
              clusterID: string
            secrets:
              token: string
          ```
        """
        response = self.request(verb=POST, path=[], json=config, response_type=Compute)
        return response

    def get(self, compute_id: str) -> Compute:
        """
        Retrieve compute.

        :param compute_id: The unique identifier of a compute
        :return: The retrieved compute
        """
        response = self.request(verb=GET, path=[compute_id], response_type=Compute)
        return response

    # PRIVATE METHODS #

    def _update(
        self,
        compute_id: str,
        config: dict[str, Any],
    ) -> Compute:
        response = self.request(
            verb=PATCH,
            path=[compute_id],
            json=config,
            response_type=Compute,
        )
        return response

    def _delete(self, compute_id: str) -> None:
        self.request(verb=DELETE, path=[compute_id])
