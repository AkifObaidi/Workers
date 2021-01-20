from flask import *
import sqlite3 as sq
app =Flask(__name__,template_folder="./template")
DATABASE=("./db/db.db")

@app.route("/", methods=['GET','POST'])
def index():
    with sq.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM worker")
        result = cur.fetchall()
        data = []
        for item in result:
	        name,work,country = item        	
	        data.append([name,work,country])
        #return '<script>alert("'+str(forv+1)+'")</script>'

        return render_template("index.html", data=data)
@app.route("/new", methods=['GET','POST'])
def new():
    if request.method=="POST":
        name = request.form.get("name")
        work = request.form.get("work")
        country = request.form.get("country")
        with sq.connect(DATABASE) as con:
            con.execute('INSERT INTO worker (name,work,country) VALUES (?,?,?)', (name,work,country))
            con.commit()
            return '<script>alert("sucisfuly insert");window.location.href="/"</script>'
    return render_template("new.html")
@app.route("/edit", methods=['GET','POST'])
def edit():
    if request.method =='POST':
        name=request.form.get('name')
        if not name:
            return '<script>alert("select a row.");window.location.href="/"</script>'

        return render_template("edit.html", name=name)
    return '<script>window.location.href="/"</script>'
@app.route("/save-edit", methods=['GET','POST'])
def save_edit():
    if request.method=="POST":
        name=request.form.get('name')
        work = request.form.get("work")
        country=request.form.get("country")
       # print(str(country))
    
        with sq.connect(DATABASE) as con:
            cur=con.cursor()
            cur.execute("UPDATE worker SET country ='"+country+"' WHERE name =='"+name+"' ")
            con.commit()
        with sq.connect(DATABASE) as conn:
            cur2=conn.cursor()
            cur2.execute("UPDATE worker SET work ='"+work+"' WHERE name =='"+name+"' ")
            conn.commit()

            return '<script>alert("sucsisfuly update"); window.location.href="/"</script>'
    return '<script>window.location.href="/"</script>'
@app.route("/del", methods=["GET","POST"])
def delate():
    if request.method=="POST":
        name=request.form.get("name")
        with sq.connect(DATABASE) as con:
            cur=con.cursor()
            cur.execute("delete from worker WHERE name='"+name+"'")
            con.commit()
    return '<script>window.location.href="/";</script>'
@app.route("/mkdb")
def mkdb():
    with sq.connect(DATABASE) as con:
        con.execute('CREATE TABLE worker (name TEXT,work TEXT,country TEXT)')
        con.commit()
        return "OJK"
if __name__=='__main__':
    app.run()
    
