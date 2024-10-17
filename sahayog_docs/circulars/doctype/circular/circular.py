import re
import os
import frappe

# from __future__ import unicode_literals
from frappe.model.document import Document
from werkzeug.wrappers import request, Response

# from frappe.utils.response import as_html
# from datetime import datetime

import json
from frappe.utils import getdate


class Circular(Document):
    pass


@frappe.whitelist(allow_guest=True)
def get_list(doc_type=None):
    filters = {}
    if doc_type:
        filters["type"] = doc_type

    circulars = frappe.db.get_all(
        "Circular",
        filters=filters,
        fields=[
            "name",
            "circular_name",
            "year",
            "date",
            "circular_id",
            "circular_doc",
            "type",
        ],
        order_by="date desc",
    )

    for circular in circulars:
        if circular["date"]:
            circular["date"] = getdate(circular["date"]).strftime("%d-%m-%Y")

    if not circulars:
        html_content = "<p>No data found for the selected filters.</p>"
    else:
        html_content = frappe.render_template(
            "templates/includes/cards.html", {"circulars": circulars}
        )

    return Response(html_content)


@frappe.whitelist(allow_guest=True)
def get_time_list(year=None, month=None):
    filters = {}

    if year:
        filters["year"] = year

    if month:
        filters["month"] = month

    circulars = frappe.get_all(
        "Circular",
        filters=filters,
        fields=[
            "name",
            "circular_name",
            "year",
            "month",
            "date",
            "circular_id",
            "circular_doc",
            "type",
        ],
        order_by="date desc",
    )

    for circular in circulars:
        if circular["date"]:
            circular["date"] = getdate(circular["date"]).strftime("%d-%m-%Y")

    if not circulars:
        html_content = "<p>No data found for the selected filters.</p>"
    else:
        html_content = frappe.render_template(
            "templates/includes/cards.html", {"circulars": circulars}
        )

    return Response(html_content)


# get current user name
@frappe.whitelist()
def get_user_full_name(email):
    # Fetch first name from Employee where user_id is the given email
    user_details = frappe.db.get_value(
        "Employee", {"user_id": email}, ["first_name"], as_dict=True
    )

    if user_details:
        # Return the first name
        return Response(user_details.get('first_name', "Guest User"))
    else:
        return Response("Guest User")



# get current user name
# @frappe.whitelist()
# def get_user_full_name(email):
#     employee = frappe.get_value(
#         "Employee",
#         {"user_id": email},
#         ["first_name", "last_name", "designation"],
#         as_dict=True,
#     )

#     if employee:
#         first_name = employee.get("first_name") or ""
#         last_name = employee.get("last_name") or ""
#         full_name = " ".join(filter(None, [first_name, last_name]))
#         designation = employee.get("designation") or ""

#         return {"full_name": full_name.strip(), "designation": designation}
#     else:
#         return {"full_name": ("Guest User"), "designation": ""}


# search funtion to handle the search functionality
@frappe.whitelist(allow_guest=True)
def search():
    query = frappe.form_dict.get("query", "")

    try:
        # Perform the search on multiple fields
        results = frappe.db.sql(
            """
            SELECT name, circular_name, year, date, circular_doc, type
            FROM `tabCircular`
            WHERE circular_name LIKE %(query)s
            OR type LIKE %(query)s
            """,
            {"query": f"%{query}%"},
            as_dict=True,
        )

        if not results:
            cards_html = "<p>No data found</p>"
            # Return a message when no results are found

        else:

            # Render the HTML using the template
            cards_html = frappe.render_template(
                "templates/includes/cards.html", {"circulars": results}
            )

        return Response(cards_html)

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Search Error")
        return frappe.utils.response.report_error(
            "An error occurred while processing your request.", error_code=500
        )


@frappe.whitelist(allow_guest=True)
def capture():
    # Get the uploaded file
    uploaded_file = frappe.request.files.get("file")
    if not uploaded_file:
        return {"message": "Error: No file uploaded."}

    file_content = uploaded_file.read()
    file_name_old = uploaded_file.filename

    # Extract year from the file name using regex
    match = re.search(r"\((\d{4}-\d{2})\)", file_name_old)
    if match:
        year = match.group(1)
    else:
        return {
            "message": "Error: Invalid file name format. Expected '(year) description.pdf'."
        }

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
    file_doc.attached_to_field = "upload_doc"
    file_doc.insert()

    # Return response with file name, file path, and success message
    return {
        "message": "File uploaded successfully.",
        "file_url": file_url,
        "file_name": file_name_old,
        "file_path": file_path,
    }


@frappe.whitelist(allow_guest=True)
def check():
    return "Pong"


@frappe.whitelist()
def fetch_employee_data(employee_id):
    # Use parameterized query to prevent SQL injection
    sql_query = """SELECT employee_name,designation,branch FROM `tabEmployee` WHERE user_id=%s"""
    # Execute the query with the provided employee_id
    result = frappe.db.sql(sql_query, (employee_id,), as_dict=True)

    return result
