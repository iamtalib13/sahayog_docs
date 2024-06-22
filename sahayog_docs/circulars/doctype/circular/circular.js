// Copyright (c) 2024, Talib Sheikh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Circular", {
  before_save: function (frm) {
    let date = frm.doc.date;
    // Assuming your date field is named 'date'
    if (date) {
      let dateObj = new Date(date); // Use 'date' directly, not 'frm.doc.date_field'
      let month = dateObj.getMonth() + 1; // getMonth() returns zero-based index (0 for January)
      let monthString = ("0" + month).slice(-2); // Ensure two-digit format ('01' to '12')
      frm.set_value("month", monthString); // Assuming 'month_field' is where you want to store the month
    }
  },

  refresh: function (frm) {
    if (frm.is_new()) {
      // frm.set_df_property("year", "read_only", 1);

      if (!frappe.user.has_role("Circular Manager")) {
        frappe.set_route("/app/sahayog-policies");
        frappe.show_alert(
          {
            message: __("Access Denied"),
            indicator: "red",
          },
          5
        );
      }
    } else if (!frm.is_new()) {
      frm.set_df_property("circular_doc", "read_only", 1);
      frm.set_df_property("year", "read_only", 0);
      frm.set_df_property("circular_name", "read_only", 0);
      frm.set_df_property("circular_id", "read_only", 0);
    }
  },

  circular_doc: function (frm) {
    console.log("hello from upload");
    frm.trigger("capture_doc_details");
    frm.trigger("capture_doc_details");
  },

  upload_doc: function (frm) {
    uploadFile(frm);
  },

  fetch_details: function (frm) {
    frm.trigger("capture_doc_details");
  },
  capture_doc_details: function (frm) {
    if (
      frappe.user.has_role("Circular Manager") ||
      frappe.user.has_role("System Manager")
    ) {
      console.log("admin");

      let file = frm.doc.circular_doc;
      console.log("file-", file);

      if (file) {
        // Corrected regular expression to match the filename pattern exactly
        let regex =
          /Circular No\. (\d+)\s\((\d{4}-\d{2})\)\s(.+)\sDate\s(\d{2}-\d{2}-\d{4})\.pdf/;
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

          frm.set_value("date", date);
          frm.refresh_field("date");

          frm.set_value("circular_id", id);
          frm.refresh_field("circular_id");

          frm.set_value("year", year);
          frm.refresh_field("year");

          frm.set_value("circular_name", fileName);
          frm.refresh_field("circular_name");
        } else {
          console.log("Filename does not match the expected pattern");
        }
      } else {
        console.log("No circular document provided");
      }
    }
  },
});

function uploadFile(frm) {
  new frappe.ui.FileUploader({
    method: "sahayog_docs.circulars.doctype.circular.circular.capture",
    make_attachments_public: false,
    dialog_title: "Upload Circular File",
    disable_file_browser: false,
    allow_link: false,
    frm: frm,
    restrictions: {
      allowed_file_types: [".pdf"],
    },
    on_success(file, response) {
      frappe.msgprint(`Server response: ${response.message}`, "Message"); // Log the response for debugging

      frm.set_df_property(
        "upload_doc",
        "description",
        "<b style='color:darkgreen;'>Path:/year/2024-25</b>"
      );
      frappe.show_alert(
        {
          message: __("File uploaded."),
          indicator: "green",
        },
        5
      );

      frm.refresh();
    },
    on_error(error) {
      console.error(error);
      frappe.msgprint({
        title: __("Error"),
        indicator: "red",
        message: __("There was an error while uploading the file."),
      });
    },
  });
}
