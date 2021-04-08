from flask import Flask, flash, render_template, request, redirect, url_for

from flaskext.mysql import MySQL


app = Flask(__name__)
app.secret_key = 'random string'
#app.config["DEBUG"] = True

mysql=MySQL()

#configure db
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='Shiva@94720'
app.config['MYSQL_DATABASE_DB']='ims'
app.config['MYSQL_DATABASE_HOST']='localhost'

# initilize app to mysql
mysql.init_app(app)

conn = mysql.connect()

@app.route('/')
def login():
    return render_template("login_form.html")

@app.route('/login',methods=['POST','GET'])
def admin():
    if request.method=='POST':
        d=request.form
        i=d['uname']
        j=d['psw']
        if i=='admin' and j=='admin':
           return redirect(url_for('home'))
        else:
            flash('incorrect username or password')
            return redirect(url_for('login'))

@app.route('/home')
def home():
    cursor=conn.cursor()
    cursor.execute("select * from stock")
    disp = cursor.fetchall()
    return render_template("home.html",display = disp)

@app.route('/customer')
def customer():
    return render_template("customer.html")

@app.route('/stock')
def stock():
    return render_template("stock.html")

@app.route('/supplier')
def supplier():
    return render_template("supplier.html")

@app.route('/order')
def order():
    return render_template("order.html")


#stock_view
@app.route('/stock_view')
def sview():
    cursor = conn.cursor()
    cursor.execute("select * from stock_avail")
    disp = cursor.fetchall()
    return render_template("stock_view.html",display = disp)
#end stock_view

#order_view

@app.route('/order_view')
def oview():
    cursor = conn.cursor()
    cursor.execute("select * from `order`")
    disp = cursor.fetchall()
    return render_template("order_view.html",display = disp)

#end order_view

#supplier_view

@app.route('/supplier_view')
def suview():
    cursor = conn.cursor()
    cursor.execute("select * from supplier_details")
    disp = cursor.fetchall()
    return render_template("supplier_view.html",display = disp)

#end supplier_view

#customer_view

@app.route('/customer_view')
def cview():
    cursor = conn.cursor()
    cursor.execute("select * from customer_details")
    disp = cursor.fetchall()
    return render_template("customer_view.html",display = disp)

#end customer_view

#stock_insert

@app.route('/sto')
def index_s():
    return render_template('stock_insert.html')

@app.route('/stock_insert',methods=['POST','GET'])
def insert_s():
    if request.method=='POST':
        userdetails = request.form

        Id = userdetails['Pro_id']
        cp = userdetails['Cp']
        np = userdetails['Np']
        sp = userdetails['Sp']
        q = userdetails['Q']
        sid = userdetails['Sup_id']

        cursor = conn.cursor()

        query1="select product_id from stock_avail where product_id = %s"
        query2="select id from supplier_details where id=%s"

        cursor.execute(query1,(Id))

        data1=cursor.fetchone()

        cursor.execute(query2,(sid))

        data2=cursor.fetchone()

        if data1==None:
            if data2!=None:
                cursor.execute("insert into stock_avail(product_id,name_of_the_product,Quantity,Cost_price,Selling_price,Supplier_id) values(%s,%s,%s,%s,%s,%s)",(Id,np,q,cp,sp,sid))
                conn.commit()
                cursor.close()
                flash('stock inserted')

                return redirect(url_for('index_s'))
            else:
                flash('supplier does not exist')

                return redirect(url_for('index_s'))
        else:
            flash('item already exist')

            return render_template('stock_insert.html')

#end stock_insert 

#customer_insert

@app.route('/cus')
def index_c():
    return render_template('customer_insert.html')

@app.route('/customer_insert',methods=['POST','GET'])
def insert_c():
    if request.method=='POST':
        userdetails = request.form

        Id = userdetails['Id']
        name = userdetails['Nm']
        add = userdetails['Add']
        con = userdetails['Con']

        cursor = conn.cursor()

        query="select id from customer_details where id = %s"

        cursor.execute(query,(Id))

        data=cursor.fetchone()

        if data==None:
            cursor.execute("insert into customer_details(id,name,address,contact) values(%s,%s,%s,%s)",(Id,name,add,con))
            conn.commit()
            cursor.close()
            flash('customer inserted')

            return redirect(url_for('index_c'))
        else:
            flash('customer already exist')

            return render_template('customer_insert.html')

#end customer_insert

#order_insert

