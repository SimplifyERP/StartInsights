frappe.ui.form.on("User",{
    cover_image:function(frm){
        if(frm.doc.cover_image){
            frm.set_value("user_image",frm.doc.cover_image)
        }
    }

})