// Copyright (c) 2024, Talib Sheikh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Circular", {
  before_save: function (frm) {
    if (
      frappe.user.has_role("Circular Manager") ||
      frappe.user.has_role("System Manager")
    ) {
      console.log("admin");

      let file = frm.doc.circular_doc;
      console.log("file-", file);

      // Define a regular expression to extract the required components
      let regex =
        /Circular No\. (\d+) \((\d{4}-\d{2})\) (.+) Date (\d{2}-\d{2}-\d{4})\.pdf/;
      let match = file.match(regex);

      if (match) {
        let id = `Circular No. ${match[1]}`;
        let year = match[2];
        let fileName = match[3];
        let date = match[4];

        console.log("ID:", id);
        console.log("Year:", year);
        console.log("File Name:", fileName);
        console.log("Date:", date);

        // Set the extracted date to the form field and refresh the field
        frm.set_value("date", date);
        frm.refresh_field("date");

        // Optionally, set other fields as well if needed
        frm.set_value("circular_id", id);
        frm.refresh_field("circular_id");

        frm.set_value("year", year);
        frm.refresh_field("year");

        frm.set_value("circular_name", fileName);
        frm.refresh_field("circular_name");

        // You can now use these variables as needed
      } else {
        console.log("Filename does not match the expected pattern");
      }
    }
  },
  refresh: function (frm) {},

  circular_doc: function (frm) {},
});
