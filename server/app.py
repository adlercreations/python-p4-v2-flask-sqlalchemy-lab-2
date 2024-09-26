from flask import Flask
from flask_migrate import Migrate

from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def index():
    return '<h1>Flask SQLAlchemy Lab 2</h1>'

@app.get('/items')
def get_items():
    from models import Item
    items = Item.query.all()
    return {'items': [item.to_dict() for item in items]}

@app.post('/items')
def post_items():
    data = request.get_json()
    item = item(name=data['name'], price=data['price'])
    db.session.add(item)
    db.session.commit()
    return item.to_dict(), 201

@app.get('/items/<int:id>')
def get_item_by_id(id):
    item = Item.query.filter(Item.id == id).first()

    if item is None:
        return {'error': 'Item not found'}, 404

    return item.to_dict(), 200


@app.patch('/items/<int:id>')
def patch_item_by_id(id):
    item = Item.query.filter(Item.id == id).first()

    if item is None:
        return {'error': 'Item not found'}, 404

    data = request.get_json()
    
    for attr in data:
        if attr not in ['id']:
            setattr(item, attr, data[attr])

    # if 'name' in data:
    #     item.name = data['name']

    # if 'price' in data:
    #     item.price = data['price']

    db.session.add(item)
    db.session.commit()

    return item.to_dict(), 200

@app.delete('/items/<int:id>')
def delete_item_by_id(id):
    item = Item.query.filter(Item.id == id).first()

    if item is None:
        return {'error': 'Item not found'}, 404
    

    db.session.delete(item)
    db.session.commit()

    return {'message': 'Item deleted sucessfully'}, 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
