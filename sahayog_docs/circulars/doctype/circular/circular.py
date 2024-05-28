import os
import frappe
from frappe.model.document import Document

class Circular(Document):
    pass

@frappe.whitelist()
def capture():
    # Get the uploaded file
    file_content = frappe.local.uploaded_file
    file_name_old = frappe.local.uploaded_filename

    # Extract year from the file name (assume format "year_circular_id_circular_name.pdf")
    try:
        year = file_name_old.split('_')[0]
    except IndexError:
        return {"message": "Error: Invalid file name format. Expected 'year_circular_id_circular_name.pdf'."}

    # Construct the folder path based on the year
    folder_path = os.path.join("private", "year", year)
    full_folder_path = frappe.get_site_path(folder_path)
    os.makedirs(full_folder_path, exist_ok=True)

    # Construct the file path
    file_path = os.path.join(full_folder_path, file_name_old)

    # Write the file content to the specified path
    with open(file_path, "wb") as file:
        file.write(file_content)

    # Construct the file URL
    site_name = frappe.utils.get_url()
    sys_file_path = f"{site_name}/{folder_path}/{file_name_old}"

    # Create a new File document in Frappe
    docname = frappe.get_request_header("Referer").split("/")[-1]
    file_doc = frappe.new_doc("File")
    file_doc.file_name = file_name_old
    file_doc.file_url = sys_file_path
    file_doc.attached_to_name = docname
    file_doc.folder = "Home"
    file_doc.attached_to_doctype = "Circular"
    file_doc.attached_to_field = 'upload_doc'
    file_doc.insert()

    # Return response
    return {"message": "File uploaded successfully.", "file_url": sys_file_path}
