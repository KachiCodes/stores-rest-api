from flask_restful import Resource
from models.Store import StoreModel

class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store Not Found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "Store with Similar name '{}' already exists".format(name)}, 400
         store = StoreModel(name)
         try:
             store.save_to_db()
         except:
             return {'message': 'An error occured while creating the store'}, 500

         store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name):
            if store:
                store.delete_from_db()
            return{'message':'Store Deleted'}

class StoreList(Resource):
    return {'stores':[x.json() for x in StoreModel.query.all()]}
