from data.repositories.ai_profile_repository_impl import AIProfileRepositoryImpl
from data.services.ai_service_provider_impl import AIServiceProviderImpl
from data.services.git_service_impl import GitServiceImpl
from domain.use_cases.create_ai_profile import CreateAIProfileUseCase
from domain.use_cases.delete_ai_profile import DeleteAIProfileUseCase
from domain.use_cases.generate_commit_message import GenerateCommitMessageUseCase
from domain.use_cases.set_active_ai_profile import SetActiveAIProfileUseCase
from domain.use_cases.update_ai_profile import UpdateAIProfileUseCase
from presentation.controllers.create_ai_profile import CreateAIProfileController
from presentation.controllers.delete_ai_profile import DeleteAIProfileController
from presentation.controllers.git_commit import GitCommitController
from presentation.controllers.list_ai_profiles import ListAIProfilesController
from presentation.controllers.update_ai_profile import UpdateAIProfileController
from presentation.controllers.use_ai_profile import UseAIProfileController
from presentation.routers.ai_profile import AIProfileRouter
from presentation.routers.app import AppRouter
from presentation.routers.git_commit import GitCommitRouter

if __name__ == "__main__":
    # repositories
    ai_profile_repositroy = AIProfileRepositoryImpl()

    # services
    ai_service_provider = AIServiceProviderImpl()
    git_service = GitServiceImpl()

    # use cases
    create_ai_profile_use_case = CreateAIProfileUseCase(ai_profile_repositroy)
    delete_ai_profile_use_case = DeleteAIProfileUseCase(ai_profile_repositroy)
    generate_commit_message_use_case = GenerateCommitMessageUseCase(
        git_service, ai_profile_repositroy, ai_service_provider
    )
    set_active_ai_profile_use_case = SetActiveAIProfileUseCase(ai_profile_repositroy)
    update_ai_profile_use_case = UpdateAIProfileUseCase(ai_profile_repositroy)

    # controllers
    create_ai_profile_controller = CreateAIProfileController(
        ai_profile_repositroy, create_ai_profile_use_case
    )
    delete_ai_profile_controller = DeleteAIProfileController(
        ai_profile_repositroy, delete_ai_profile_use_case
    )
    git_commit_controller = GitCommitController(generate_commit_message_use_case)
    list_ai_profiles_controller = ListAIProfilesController(ai_profile_repositroy)
    update_ai_profile_controller = UpdateAIProfileController(
        ai_profile_repositroy, update_ai_profile_use_case
    )
    use_ai_profile_controller = UseAIProfileController(
        ai_profile_repositroy, set_active_ai_profile_use_case
    )

    # routers
    ai_profile_router = AIProfileRouter(
        create_ai_profile_controller,
        list_ai_profiles_controller,
        update_ai_profile_controller,
        delete_ai_profile_controller,
        use_ai_profile_controller,
    )
    git_commit_router = GitCommitRouter(git_commit_controller)
    app_router = AppRouter(ai_profile_router(), git_commit_router())
    app = app_router()
    app()
