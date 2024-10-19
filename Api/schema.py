import graphene
from User.schema import Query as UserQuery, Mutation as UserMutation
from Common.schema import Query as CommonQuery, Mutation as CommonMutation
from Inventory.schema import Query as InventoryQuery, Mutation as InventoryMutation


class Query(UserQuery, CommonQuery, InventoryQuery):
    greet = graphene.String(name=graphene.String(default_value="stranger"))
    
    def resolve_greet(self, info, name = None):
        return f'Hello {name}!'

class Mutation(UserMutation, CommonMutation, InventoryMutation):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)