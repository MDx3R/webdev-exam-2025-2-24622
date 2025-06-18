from dependency_injector import containers, providers

from application.usecases.recipe.create_recipe_usecase import (
    CreateRecipeUseCase,
)
from application.usecases.recipe.delete_recipe_usecase import (
    DeleteRecipeUseCase,
)
from application.usecases.recipe.get_recipe_by_id_usecase import (
    GetRecipeByIdUseCase,
)
from application.usecases.recipe.list_recipes_usecase import ListRecipesUseCase
from application.usecases.recipe.update_recipe_usecase import (
    UpdateRecipeUseCase,
)
from application.usecases.review.create_review_usecase import (
    CreateReviewUseCase,
)
from application.usecases.user.authenticate_user_usecase import (
    AuthenticateUserUseCase,
)
from application.usecases.user.logout_user_usecase import LogoutUserUseCase
from domain.clock import GlobalClock, SystemClock
from domain.entities.recipe.factories import RecipeFactory, RecipeImageFactory
from domain.entities.review.factories import ReviewFactory
from infrastructure.config.config import Config
from infrastructure.password_hasher.bcrypt_password_hasher import (
    BcryptPasswordHasher,
)
from infrastructure.presentation.presentators.markdown_renderer import (
    MarkdownRenderer,
)
from infrastructure.presentation.sanitizer.bleach_markdown_sanitizer import (
    BleachMarkdownSanitizer,
)
from infrastructure.sqlalchemy.database import Database
from infrastructure.sqlalchemy.query_executor import QueryExecutor
from infrastructure.sqlalchemy.repositories.recipe_repository import (
    SQLAlchemyRecipeRepository,
)
from infrastructure.sqlalchemy.repositories.review_repository import (
    SQLAlchemyReviewRepository,
)
from infrastructure.sqlalchemy.repositories.user_repository import (
    SQLAlchemyUserRepository,
)
from infrastructure.sqlalchemy.transactions import SQLAlchemyTransactionManager
from infrastructure.store.image.local_image_store import LocalImageStore


def session_factory(db: Database):
    return db.get_session_factory()


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["presentation", "run", "infrastrcuture"],
    )

    config = providers.Singleton(Config.load)
    auth_config = config.provided.AUTH
    db_config = config.provided.DB
    file_storage_config = config.provided.FILE

    clock = providers.Singleton(SystemClock)
    GlobalClock.set_clock(clock())

    # ---------------------- Database ----------------------
    database = providers.Singleton(Database, config=db_config)
    session_factory = providers.Singleton(session_factory, database)
    transaction_manager = providers.Singleton(
        SQLAlchemyTransactionManager, session_factory=session_factory
    )
    query_executor = providers.Singleton(QueryExecutor, transaction_manager)

    markdown_renderer = providers.Singleton(MarkdownRenderer)
    markdown_sanitizer = providers.Singleton(BleachMarkdownSanitizer)
    password_hasher = providers.Singleton(BcryptPasswordHasher)

    # ---------------------- Repository ----------------------
    recipe_repo = providers.Singleton(
        SQLAlchemyRecipeRepository, query_executor, transaction_manager
    )
    review_repo = providers.Singleton(
        SQLAlchemyReviewRepository, query_executor, transaction_manager
    )
    user_repo = providers.Singleton(
        SQLAlchemyUserRepository, query_executor, transaction_manager
    )

    # ---------------------- Image Store ----------------------
    image_store = providers.Singleton(
        LocalImageStore, file_storage_config.ACCESS
    )

    # ---------------------- Domain Factory ----------------------
    recipe_factory = providers.Singleton(RecipeFactory)
    recipe_image_factory = providers.Singleton(RecipeImageFactory)
    review_factory = providers.Singleton(ReviewFactory, clock)

    # ---------------------- Use Case ----------------------
    create_recipe_uc = providers.Singleton(
        CreateRecipeUseCase,
        recipe_factory,
        recipe_image_factory,
        recipe_repo,
        image_store,  # TODO
    )
    update_recipe_uc = providers.Singleton(UpdateRecipeUseCase, recipe_repo)
    delete_recipe_uc = providers.Singleton(DeleteRecipeUseCase, recipe_repo)
    get_recipe_uc = providers.Singleton(
        GetRecipeByIdUseCase, recipe_repo, review_repo, user_repo
    )
    list_recipes_uc = providers.Singleton(
        ListRecipesUseCase, recipe_repo, review_repo
    )
    create_review_uc = providers.Singleton(
        CreateReviewUseCase, review_factory, recipe_repo, review_repo
    )
    auth_uc = providers.Singleton(
        AuthenticateUserUseCase, user_repo, password_hasher
    )
    logout_uc = providers.Singleton(LogoutUserUseCase)
