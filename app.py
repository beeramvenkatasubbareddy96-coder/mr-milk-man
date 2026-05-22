from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)

app.secret_key = "milkman_secret"

# PRODUCTS
products = [
    ("buffalomilk.jpg", "Buffalo Milk", 90),
    ("cowmilk.jpg", "Cow Milk", 90),
    ("desicowmilk.jpg", "Desi Cow Milk", 110),
    ("tonedmilk.jpg", "Toned Milk", 80),
    ("doubletonedmilk.jpg", "Double Toned Milk", 70),
    ("buffaloghee.jpg", "Buffalo Ghee", 1000),
    ("paneer.jpg", "Paneer", 440),
    ("kova.jpg", "Sweetless Kova", 440)
]

# HOME PAGE
@app.route("/")
def home():

    return render_template(
        "index.html",
        products=products
    )


# ADD TO CART
@app.route("/add/<name>/<int:price>")
def add_to_cart(name, price):

    if "cart" not in session:
        session["cart"] = []

    session["cart"].append({
        "name": name,
        "price": price
    })

    session.modified = True

    return redirect(url_for("home"))


# CART PAGE
@app.route("/cart")
def cart():

    cart = session.get("cart", [])

    total = sum(item["price"] for item in cart)

    return render_template(
        "cart.html",
        cart=cart,
        total=total
    )


# REMOVE ITEM
@app.route("/remove/<int:index>")
def remove(index):

    cart = session.get("cart", [])

    if 0 <= index < len(cart):
        cart.pop(index)

    session["cart"] = cart

    session.modified = True

    return redirect(url_for("cart"))


# CHECKOUT PAGE
@app.route("/checkout")
def checkout():

    cart = session.get("cart", [])

    total = sum(item["price"] for item in cart)

    return render_template(
        "checkout.html",
        total=total
    )

# PAYMENT SUCCESS
@app.route("/payment-success")
def payment_success():

    session.pop("cart", None)

    return """
    <h1>Payment Successful ✅</h1>

    <h2>Thank You for Your Order 🥛</h2>

    <a href='/'>
        <button>Back to Home</button>
    </a>
    """
# ORDER FORM
@app.route("/order", methods=["POST"])
def order():

    name = request.form.get("name")

    phone = request.form.get("phone")

    product = request.form.get("product")

    return f"""
    <h1>Order Placed Successfully ✅</h1>

    <p><b>Name:</b> {name}</p>

    <p><b>Phone:</b> {phone}</p>

    <p><b>Product:</b> {product}</p>

    <br>

    <a href="/">
        <button>Go Back</button>
    </a>
    """


if __name__ == "__main__":

    app.run(debug=True)  