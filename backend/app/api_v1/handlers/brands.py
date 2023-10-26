from app.models.adidas_model import Brands
from app.utils.product_utils import ApiServices
from beanie import PydanticObjectId
from fastapi import APIRouter

brands_router = APIRouter()


# ------------------------------- GET REQUESTS ------------------------------- #


@brands_router.get(
    "/",
    summary="Get all of the Brands product information",
    description="Retrieve all Brand products from MongoDB using a Beanie Document model",
    response_model=list[Brands],
)
async def read_brands():
    return await ApiServices.list_products(collection=Brands)


@brands_router.get(
    "/object/{object_id}", summary="Get a product by ObjectId", response_model=Brands
)
async def read_id(object_id: PydanticObjectId):
    return await ApiServices.retrieve_object(collection=Brands, product_id=object_id)


@brands_router.get(
    "/query/",
    summary="Search via 6 different parameters",
    description="The user can query the database using any of the stated values",
    response_model=list[Brands],
)
async def query_by_parameter(
    product: str | None = None,
    price: int | None = None,
    category: str | None = None,
    link: str | None = None,
    image: str | None = None,
    division: str | None = None,
):
    return await ApiServices.parameter_query(
        collection=Brands,
        product=product,
        price=price,
        category=category,
        link=link,
        image=image,
        division=division,
    )


@brands_router.get(
    "/query/ai/{product}", summary="Return AI response of specific product info"
)
async def get_ai_response(product: str, question: str | None = None):
    return await ApiServices.ai_query(
        collection="brands", product=product, question=question
    )


# ------------------------------- POST REQUESTS ------------------------------- #


# CREATE AN ENDPOINT THAT RETURNS A PRODUCT DIRECTLY FROM THE API THAT A CUSTOMER WANTS
@brands_router.post(
    "/{product}",
    summary="Return the project that a customer specifically asks to look at",
)
async def get_product(product: str):
    return await ApiServices.product_from_api(product=product)


# return product and can return similar products with the same model Id
# display some graphs or insights about the product when returned
# return a photo of the product
# return what customers have said about it with this information
