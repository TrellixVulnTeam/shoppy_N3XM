from flask import Flask, render_template, redirect , request
from flask_sqlalchemy import SQLAlchemy
from cloudipsp import Api, Checkout

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    desc = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return self.title


@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template('index.html' , data=items)

@app.route('/delete/<int:id>')
def delete(id):
    item = Item.query.get_or_404(id)
    try:
        db.session.delete(item)
        db.session.commit()
        return redirect('/')
    except:
        return "ERROR"


@app.route('/cart/<int:id>')
def addcart(id):
    item = Item.query.order_by(Item.id)
    return render_template('cart.html' ,data=item)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/buy/<int:id>')
def item_buy(id):
    item = Item.query.get(id)

    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "USD" ,
        "amount": item.price + 00
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']
        desc = request.form['desc']

        item = Item(title=title, price=price, desc=desc)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "ERROR"
    else:
        return render_template('create.html')





if __name__ == "__main__":
    app.run(debug=True)


