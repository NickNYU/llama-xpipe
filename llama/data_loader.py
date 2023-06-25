import os
import pickle
from abc import abstractmethod, ABC
from typing import Optional, Sequence, List

from llama_hub.github_repo import GithubRepositoryReader, GithubClient
from llama_index import download_loader
from llama_index.readers.schema.base import Document


class WikiLoader(ABC):
    @abstractmethod
    def load(self) -> List[Document]:
        pass


class GithubLoader(WikiLoader):
    def __init__(
            self,
            github_owner: Optional[str] = None,
            repo: Optional[str] = None,
            dirs: Optional[Sequence[str]] = None,
    ):
        super().__init__()
        self.owner = (
            github_owner if github_owner is not None else os.environ["GITHUB_OWNER"]
        )
        self.repo = repo if repo is not None else os.environ["GITHUB_REPO"]
        self.dirs = dirs if dirs is not None else [".", "doc"]

    def load(self) -> List[Document]:
        download_loader("GithubRepositoryReader")
        docs = None
        if os.path.exists("docs/docs.pkl"):
            with open("docs/docs.pkl", "rb") as f:
                docs = pickle.load(f)

        if docs is not None:
            return docs

        # otherwise, we download from github and save it locally
        github_client = GithubClient(os.getenv("GITHUB_TOKEN"))
        loader = GithubRepositoryReader(
            github_client,
            # owner="ctripcorp",
            owner=self.owner,
            # repo="x-pipe",
            repo=self.repo,
            filter_directories=(self.dirs, GithubRepositoryReader.FilterType.INCLUDE),
            filter_file_extensions=([".md"], GithubRepositoryReader.FilterType.INCLUDE),
            verbose=True,
            concurrent_requests=10,
        )

        docs = loader.load_data(branch="master")

        with open("docs/docs.pkl", "wb") as f:
            pickle.dump(docs, f)

        return docs