@app.route('/or')
def index_o():
    return render_template('order_insert.html')

@app.route('/order_insert',methods=['POST','GET'])
def insert_o():
    if request.method=='POST':
        userdetails = request.form

        oid = userdetails['or_id'] #order_id
        cid = userdetails['cus_id'] #customer_id
        pid = userdetails['pro_id'] #product_id
        pr = userdetails['pr'] #price
        Q = userdetails['Q'] #Quantity
        t_a = userdetails['t_a'] #total_amount
        pt = userdetails['pt'] #payment
        md = userdetails['md'] #mode

        cursor = conn.cursor()

        query1="select id from customer_details where id=%s"

        query2="select id from `order` where id = %s"

        query3="select product_id from stock_avail where product_id=%s"

        query4="select quantity from stock_avail where product_id=%s"

        cursor.execute(query1,(cid))

        data1=cursor.fetchone()

        cursor.execute(query2,(oid))

        data2=cursor.fetchone()

        cursor.execute(query3,(pid))

        data3=cursor.fetchone()

        cursor.execute(query4,(pid))

        data4=cursor.fetchone()

        print(data1,data2,data3)

        n=int(Q)

        if data2==None:
            if data1!=None:
                if data3!=None:
                    if data4[0]>n:
                        cursor.execute("insert into `order`(id,customer_id,product_id,price,quantity,total_amount,payment,mode) values(%s,%s,%s,%s,%s,%s,%s,%s)",(oid,cid,pid,pr,Q,t_a,pt,md))
                        cursor.execute("update stock_avail set quantity=quantity-%s where product_id=%s",(Q,pid))
                        conn.commit()
                        cursor.close()
                        flash('order placed')

                        return redirect(url_for('index_o'))
                    else:
                        flash('not enough stock')

                        return redirect(url_for('index_o'))
                else:
                    flash('product does not exist')

                    return redirect(url_for('index_o'))
            else:
                flash('customer does not exist')

                return redirect(url_for('index_o'))
        else:
            flash('order already exist')

            return render_template('order_insert.html')


#end order_insert

#supplier_insert

@app.route('/sup')
def index_su():
    return render_template('supplier_insert.html')

@app.route('/supplier_insert',methods=['POST','GET'])
def insert_su():
    if request.method=='POST':
        userdetails = request.form

        Id = userdetails['Id']
        nm = userdetails['Nm']
        add = userdetails['Add']
        con = userdetails['Con']

        cursor = conn.cursor()

        query="select id from supplier_details where id = %s"

        cursor.execute(query,(Id))

        data=cursor.fetchone()

        if data==None:
            cursor.execute("insert into supplier_details(id,supplier_name,supplier_address,supplier_contact1) values(%s,%s,%s,%s)",(Id,nm,add,con))
            conn.commit()
            cursor.close()
            flash('supplier inserted')

            return redirect(url_for('index_su'))
        else:
            flash('supplier already exist')

            return render_template('supplier_insert.html')


#end supplier_insert

#transaction

@app.route('/bill')
def index_t():
    return render_template('transaction.html')

@app.route('/gen-bill',methods=['post','get'])
def genbill():
     if request.method=='POST':
        userdetails = request.form

        Id = userdetails['Cus_id']

        cursor = conn.cursor()

        query="select customer_id from `order` where customer_id = %s"

        cursor.execute(query,(Id))

        data=cursor.fetchone()

        if data!=None:
            cursor.callproc("genbill",(Id))
            disp=cursor.fetchall()

            return render_template('bill.html',display=disp)
        else:
            flash('No order has been placed with this is')

            return redirect(url_for('index_t'))
#end transaction

# update stock

@app.route('/up')
def index_u():
    return render_template('update.html')
@app.route('/update',methods=['post','get'])
def update():
    if request.method=='POST':
        userdetails = request.form

        pro_id = userdetails['Pro_id']
        Q = userdetails['Q']

        cursor = conn.cursor()

        query="select product_id from stock_avail where product_id = %s"

        cursor.execute(query,(pro_id))

        data=cursor.fetchone()

        if data!=None:
            q="update stock_avail set quantity=%s where product_id=%s"
            cursor.execute(q,(Q,pro_id))
            conn.commit()
            cursor.close()
            flash('stock updated')

            return redirect(url_for('index_u'))
        else:
            flash('product does not exist')

            return render_template('update.html')

if __name__== '__main__':
    app.run(debug=True)
