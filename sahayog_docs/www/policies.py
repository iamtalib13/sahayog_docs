import frappe

@frappe.whitelist(allow_guest=True)
def pong():
    return "Pong"