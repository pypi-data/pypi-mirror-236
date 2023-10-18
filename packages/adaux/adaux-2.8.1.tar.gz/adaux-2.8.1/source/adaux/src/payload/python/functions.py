# pylint: disable=relative-beyond-top-level
import dataclasses as dc
import functools
import os
import re
import typing as tp

from ...._components._payload._docker_executors import subprocess_run
from ...._components._payload._docker_executors import tag_image
from ...._components._payload._docker_executors import upload_to_remote
from ...._gitlab import ApiRequestCommunicator
from ...._logging import logger
from ...._proto_namespace import _ProtoNamespace


def check_release_notes(aux: _ProtoNamespace) -> None:
    release_notes = aux.project.release_notes
    version = aux.project.version
    # check that version has a note
    if version not in release_notes:
        raise RuntimeError(f"version {version} is not in release notes, please add!")
    # check that version was not already released
    out = subprocess_run(
        ["git", "ls-remote", "--tags"], check=True, capture_output=True
    )
    already_released = list(re.findall(r"tags/([\d.]+)\n", out.stdout.decode()))
    if version in already_released:
        raise RuntimeError(
            f"version {version} was already released and cannot be released again!"
        )

    print(f"version {version} has description '{release_notes[version]}'")


def gitlab_release(aux: _ProtoNamespace) -> None:
    release_notes = aux.project.release_notes
    version = aux.project.version
    description = release_notes[version]
    os.environ["RELEASE_TAG"] = version
    os.environ["RELEASE_DESCRIPTION"] = description
    payload = aux.payload.lookup["gitlab-release-run"]
    payload.run()


@dc.dataclass(frozen=True)
class TagVariables:
    aux: _ProtoNamespace

    @functools.cached_property
    def version(self) -> str:
        res: str = self.aux.project.version
        return res

    @functools.cached_property
    def branch(self) -> str:
        res: str = self.aux.gitlab.current_branch
        return res

    @functools.cached_property
    def ci_adaux_image(self) -> str:
        res: str = self.aux.versions.ci_adaux_image
        return res

    @functools.cached_property
    def commit_tag(self) -> str:
        res = os.environ.get("CI_COMMIT_TAG", "")
        if res:
            return res
        reason = "empty" if "CI_COMMIT_TAG" in os.environ else "inexistent"
        raise ValueError(f"commit_tag is {reason}")

    @functools.cached_property
    def autoincr(self) -> str:
        coord = [
            "projects",
            os.environ["CI_PROJECT_ID"],
            "repository",
            "tags",
        ]
        api = ApiRequestCommunicator()
        token = os.environ["GITLAB_READ_API"]
        api.headers = {"PRIVATE-TOKEN": token}
        api.base_url = "https://" + os.environ["CI_SERVER_HOST"]
        params = dict(
            order_by="version",
        )
        res = api.api_request(*coord, params=params)
        for x in res:
            logger.info("tag %s available", x["name"])
        for x in res:
            # get the first tag that matches the format
            version = x["name"]
            regex = r"(v)?(\d+)\.(\d+)\.(\d+)"
            match = re.match(regex, version)

            if match:
                _, major, minor, patch = match.groups()
                return f"{major}.{minor}.{int(patch)+1}"

        raise ValueError(f"no tag adheres to {regex}")

    def __getitem__(self, key: str) -> str:
        res: str = getattr(self, key)
        return res


def tag(
    aux: _ProtoNamespace,  # pylint: disable=unused-argument
    deps: tp.Any,
    tags: tp.Union[str, tp.Sequence[str]],  # pylint: disable=redefined-outer-name
) -> None:
    if isinstance(tags, str):
        tags = [tags]

    last_local_tag = ""
    valid_variables = TagVariables(aux)
    for dep in deps:
        for tag in tags:  # pylint: disable=redefined-outer-name
            tag = tag.format_map(valid_variables)
            local_tag, release_tag = dep.executor.tag_and_upload(tag)
            if last_local_tag != local_tag:
                last_local_tag = local_tag
                msg = "uploaded" if dep.executor.remote_exists() else "  tagged"
                print(msg, local_tag)
            print("   -> to", release_tag)


def gittag(
    aux: _ProtoNamespace,
    deps: tp.Any,
    tags: tp.Union[str, tp.Sequence[str], None] = None,
) -> None:
    if tags is None:
        # get it from the deps
        assert len(deps) == 1
        dep = deps[0]
        tags = dep.param["tags"]

    if isinstance(tags, str):
        tags = [tags]

    valid_variables = TagVariables(aux)
    for tag_ in tags:
        tag_ = tag_.format_map(valid_variables)
        subprocess_run(["git", "tag", "-f", tag_])
        url = os.environ["CI_REPOSITORY_URL"]
        protocol, rest = url.split("//", 1)
        _, rest = rest.split("@", 1)
        url = f"{protocol}//__token__:{os.environ['GITLAB_WRITE_REPOSITORY']}@{rest}"
        subprocess_run(["git", "push", url, tag_])


def img_dockerhub(
    aux: _ProtoNamespace,
    deps: tp.Any,
    release_tag: str,
) -> None:
    if len(deps) != 1:
        raise RuntimeError(
            f"img-dockerhub job for {release_tag} should have exactly 1 dependency, not {len(deps)}!"
        )
    valid_variables = TagVariables(aux)
    release_tag = release_tag.format_map(valid_variables)
    local_tag = deps[0].executor.pull_if_not_existent()
    tag_image(local_tag, release_tag)
    subprocess_run(
        [
            "docker",
            "login",
            "-u",
            os.environ["DOCKERHUB_USERNAME"],
            "-p",
            os.environ["DOCKERHUB_PASSWORD"],
            "docker.io",
        ]
    )
    upload_to_remote(local_tag, release_tag)
    subprocess_run(["docker", "logout", "docker.io"])
    print("uploaded", local_tag)
    print("   -> to", release_tag)
