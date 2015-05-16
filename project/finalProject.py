from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Restaurant, MenuItem


app = Flask(__name__)

### SQLITE DB CONNECTION ###
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

### Helper Functions ###
def getRestaurantObj(restaurant_id):
    return session.query(Restaurant).filter_by(id=restaurant_id).one()

def getMenuItemObj(restaurant_id, menu_id):
    return session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).one()


### API ENDPOINTS ###
@app.route('/restaurants/JSON')
def showRestaurantsJSON():
    restaurants = session.query(Restaurant).all()
    #serializing manualy 
    lstRestaurants = []
    for restaurant in restaurants:
        jsonItem = {
            'id': restaurant.id,
            'name': restaurant.name,
        }
        lstRestaurants.append(jsonItem)
    return jsonify(Restaurants=lstRestaurants)


### APP URLS ###
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def showMenuJSON(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    #using list generator and the serialize function from database_setup
    return jsonify(RestaurantMenu=[i.serialize for i in items])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def showMenuItem(restaurant_id, menu_id):
    item = getMenuItemObj(restaurant_id, menu_id)
    #using the serialize function from database_setup
    lstItem = [item.serialize,]
    return jsonify(MenuItem=lstItem)


@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    if request.method == 'GET':
        restaurants = session.query(Restaurant).all()
        return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurant/<int:restaurant_id>/menu/')
@app.route('/restaurant/<int:restaurant_id>/')
def showMenu(restaurant_id):
    if request.method == 'GET':
        restaurant = getRestaurantObj(restaurant_id)
        items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
        return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'GET':
        return render_template('newrestaurant.html')
    elif request.method == 'POST':
        newRestaurant = Restaurant()
        newRestaurant.name = request.form['name']
        session.add(newRestaurant)
        session.commit()
        flash('New Restaurant Created.')
        return redirect(url_for('showRestaurants'))


@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'GET':
        restaurant = getRestaurantObj(restaurant_id)
        return render_template('newmenuitem.html', restaurant=restaurant)
    elif request.method == 'POST':
        try:
            restaurant = getRestaurantObj(restaurant_id)
            newItem = MenuItem()
            newItem.name = request.form['name']
            newItem.course = request.form['course']
            newItem.description = request.form['description']
            newItem.price = request.form['price']
            newItem.restaurant_id = restaurant.id
            session.add(newItem)
            session.commit()
            flash('New Menu Item Created.')
            return redirect(url_for('showMenu', restaurant_id=restaurant_id))
        except Exception, e:
                print 'ERROR - ' + str(e)
            


@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    if request.method == 'GET':
        restaurant = getRestaurantObj(restaurant_id)
        return render_template('editrestaurant.html', restaurant=restaurant)
    elif request.method == 'POST':
        try:
            restaurant = getRestaurantObj(restaurant_id)
            restaurant.name = request.form['name']
            session.add(restaurant)
            session.commit()
            flash('Restaurant Successfully Edited.')
            return redirect(url_for('showMenu', restaurant_id=restaurant_id))
        except Exception, e:
            print 'ERROR - ' + str(e)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method == 'GET':
        restaurant = getRestaurantObj(restaurant_id)
        item = getMenuItemObj(restaurant_id, menu_id)
        return render_template('editmenuitem.html', restaurant=restaurant, item=item)
    elif request.method == 'POST':
        try:
            item = getMenuItemObj(restaurant_id, menu_id)
            item.name = request.form['name']
            item.course = request.form['course']
            item.description = request.form['description']
            item.price = request.form['price']
            session.add(item)
            session.commit()
            flash('Menu Item Successfully Edited.')
            return redirect(url_for('showMenu', restaurant_id=restaurant_id))
        except Exception, e:
            print 'ERROR - ' + str(e)


@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
    if request.method == 'GET':
        restaurant = getRestaurantObj(restaurant_id)
        return render_template('deleterestaurant.html', restaurant=restaurant)
    elif request.method == 'POST':
        try:
            restaurant = getRestaurantObj(restaurant_id)
            session.delete(restaurant)
            session.commit()
            flash('Restaurant Successfully Deleted.')
            return redirect(url_for('showRestaurants'))
        except Exception, e:
            print 'ERROR - ' + str(e)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    if request.method == 'GET':
        restaurant = getRestaurantObj(restaurant_id)
        item = getMenuItemObj(restaurant_id, menu_id)
        return render_template('deletemenuitem.html', restaurant=restaurant, item=item)
    elif request.method == 'POST':
        try:
            item = getMenuItemObj(restaurant_id, menu_id)
            session.delete(item)
            session.commit()
            flash('Menu Item Successfully Deleted.')
            return redirect(url_for('showMenu', restaurant_id=restaurant_id))
        except Exception, e:
            print 'ERROR - ' + str(e)




if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)