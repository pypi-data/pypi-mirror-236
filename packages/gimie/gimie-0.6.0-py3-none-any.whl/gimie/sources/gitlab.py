from __future__ import annotations
from dataclasses import dataclass
import os
import requests
from datetime import datetime
from dateutil.parser import isoparse
from functools import cached_property
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse
from dotenv import load_dotenv
from calamus import fields
from calamus.schema import JsonLDSchema
from rdflib import Graph
import tempfile
from gimie.graph.namespaces import SDO
from gimie.io import RemoteResource
from gimie.models import (
    Organization,
    OrganizationSchema,
    Person,
    PersonSchema,
)
from gimie.sources.abstract import Extractor
from gimie.sources.common.queries import send_graphql_query, send_rest_query

load_dotenv()


@dataclass
class GitlabExtractor(Extractor):
    """Extractor for Gitlab repositories. Uses the Gitlab GraphQL API to
    extract metadata into linked data.
    url: str
        The url of the git repository.
    base_url: Optional[str]
        The base url of the git remote.

    """

    url: str
    base_url: Optional[str] = None
    local_path: Optional[str] = None

    token: Optional[str] = None
    name: Optional[str] = None
    identifier: Optional[str] = None
    author: Optional[List[Union[Organization, Person]]] = None
    contributors: Optional[List[Person]] = None
    prog_langs: Optional[List[str]] = None
    description: Optional[str] = None
    date_created: Optional[datetime] = None
    date_modified: Optional[datetime] = None
    date_published: Optional[datetime] = None
    version: Optional[str] = None
    keywords: Optional[List[str]] = None
    source_organization: Optional[Organization] = None
    download_url: Optional[str] = None
    license: Optional[List[str]] = None

    def to_graph(self) -> Graph:
        """Convert repository to RDF graph."""
        jd = GitlabExtractorSchema().dumps(self)
        g: Graph = Graph().parse(format="json-ld", data=str(jd))
        g.bind("schema", SDO)
        return g

    def list_files(self) -> List[RemoteResource]:
        """takes the root repository folder and returns the list of files present"""
        file_list = []
        file_dict = self._repo_data["repository"]["tree"]["blobs"]["nodes"]
        defaultbranchref = self._repo_data["repository"]["rootRef"]
        for item in file_dict:
            file = RemoteResource(
                name=item["name"],
                url=f'{self.url}/-/raw/{defaultbranchref}/{item["name"]}',
                headers=self._set_auth(),
            )
            file_list.append(file)
        return file_list

    def extract(self):
        """Extract metadata from target Gitlab repository."""

        # fetch metadata
        data = self._repo_data

        # Each Gitlab project has a unique identifier (integer)
        self.identifier = urlparse(data["id"]).path.split("/")[2]
        # at the moment, Gimie fetches only the group directly related to the project
        # the group takes the form: parent/subgroup
        self.source_organization = self._safe_extract_group(data)
        self.description = data["description"]
        self.prog_langs = [lang["name"] for lang in data["languages"]]
        self.date_created = isoparse(data["createdAt"][:-1])
        self.date_modified = isoparse(data["lastActivityAt"][:-1])
        if data["releases"]["edges"]:
            self.date_published = isoparse(
                data["releases"]["edges"][0]["node"]["releasedAt"]
            )
        self.license = self._get_licenses()
        self.keywords = data["topics"]

        # Get contributors as the project members that are not owners and those that have written merge requests
        # owners are either multiple individuals or a group, if not user is marked as owner
        self.author = self._safe_extract_author(data)
        # contributors are project members or merge request authors
        self.contributors = self._safe_extract_contributors(data)

        if data["releases"] and (len(data["releases"]["edges"]) > 0):
            # go into releases and take the name from the first node (most recent)
            self.version = data["releases"]["edges"][0]["node"]["name"]
            self.download_url = f"{self.url}/-/archive/{self.version}/{self.path.split('/')[-1]}-{self.version}.tar.gz"

    def _safe_extract_group(
        self, repo: Dict[str, Any]
    ) -> Optional[Organization]:
        """Extract the group from a GraphQL repository node if it has one."""
        if (self.path is not None) and (repo["group"] is not None):
            repo["group"]["name"] = "/".join(self.path.split("/")[0:-1])
            return self._get_organization(repo["group"])
        return None

    def _safe_extract_author(
        self, repo: Dict[str, Any]
    ) -> List[Union[Person, Organization]]:
        """Extract the author from a GraphQL repository node.
        projectMembers is used if available, otherwise the author
        is inferred from the project url."""
        members = repo["projectMembers"]["edges"]
        if len(members) > 0:
            owners = filter(
                lambda m: m["node"]["accessLevel"]["stringValue"] == "OWNER",
                members,
            )
            return [
                self._get_author(owner["node"]["user"]) for owner in owners
            ]

        if repo["group"] is not None:
            return [self._get_author(repo["group"])]

        # If the author is absent from the GraphQL response (permission bug),
        # fallback to the REST API
        return [self._user_from_rest(self.path.split("/")[0])]

    def _safe_extract_contributors(
        self, repo: dict[str, Any]
    ) -> List[Person] | None:
        members = [
            user["node"]["user"]
            for user in repo["projectMembers"]["edges"]
            if user["node"]["accessLevel"]["stringValue"] != "OWNER"
        ]
        merge_request_authors = [
            author["node"]["author"]
            for author in repo["mergeRequests"]["edges"]
        ]
        contributors = members + merge_request_authors
        # Drop duplicate (unhashable) dicts by "id" key
        uniq_contrib = list({c["id"]: c for c in contributors}.values())
        return [self._get_user(contrib) for contrib in uniq_contrib]

    @cached_property
    def _repo_data(self) -> Dict[str, Any]:
        """Fetch repository metadata from GraphQL endpoint."""
        data = {"path": self.path}
        project_query = """
        query project_query($path: ID!) {
            project(fullPath: $path) {
                name
                id
                description
                createdAt
                lastActivityAt
                group {
                    id
                    name
                    description
                    avatarUrl
                    webUrl
                }
                languages {
                    name
                    share
                }
                topics
                projectMembers {
                    edges {
                        node {
                        id
                        accessLevel {
                            stringValue
                        }
                        user {
                            id
                            name
                            username
                            publicEmail
                            webUrl
                        }
                        }
                    }
                }
                mergeRequests{
                    edges {
                    node {
                        author {
                        id
                        name
                        username
                        publicEmail
                        webUrl
                        }
                    }
                    }
                }
                repository {
                    rootRef
                    tree{
                    blobs{
                        nodes {
                            name
                            webUrl
                          }}}}
                releases {
                    edges {
                    node {
                        name
                        releasedAt
                    }
                    }
                }
        }
        }
        """
        response = send_graphql_query(
            self.graphql_endpoint, project_query, data, self._set_auth()
        )
        if "errors" in response:
            raise ValueError(response["errors"])

        return response["data"]["project"]

    def _set_auth(self) -> Any:
        """Set authentication headers for Gitlab API requests."""
        try:
            if not self.token:
                self.token = os.environ.get("GITLAB_TOKEN")
                assert self.token
            headers = {"Authorization": f"token {self.token}"}

            login = requests.get(f"{self.rest_endpoint}/user", headers=headers)
            assert login.json().get("login")
        except AssertionError:
            return {}
        else:
            return headers

    def _get_author(self, node: Dict[str, Any]) -> Union[Organization, Person]:
        """Given the GraphQL node for a repository owner,
        return the author as a Person or Organization object."""
        # Is this the best test?
        if "username" in node:
            return self._get_user(node)
        return self._get_organization(node)

    def _get_organization(self, node: Dict[str, Any]) -> Organization:
        """Extract details from a GraphQL organization node."""
        return Organization(
            _id=node["webUrl"],
            name=node["name"],
            description=node.get("description"),
            logo=node.get("avatarUrl"),
        )

    def _get_user(self, node: Dict[str, Any]) -> Person:
        """Extract details from a GraphQL user node."""
        return Person(
            _id=node["webUrl"],
            identifier=node["username"],
            name=node.get("name"),
            email=node.get("publicEmail"),
        )

    def _user_from_rest(self, username: str) -> Person:
        """Given a username, use the REST API to retrieve the Person object."""

        author = send_rest_query(
            self.rest_endpoint,
            f"/users?username={username}",
            self._set_auth(),
        )
        if isinstance(author, list):
            author = author[0]

        return Person(
            _id=author["web_url"],
            identifier=author["username"],
            name=author.get("name"),
        )

    @property
    def rest_endpoint(self) -> str:
        return f"{self.base}/api/v4/"

    @property
    def graphql_endpoint(self) -> str:
        return f"{self.base}/api"


class GitlabExtractorSchema(JsonLDSchema):
    """This defines the schema used for json-ld serialization."""

    _id = fields.Id()
    path = fields.String(SDO.name)
    identifier = fields.String(SDO.identifier)
    source_organization = fields.Nested(SDO.isPartOf, OrganizationSchema)
    author = fields.Nested(
        SDO.author, [PersonSchema, OrganizationSchema], many=True
    )
    contributors = fields.Nested(SDO.contributor, PersonSchema, many=True)
    prog_langs = fields.List(SDO.programmingLanguage, fields.String)
    download_url = fields.Raw(SDO.downloadUrl)
    description = fields.String(SDO.description)
    date_created = fields.Date(SDO.dateCreated)
    date_modified = fields.Date(SDO.dateModified)
    date_published = fields.Date(SDO.datePublished)
    license = fields.List(SDO.license, fields.IRI)
    url = fields.IRI(SDO.codeRepository)
    keywords = fields.List(SDO.keywords, fields.String)
    version = fields.String(SDO.version)

    class Meta:
        rdf_type = SDO.SoftwareSourceCode
        model = GitlabExtractor
        add_value_types = False
