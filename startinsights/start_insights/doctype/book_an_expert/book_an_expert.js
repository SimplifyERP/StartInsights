// Copyright (c) 2024, Suriya and contributors
// For license information, please see license.txt

frappe.ui.form.on("Book an Expert", {
	refresh(frm) {

	},
    create_booking(frm) {
        frm.call("get_total_dates").then((r) => {
            var existingDates = frm.doc.booking.map(row => row.date);
            $.each(r.message.dates, function (i, date) {
                if (existingDates.includes(date)) {
                    // If the date already exists, update the time slots
                    var existingRow = frm.doc.booking.find(row => row.date === date);
                    existingRow.start_time = r.message.time_list[0][0];
                    existingRow.end_time = r.message.time_list[r.message.time_list.length - 1][1];
                } else {
                    // If the date doesn't exist, add a new row
                    $.each(r.message.time_list, function (j, time_slot) {
                        var start_time = time_slot[0];
                        var end_time = time_slot[1];
                        frm.add_child('booking', {
                            "date": date,
                            "start_time": start_time,
                            "end_time": end_time,
                            "status":"False"
                        });
                    });
                }
            });
            frm.refresh_field('booking');
        });
    }
    
});
