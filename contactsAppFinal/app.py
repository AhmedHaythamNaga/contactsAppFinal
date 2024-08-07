
from flask import Flask, Flask, render_template, request, redirect, url_for, session, jsonify

from utils.establishDBConnection import get_db_connection

app = Flask(__name__, template_folder='templates')

#The login page (Ahmed Naga)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')  #not used currently
        password = request.form.get('password') #same as email
        conn=get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        data=cur.fetchall()
        cur.close()
        return jsonify(data=data)
    else:
        return render_template("login.html",custom_css="login.css")
    

#Routes of render Templetes 
@app.route("/contactList")
def contactList():
   return render_template("contacts.html",custom_css="contacts.css")

@app.route("/View")
def View():
   return render_template("view.html",custom_css="view.css")

@app.route('/addContact')
 def addContact():
    return render_template("add_contact.html",custom_css="add_contact.css")

@app.route("/edit_contact")
def edit_contact():
   return render_template("edit_contact.html",custom_css="edit_contact.css")

@app.route("/Update_Contact")
def Update_Contact():
   return render_template("Update_Contact.html",custom_css="Update_Contact.css")


 #The contact Details page (Mohamed Ali)
 

@app.route("/contacts", methods=['GET'])
def contact_list(): 
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM contacts')
    contacts = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(contacts)




@app.route("/contact/<int:contact_id>", methods=['GET'])
def view_contact(contact_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (contact_id,))
    contact = cur.fetchone()
    cur.close()
    conn.close()
    if contact:
        return jsonify(contact)
    else:
        return jsonify({"error": "Contact not found"}), 404


        

@app.route("/contact/<int:contact_id>/edit", methods=['POST'])
def edit_contact(contact_id):
    conn = get_db_connection()
    cur = conn.cursor()
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')

    if not name or not email or not phone:
        return jsonify({"error": "Name, email, and phone are required fields"}), 400

    cur.execute('UPDATE contacts SET name = %s, email = %s, phone = %s WHERE id = %s',
                (name, email, phone, contact_id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"success": "Contact updated successfully"})



@app.route("/contact/<int:contact_id>/delete", methods=['POST'])
def delete_contact(contact_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM contacts WHERE id = %s', (contact_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"success": "Contact deleted successfully"})

# Added the add contact function
@app.route('/add_contact', methods=['POST'])
def add_contact():
    data = request.get_json()
    id = data.get('Uid')
    name = data.get('full-name')
    email = data.get('email')
    phone = data.get('phone-number')

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # Check if the contact already exists
        cur.execute('SELECT * FROM contacts WHERE email = %s OR phone_number = %s', (email, phone))
        check = cur.fetchall()

        if check:
            return jsonify({"error": "Contact already exists"}), 400

        # Insert the new contact
        cur.execute('INSERT INTO contacts (user_id, full_name, email, phone_number) VALUES (%s, %s, %s, %s)',
                    (id, name, email, phone))
        conn.commit()
        return jsonify({"success": "Contact added successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        conn.close()

    finally:
        cur.close()
        conn.close()

 

if __name__ == "__main__":
    app.run(debug=True)
