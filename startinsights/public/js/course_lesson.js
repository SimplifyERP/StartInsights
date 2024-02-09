frappe.ui.form.on("Course Lesson",{
    refresh:function(frm){
        frm.fields_dict['custom_quiz_table'].grid.wrapper.find('.grid-add-row').remove(); 
        document.querySelectorAll("[data-fieldname='custom_create_quiz_table']")[1].style.backgroundColor = "#0BEBB5 "
    },
    custom_create_quiz_table(frm) {
        var currentAttempts = frm.doc.custom_quiz_table.length;
        var newMaxAttempts = frm.doc.custom_max_attempts;
        if (currentAttempts > newMaxAttempts) {
            // If current attempts exceed the new max attempts, remove excess rows
            for (var i = currentAttempts - 1; i >= newMaxAttempts; i--) {
                frm.get_field('custom_quiz_table').grid.grid_rows[i].remove();
            }
        } else if (currentAttempts < newMaxAttempts) {
            // If current attempts are less than the new max attempts, add new rows
            for (var j = currentAttempts; j < newMaxAttempts; j++) {
                frm.add_child('custom_quiz_table', {
                    'attempts': j + 1
                });
            }
        }
        frm.refresh_field('custom_quiz_table');
    } 
})