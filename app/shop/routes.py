from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app.models import User, db, Shop, finsta_shop
from ..apiauthhelper import token_required


shop = Blueprint('shop', __name__, template_folder='shop_templates')


################# API ROUTES #####################

@shop.route('/api/items')
def getAllItemsAPI():
    # args = request.args
    # pin = args.get('pin')
    # print(pin, type(pin))
    # if pin == '1234':

        items = Shop.query.order_by(Shop.date_created.desc()).all()

        my_items = [i.to_dict() for i in items]
        return {'status': 'ok', 'total_results': len(items), "posts": my_items}
    # else:
    #     return {
    #         'status': 'not ok',
    #         'code': 'Invalid Pin',
    #         'message': 'The pin number was incorrect, please try again.'
    #     }

@shop.route('/api/items/<int:item_id>')
def getSingleItemAPI(item_id):
    item = Shop.query.get(item_id)
    if item:
        return {
            'status': 'ok',
            'total_results': 1,
            "item": item.to_dict()
            }
    else:
        return {
            'status': 'not ok',
            'message': f"A post with the id : {item_id} does not exist."
        }


@shop.route('/api/items/create', methods=["POST"])
@token_required
def createItemAPI(user):
    data = request.json 

    title = data['title']
    price = data['price']
    description = data['description']
    img_url = data['imgUrl']

    item = Shop(title, price, description, img_url, user.id)
    item.save()

    return {
        'status': 'ok',
        'message': "Item was successfully created."
    }

@shop.route('/api/items/update', methods=["POST"])
@token_required
def updateItemAPI(user):
    data = request.json 

    item_id = data['itemID']

    item = Shop.query.get(item_id)
    if item.user_id != user.id:
        return {
            'status': 'not ok',
            'message': "You cannot update another user's item!"
        }

    title = data['title']
    price = data['price']
    description = data['description']
    img_url = data['imgUrl']
    item.updateItemInfo(title, price, description, img_url, user.id)
    item.saveUpdates()

    return {
        'status': 'ok',
        'message': "Post was successfully updated."
    }
