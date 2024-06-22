frappe.pages["sahayog-docs"].on_page_load = function (wrapper) {
  var page = frappe.ui.make_app_page({
    parent: wrapper,
    title: "",
    single_column: true,
  });

  $(frappe.render_template("sahayog_docs", {})).appendTo(page.body);
};
