from typing import List

from pydantic import validate_arguments

from ..config import PermitConfig
from .base import BasePermitApi, ensure_context, pagination_params
from .context import ApiKeyLevel
from .models import (
    APIKeyRead,
    EnvironmentCopy,
    EnvironmentCreate,
    EnvironmentRead,
    EnvironmentStats,
    EnvironmentUpdate,
)


class EnvironmentsApi(BasePermitApi):
    def __init__(self, config: PermitConfig):
        super().__init__(config)
        self.__environments = self._build_http_client("")

    @ensure_context(ApiKeyLevel.PROJECT_LEVEL_API_KEY)
    @validate_arguments
    async def list(
        self, project_key: str, page: int = 1, per_page: int = 100
    ) -> List[EnvironmentRead]:
        """
        Retrieves a list of environments.

        Args:
            params: The filters and pagination options.

        Returns:
            an array of EnvironmentRead objects representing the listed environments.

        Raises:
            PermitApiError: If the API returns an error HTTP status code.
            PermitContextError: If the configured ApiContext does not match the required endpoint context.
        """
        return await self.__environments.get(
            f"/v2/projects/{project_key}/envs",
            model=List[EnvironmentRead],
            params=pagination_params(page, per_page),
        )

    @ensure_context(ApiKeyLevel.PROJECT_LEVEL_API_KEY)
    @validate_arguments
    async def get(self, project_key: str, environment_key: str) -> EnvironmentRead:
        """
        Gets an environment by project key and environment key.

        Args:
            project_key: The project key.
            environment_key: The environment key.

        Returns:
            an EnvironmentRead object representing the retrieved environment.

        Raises:
            PermitApiError: If the API returns an error HTTP status code.
            PermitContextError: If the configured ApiContext does not match the required endpoint context.
        """
        return await self.__environments.get(
            f"/v2/projects/{project_key}/envs/{environment_key}", model=EnvironmentRead
        )

    @ensure_context(ApiKeyLevel.PROJECT_LEVEL_API_KEY)
    @validate_arguments
    async def get_by_key(
        self, project_key: str, environment_key: str
    ) -> EnvironmentRead:
        """
        Gets an environment by project key and environment key.
        Alias for the get method.

        Args:
            project_key: The project key.
            environment_key: The environment key.

        Returns:
            an EnvironmentRead object representing the retrieved environment.

        Raises:
            PermitApiError: If the API returns an error HTTP status code.
            PermitContextError: If the configured ApiContext does not match the required endpoint context.
        """
        return await self.get(project_key, environment_key)

    @ensure_context(ApiKeyLevel.PROJECT_LEVEL_API_KEY)
    @validate_arguments
    async def get_by_id(self, project_id: str, environment_id: str) -> EnvironmentRead:
        """
        Gets an environment by project ID and environment ID.
        Alias for the get method.

        Args:
            project_id: The project ID.
            environment_id: The environment ID.

        Returns:
            an EnvironmentRead object representing the retrieved environment.

        Raises:
            PermitApiError: If the API returns an error HTTP status code.
            PermitContextError: If the configured ApiContext does not match the required endpoint context.
        """
        return await self.get(project_id, environment_id)

    @ensure_context(ApiKeyLevel.PROJECT_LEVEL_API_KEY)
    @validate_arguments
    async def get_stats(
        self, project_key: str, environment_key: str
    ) -> EnvironmentStats:
        """
        Retrieves statistics and metadata for an environment.

        Args:
            project_key: The project key.
            environment_key: The environment key.

        Returns:
            an EnvironmentStats object representing the statistics data.

        Raises:
            PermitApiError: If the API returns an error HTTP status code.
            PermitContextError: If the configured ApiContext does not match the required endpoint context.
        """
        return await self.__environments.get(
            f"/v2/projects/{project_key}/envs/{environment_key}/stats",
            model=EnvironmentStats,
        )

    @ensure_context(ApiKeyLevel.PROJECT_LEVEL_API_KEY)
    @validate_arguments
    async def get_api_key(self, project_key: str, environment_key: str) -> APIKeyRead:
        """
        Retrieves the API key that grants access for an environment.

        Args:
            project_key: The project key.
            environment_key: The environment key.

        Returns:
            an APIKeyRead object containing the API key and its metadata.

        Raises:
            PermitApiError: If the API returns an error HTTP status code.
            PermitContextError: If the configured ApiContext does not match the required endpoint context.
        """
        return await self.__environments.get(
            f"/v2/api-key/{project_key}/{environment_key}",
            model=APIKeyRead,
        )

    @ensure_context(ApiKeyLevel.PROJECT_LEVEL_API_KEY)
    @validate_arguments
    async def create(
        self, project_key: str, environment_data: EnvironmentCreate
    ) -> EnvironmentRead:
        """
        Creates a new environment.

        Args:
            project_key: The project key.
            environment_data: The data for creating the environment.

        Returns:
            an EnvironmentRead object representing the created environment.

        Raises:
            PermitApiError: If the API returns an error HTTP status code.
            PermitContextError: If the configured ApiContext does not match the required endpoint context.
        """
        return await self.__environments.post(
            f"/v2/projects/{project_key}/envs",
            model=EnvironmentRead,
            json=environment_data,
        )

    @ensure_context(ApiKeyLevel.PROJECT_LEVEL_API_KEY)
    @validate_arguments
    async def update(
        self,
        project_key: str,
        environment_key: str,
        environment_data: EnvironmentUpdate,
    ) -> EnvironmentRead:
        """
        Updates an existing environment.

        Args:
            project_key: The project key.
            environment_key: The environment key.
            environment_data: The data for updating the environment.

        Returns:
            an EnvironmentRead object representing the updated environment.

        Raises:
            PermitApiError: If the API returns an error HTTP status code.
            PermitContextError: If the configured ApiContext does not match the required endpoint context.
        """
        return await self.__environments.patch(
            f"/v2/projects/{project_key}/envs/{environment_key}",
            model=EnvironmentRead,
            json=environment_data,
        )

    @ensure_context(ApiKeyLevel.PROJECT_LEVEL_API_KEY)
    @validate_arguments
    async def copy(
        self, project_key: str, environment_key: str, copy_params: EnvironmentCopy
    ) -> EnvironmentRead:
        """
        Clones data from a source specified environment into a different target environment in the same project.

        Args:
            project_key: The project key.
            environment_key: The environment key.
            copy_params: The parameters for copying the environment.

        Returns:
            an EnvironmentRead object representing the copied environment.

        Raises:
            PermitApiError: If the API returns an error HTTP status code.
            PermitContextError: If the configured ApiContext does not match the required endpoint context.
        """
        return await self.__environments.post(
            f"/v2/projects/{project_key}/envs/{environment_key}/copy",
            model=EnvironmentRead,
            json=copy_params,
        )

    @ensure_context(ApiKeyLevel.PROJECT_LEVEL_API_KEY)
    @validate_arguments
    async def delete(self, project_key: str, environment_key: str) -> None:
        """
        Deletes an environment.

        Args:
            project_key: The project key.
            environment_key: The environment key.

        Raises:
            PermitApiError: If the API returns an error HTTP status code.
            PermitContextError: If the configured ApiContext does not match the required endpoint context.
        """
        return await self.__environments.delete(
            f"/v2/projects/{project_key}/envs/{environment_key}"
        )
