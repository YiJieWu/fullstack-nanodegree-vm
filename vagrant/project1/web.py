from flask import Flask,request,render_template,redirect,url_for,flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

'''
CURD
http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#querying

{%logical code%}-> the code we want to execute within our html
{{printed code}}


The key function today to learn is 
1 render_template(String->template_name,You_Designed_name)

The 1st argument is the template name of string, it will usually be html,
The rest of the arguments you pass to is the arguments you will need when 
write the render template

2 url_for(String->fuction name,parname=value1........)

The parameter name has to exactly the same with the fun parameter name!!!!

'''




app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def restaurantList():
    pass


@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)

    #Template rendering, pass the template name and the variables
    return render_template('menu.html',restaurant=restaurant,all_items=items)


@app.route('/restaurants/<int:restaurant_id>/new/',methods=['GET','POST'])
def newMenuItem(restaurant_id):
    #return "page to create a new menu item. Task 1 complete!"
    if request.method=='POST':
        newItem = MenuItem(name=request.form['name'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash('New menue item created!')
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))

    else:
        #just render the page
        return render_template('newmenueitem.html',rAAA_id=restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/',methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method=='POST':
        new_item_name=request.form['name']
        item=session.query(MenuItem).filter_by(restaurant_id=restaurant_id,id=menu_id).one()
        item.name=new_item_name
        session.add(item)
        session.commit()
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html',r_id=restaurant_id,m_id=menu_id)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/',methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    delete_item=session.query(MenuItem).filter_by(restaurant_id=restaurant_id,id=menu_id).one()
    if request.method=='POST':
        session.delete(delete_item)
        session.commit()
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html',item=delete_item)



if __name__ == '__main__':
    app.secret_key='super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)