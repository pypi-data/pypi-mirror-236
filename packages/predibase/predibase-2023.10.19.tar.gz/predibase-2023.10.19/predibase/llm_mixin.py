from abc import abstractmethod
from typing import Dict, List, Union

from tabulate import tabulate

from predibase.pql.api import Session
from predibase.resource.connection import Connection
from predibase.resource.dataset import Dataset
from predibase.resource.llm import interface


class LlmMixin:
    session: Session

    def LLM(self, uri: str) -> Union["interface.HuggingFaceLLM", "interface.LLMDeployment"]:
        if uri.startswith("pb://deployments/"):
            return interface.LLMDeployment(self.session, uri[len("pb://deployments/") :])

        if uri.startswith("hf://"):
            return interface.HuggingFaceLLM(self.session, uri[len("hf://") :])

        raise ValueError(
            "must provide either a Hugging Face URI (hf://<...>) "
            "or a Predibase deployments URI (pb://deployments/<name>).",
        )

    def get_supported_llms(self):
        """Returns a list of supported HuggingFace LLMs."""
        data = self.session.get_json("/supported_llms")
        return data

    _simple_table_keys = ["name", "modelName", "deploymentStatus", "isShared"]

    def list_llm_deployments(self, active_only=False, print_as_table=True) -> Union[List[Dict], None]:
        """Fetches the current list of all LLM deployments regardless of status. Can either return this list or
        print it as a concise table. Can also optionally filter by active deployments.

        Returns: List of LLMDeployment objects or None
        """
        llms: List[Dict] = self.session.get_json(f'/llms?activeOnly={"true" if active_only else "false"}')
        if print_as_table:
            compressed_llms = [{k: llm[k] for k in self._simple_table_keys} for llm in llms]
            print(tabulate(compressed_llms, headers="keys", tablefmt="fancy_grid"))
        else:
            return llms

    @abstractmethod
    def get_dataset(self) -> Dataset:
        pass

    @abstractmethod
    def list_connections(self) -> List[Connection]:
        pass
