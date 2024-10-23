import graphene
from graphene_django import DjangoConnectionField
from graphene_django.types import DjangoObjectType

from Admin.models import Brand
from Api import relay
from Common.exceptions import InvalidImageException, InvalidModelIdException, UnAuthorizedException
from Common.models import Image
from Common.tools import ImageHandler
from Inventory.models import Item, Category, Order, OrderItem, Inventory, ItemVariation, ItemReview, Tag
from Inventory.types import ItemExtraFieldObject, NewItemInput
from Vendor.models import Vendor

class ItemObject(DjangoObjectType):
    bullet_points = graphene.List(graphene.String)
    extra_fields = graphene.List(ItemExtraFieldObject)

    class Meta:
        model = Item
        exclude = ('created_at', 'updated_at')
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'description': ['exact', 'icontains', 'istartswith'],
            'category': ['exact'],
            'tags': ['exact'],
            'price': ['exact', 'gt', 'gte', 'lt', 'lte'],
        }
        interface= (relay.Node, )
        use_connection = True


class CategoryObject(DjangoObjectType):
    class Meta:
        model = Category
        exclude = ('created_at', 'updated_at')
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
        }
        interface= (relay.Node, )
        use_connection = True


class OrderObject(DjangoObjectType):
    class Meta:
        model = Order
        fields = '__all__'
        filter_fields = {
            'user': ['exact'],
            'status': ['exact'],
            'created_at': ['exact', 'gt', 'gte', 'lt', 'lte'],
        }
        interface= (relay.Node, )
        use_connection = True

class OrderItemObject(DjangoObjectType):
    class Meta:
        model = OrderItem
        fields = '__all__'
        filter_fields = {
            'order': ['exact'],
            'item': ['exact'],
            'quantity': ['exact', 'gt', 'gte', 'lt', 'lte'],
        }
        interface= (relay.Node, )
        use_connection = True

class InventoryObject(DjangoObjectType):
    class Meta:
        model = Inventory
        fields = '__all__'
        filter_fields = {
            'item': ['exact'],
            'quantity': ['exact', 'gt', 'gte', 'lt', 'lte'],
        }
        interface= (relay.Node, )
        use_connection = True

class ItemVariationObject(DjangoObjectType):
    class Meta:
        model = ItemVariation
        fields = '__all__'
        # interface= (relay.Node, )
        # use_connection = True

class ItemReviewObject(DjangoObjectType):
    
    class Meta:
        model = ItemReview
        fields = '__all__'
        filter_fields = {
            'item': ['exact'],
            'user': ['exact'],
            'rating': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'review': ['exact', 'icontains', 'istartswith'],
        }
        interface= (relay.Node, )
        use_connection = True 

class TagObject(DjangoObjectType):
    class Meta:
        model = Tag
        fields = '__all__'
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
        }
        interface= (relay.Node, )
        use_connection = True

'''********** Mutations **********'''

class CreateItem(graphene.Mutation):
    class Input:
        input = NewItemInput(required=True)

    item = graphene.Field(ItemObject)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, input: NewItemInput):
        if not info.context.user.is_authenticated:
            raise UnAuthorizedException()
        elif not info.context.user.type.lower() == 'vendor':
            raise UnAuthorizedException()
        
        try: vendor = Vendor.objects.get(key=input.vendor)
        except Vendor.DoesNotExist: raise InvalidModelIdException(model="Vendor")
        
        try: category = Category.objects.get(id=input.category)
        except Category.DoesNotExist: raise InvalidModelIdException(model="Category")

        brand = None
        if input.brand:
            try: brand = Brand.objects.get(id=input.brand)
            except Brand.DoesNotExist: raise InvalidModelIdException(model="Brand")

        if not vendor or not category: raise InvalidModelIdException(model="Vendor or Category")

        image = ImageHandler(input.image).auto_image()

        if not image or not isinstance(image, Image): raise InvalidImageException()

        item = Item(
            sku=input.sku,
            name=input.name,
            teaser=input.teaser,
            description=input.description,
            bullet_points=input.bullet_points,
            image=image,
            status=input.status,
            price=input.price,
            delivery_time=input.delivery_time,
            shipping_cost=input.shipping_cost,
            can_return=input.can_return,
            return_time=input.return_time,
            return_policy=input.return_policy,
            category=category,
            vendor=vendor,
            brand=brand,
            extra_fields=input.extra_fields
        )

        for tag in input.tags:
            tag = Tag.objects.get_or_create(name=tag)
            item.tags.add(tag)

        for image in input.images:
            image = ImageHandler(image).auto_image()
            if image and isinstance(image, Image):
                item.images.add(image)

        item.save()
        return CreateItem(item=item, success=True, message="Item created successfully")


'''********** Query **********'''

class Query(graphene.ObjectType):
    items = DjangoConnectionField(ItemObject)
    categories = DjangoConnectionField(CategoryObject)
    orders = DjangoConnectionField(OrderObject)
    order_items = DjangoConnectionField(OrderItemObject)
    inventories = DjangoConnectionField(InventoryObject)
    item_reviews = DjangoConnectionField(ItemReviewObject)
    tags = DjangoConnectionField(TagObject)

    item = relay.Node.Field(ItemObject)
    category = relay.Node.Field(CategoryObject)
    order = relay.Node.Field(OrderObject)
    order_item = relay.Node.Field(OrderItemObject)
    inventory = relay.Node.Field(InventoryObject)
    item_review = relay.Node.Field(ItemReviewObject)
    tag = relay.Node.Field(TagObject)


class Mutation(graphene.ObjectType):
    create_item = CreateItem.Field()