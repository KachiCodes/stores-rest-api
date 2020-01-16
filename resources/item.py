from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required
from models.item import itemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type = float,
        required = True,
        help = "This field cannot be left Blank!"
    )
    parser.add_argument(
        'store_id',
        type = int,
        required = True,
        help = "This holds the store id for every item"
    )
    @jwt_required
    def get(self, name):
        item = itemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not Found'}, 404

    def post(self, name):
        if itemModel.find_by_name(name):
            return {'message': "An item with name {} already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        item = itemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred while inserting the item"}, 500 #internal server error
        return item.json(), 201 #Status codes for creating items


    def delete(self,name):
        item = itemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = itemModel.find_by_name(name)

        if item is None:
            item = itemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()

class ItemList(Resource):
    def get(self):
        return {'items':[x.json() for x in itemModel.query.all()]}
