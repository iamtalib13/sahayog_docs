# Copyright (c) 2024, Talib Sheikh and contributors
# For license information, please see license.txt
import re
import os
import frappe
from frappe.model.document import Document

class Circular(Document):
    pass

@frappe.whitelist()
def capture(file=None):
    file_content = frappe.local.uploaded_file
    file_name_old = frappe.local.uploaded_filename

    # Extract details from the file name (assume format "year_circular_id_circular_name.pdf")
    match = re.match(r"(\d{4})_(\d+)_([^\.]+)\.pdf", file_name_old)
    if not match:
        return {"message": "Error: Invalid file name format. Expected 'year_circular_id_circular_name.pdf'."}

    year, circular_id, circular_name = match.groups()

    # Construct the folder path based on the year
    folder_path = f"private/year/{year}"
    os.makedirs(os.path.join(frappe.get_site_path(), folder_path), exist_ok=True)

    # Construct the file path
    file_path = os.path.join(folder_path, file_name_old)

    # Write the file content to the specified path
    with open(os.path.join(frappe.get_site_path(), file_path), "wb") as file:
        file.write(file_content)

    # Construct the file URL
    sys_file_path = f"/{file_path}"

    # Create a new File document in Frappe
    file_doc = frappe.new_doc("File")
    file_doc.file_name = file_name_old
    file_doc.file_url = sys_file_path
    file_doc.attached_to_name = frappe.get_request_header("Referer").split("/")[-1]
    file_doc.folder = "Home"
    file_doc.attached_to_doctype = "Circular"
    file_doc.attached_to_field = 'upload_image'
    file_doc.insert()

    # Return response
    return {"message": "File uploaded successfully.", "file_url": sys_file_path}
