from flask import Flask, request, render_template, session, redirect
import psycopg2

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    user = None
    if 'user_id' in session:
        user = {'id': session['user_id'], 'name': session.get('username')}
    return render_template('index.html', user=user)

@app.route('/bin')
def bin_page():

    if 'user_id' not in session:
        cart_items = session.get('cart', [])
    else:
        conn = psycopg2.connect(user="postgres",
                            password="Cookie123",
                            host="localhost",
                            port="5432",
                            dbname="online_shop")
        c = conn.cursor()
        c.execute("""
                SELECT p.product_id, p.name, p.price, p.description, p.image_path 
                FROM cart_items c
                INNER JOIN products p ON p.product_id = c.product_id
                WHERE c.user_id = %s
            """, (session['user_id'],))

        cart_items = [{
                'id': row[0],
                'name': row[1],
                'price': row[2],
                'description': row[3],
                'image': row[4]
            } for row in c.fetchall()]
        c.close()
        conn.close()
    return render_template('bin.html', cart=cart_items)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    conn = psycopg2.connect(user="postgres",
                            password="Cookie123",
                            host="localhost",
                            port="5432",
                            dbname="online_shop")
    c = conn.cursor()
    username = request.form.get("username")
    phone = request.form.get("phone")
    try:
        c.execute('SELECT user_id, name FROM users WHERE phone = %s', (phone,))
        user = c.fetchone()

        if user:
            user_id, db_username = user
            session['user_id'] = user_id
            session['username'] = db_username

        else:
            c.execute('INSERT INTO users(name, phone) VALUES (%s, %s) RETURNING user_id', (username, phone))
            user_id = c.fetchone()[0]
            session['user_id'] = user_id
            session['username'] = username
            conn.commit()
    
    except:
        conn.rollback()
        return "Ошибка регистрации"
    
    finally:
        c.close()
        conn.close()

    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/category/<category_name>')
def show_category(category_name):
    category_db = {
        'outwear': 'верхняя одежда',
        'shoes': 'обувь',
        'accessories': 'аксессуары',
        'dress | overalls': 'платья и комбинезоны',
        'trousers | jeans': 'брюки и джинсы',
        'suits': 'костюмы',
        'skirts': 'юбки',
        'sweatshirts': 'толстовки',
        'home clothes': 'домашняя одежда',
        'bags': 'сумки'
    }
    titles = {
        'outwear': ('TANGERINE-outwear', 'OUTWEAR'),
        'shoes': ('TANGERINE-shoes', 'SHOES'),
        'accessories': ('TANGERINE-accessories', 'ACCESSORIES'),
        'dress | overalls': ('TANGERINE-dress | overalls', 'DRESS | OVERALL'),
        'trousers | jeans': ('TANGERINE-trousers | jeans', 'TROUSERS | JEANS'),
        'suits': ('TANGERINE-suits', 'SUITS'),
        'skirts': ('TANGERINE-skirts', 'SKIRTS'),
        'sweatshirts': ('TANGERINE-sweatshirts', 'SWEATSHIRTS'),
        'home clothes': ('TANGERINE-home clothes', 'HOME CLOTHES'),
        'bags': ('TANGERINE-bags', 'BAGS')
    }
    title, subtitle = titles.get(category_name, ('TANGERINE', 'Категория'))
    russian_category = category_db[category_name]
    conn = psycopg2.connect(user="postgres",
                            password="Cookie123",
                            host="localhost",
                            port="5432",
                            dbname="online_shop")
    c = conn.cursor()
    c.execute('SELECT * FROM products WHERE category = %s', (russian_category,))
    goods = c.fetchall()
    c.close()
    conn.close()
    return render_template('base.html', goods = goods, title=title, subtitle=subtitle)

@app.route('/add_to_bin', methods=['POST'])
def add_to_bin():
    product_id = request.form.get('product_id')
    category = request.form.get('product_category')
    categories = {
        'верхняя одежда': 'outwear',
        'обувь': 'shoes',
        'аксессуары': 'accessories',
        'платья и комбинезоны': 'dress | overalls',
        'брюки и джинсы': 'trousers | jeans',
        'костюмы': 'suits',
        'юбки': 'skirts',
        'толстовки': 'sweatshirts',
        'домашняя одежда': 'home clothes',
        'сумки': 'bags'
    }
    category_name = categories[category]

    if 'cart' in session:
        if any(item['id'] == int(product_id) for item in session['cart']):
            return redirect('/category/<category_name>')
    
    conn = psycopg2.connect(user="postgres",
                          password="Cookie123",
                          host="localhost",
                          port="5432",
                          dbname="online_shop")
    c = conn.cursor()

    try:
        if 'user_id' in session:
            user_id = session['user_id']
            c.execute("SELECT id FROM cart_items WHERE user_id = %s AND product_id = %s", (user_id, product_id))
            if not c.fetchone():
                c.execute("INSERT INTO cart_items (user_id, product_id) VALUES (%s, %s)", (user_id, product_id))
                conn.commit()

        else:
            if 'cart' not in session:
                session['cart'] = []
            if not any(item['id'] == int(product_id) for item in session['cart']):
                c.execute('SELECT * FROM products WHERE product_id = %s', (product_id,))
                product = c.fetchone()
                if product:
                    session['cart'].append({
                        'id': product[0],
                        'name': product[1],
                        'price': product[2],
                        'description': product[4],
                        'image': product[5]
                    })
                    session.modified = True
    except:
        conn.rollback()
        return "Ошибка"
    return redirect(f'/category/{category_name}') 

@app.route('/remove_from_bin/<product_id>', methods=['POST'])
def remove_from_bin(product_id):
    if 'user_id' in session:
        conn = psycopg2.connect(
            user="postgres",
            password="Cookie123",
            host="localhost",
            port="5432",
            dbname="online_shop"
        )
        c = conn.cursor()
        c.execute("DELETE FROM cart_items WHERE user_id = %s AND product_id = %s", (session['user_id'], product_id))
        conn.commit()
        c.close()
        conn.close()
        
    elif 'cart' in session:
        session['cart'] = [item for item in session['cart'] if str(item['id']) != str(product_id)]
        session.modified = True
    return redirect('/bin')


if __name__ == '__main__':
    app.run(debug=True)