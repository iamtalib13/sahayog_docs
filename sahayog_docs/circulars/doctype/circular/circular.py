import re
import os
import frappe
# from __future__ import unicode_literals
from frappe.model.document import Document
from werkzeug.wrappers import request, Response
# from frappe.utils.response import as_html
# from datetime import datetime

import json

class Circular(Document):
    pass

@frappe.whitelist(allow_guest=True)
def get_list(doc_type=None):
    filters = {}
    if doc_type:
        filters['type'] = doc_type
        

    circulars = frappe.db.get_all("Circular", 
                                  filters=filters,
                                  fields=["name", "circular_name", "year", "date", "circular_id", "circular_doc", "type"],
                                  order_by="name desc")
    
    
    html_content = frappe.render_template("templates/includes/cards.html", {"circulars": circulars})

    return Response(html_content)



@frappe.whitelist(allow_guest=True)
def get_time_list(year=None):
    filters = {}
        
    if year:
        filters['year'] = year
        
    
        
    circulars = frappe.get_all("Circular", 
                                  filters=filters,
                                  fields=["name", "circular_name", "year", "date", "circular_id", "circular_doc", "type"],
                                  order_by="name desc")
    
    if not circulars:
        # Return a message if no data is found
        html_content = "<p>No data found for the selected year.</p>"
    else:
        # Render HTML content using the data fetched
        html_content = frappe.render_template("templates/includes/cards.html", {"circulars": circulars})
    return Response(html_content)

# @frappe.whitelist(allow_guest=True)
# def get_time_list(year=None, month=None):
#     filters = {}

#     if not year and not month:
#         # Case 1: Both year and month are None
#         circulars = frappe.get_all("Circular",
#                                    fields=["name", "circular_name", "year", "month", "date", "circular_id", "circular_doc", "type"],
#                                    order_by="name desc")
#     elif year and not month:
#         # Case 2: Year is present, but month is None
#         filters['year'] = year
#         circulars = frappe.get_all("Circular",
#                                    filters=filters,
#                                    fields=["name", "circular_name", "year", "month", "date", "circular_id", "circular_doc", "type"],
#                                    order_by="name desc")
#     elif not year and month:
#         # Case 3: Year is None, but month is present
#         # Handle this case as per your application logic
#         # Example: Fetch circulars for the given month across all years
#         # Here we assume you have the logic to handle month filtering
#         circulars = frappe.get_all("Circular",
#                                    fields=["name", "circular_name", "year", "month", "date", "circular_id", "circular_doc", "type"],
#                                    order_by="name desc")
#     elif year and month:
#         # Case 4: Both year and month are present
#         filters['year'] = year
#         filters['month'] = month
#         circulars = frappe.get_all("Circular",
#                                    filters=filters,
#                                    fields=["name", "circular_name", "year", "month", "date", "circular_id", "circular_doc", "type"],
#                                    order_by="name desc")
#     else:
#         # Handle any unexpected case here
#         circulars = []

#     if not circulars:
#         # Return a message if no data is found
#         html_content = "<p>No data found for the selected filters.</p>"
#     else:
#         # Render HTML content using the data fetched
#         html_content = frappe.render_template("templates/includes/cards.html", {"circulars": circulars})
    
#     return html_content




@frappe.whitelist(allow_guest=True)
def capture():
    # Get the uploaded file
    uploaded_file = frappe.request.files.get('file')
    if not uploaded_file:
        return {"message": "Error: No file uploaded."}
    
    file_content = uploaded_file.read()
    file_name_old = uploaded_file.filename
    
    # Extract year from the file name using regex
    match = re.search(r'\((\d{4}-\d{2})\)', file_name_old)
    if match:
        year = match.group(1)
    else:
        return {"message": "Error: Invalid file name format. Expected '(year) description.pdf'."}

    # Construct the folder path based on the year
    folder_path = os.path.join("private", "files", "circulars", year)
    full_folder_path = frappe.utils.get_site_path(folder_path)
    os.makedirs(full_folder_path, exist_ok=True)

    # Construct the file path
    file_path = os.path.join(full_folder_path, file_name_old)

    # Write the file content to the specified path
    with open(file_path, "wb") as file:
        file.write(file_content)

    # Construct the file URL without the /files prefix
    file_url = f"/{folder_path}/{file_name_old}"

    # Create a new File document in Frappe
    docname = frappe.get_request_header("Referer").split("/")[-1]
    file_doc = frappe.new_doc("File")
    file_doc.file_name = file_name_old
    file_doc.file_url = file_url
    file_doc.attached_to_name = docname
    file_doc.folder = "Home"
    file_doc.attached_to_doctype = "Circular"
    file_doc.attached_to_field = 'upload_doc'
    file_doc.insert()

    # Return response with file name, file path, and success message
    return {
        "message": "File uploaded successfully.",
        "file_url": file_url,
        "file_name": file_name_old,
        "file_path": file_path
    }



@frappe.whitelist(allow_guest=True)
def check():
    return "Pong"


