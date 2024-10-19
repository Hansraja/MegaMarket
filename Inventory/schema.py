import graphene
from graphene_django import DjangoConnectionField
from graphene_django.types import DjangoObjectType

from Api import relay
from Inventory.models import Item, Category, Order, OrderItem, Inventory, ItemVariation, ItemReview, Tag

class ItemObject(DjangoObjectType):
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
    pass