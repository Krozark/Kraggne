$(function(){
    $.each($(".btn-add"),function(){
        // + on containeur
        $(this).click(function(){
            conf = $(this).parent().children(".config");
            module = conf.children(".module_name").html();
            app = conf.children(".app_name").html();
            id = conf.children(".obj_id").html();
            hiddens = '<div style="display:none">' + create_hidden("st","add-content") + create_hidden("app_name",app) + create_hidden("module_name",module) + create_hidden("obj_id",id) + "</div>";

            $.ajax({
                type: 'POST',
                url: contentblocks_ajax_receiver,
                data: "st=add-req",
                success: function(json){
                    // get all posibles objects
                    if (json.st == "error"){
                        admin_dialog_reset("Une erreur est suvenue.");

                    }else{
                        form = create_ajax_form(create_selector(json.choices));
                        admin_dialog_reset(form);
                        $("#admin-form-valid").click(function(){
                            // send choice
                            admin_dialog.dialog2("close");
                            v = $("#admin-selector").val();
                            $.ajax({
                                type: 'POST',
                                url: contentblocks_ajax_receiver,
                                data: "st=get-form&contenttype_pk="+v,
                                success: function(json){
                                    if (json.st == "error"){
                                        admin_dialog_reset("Une erreur est suvenue.");

                                    }else{
                                        admin_dialog_reset(create_form(hiddens+json.form));
                                        admin_dialog.dialog2("open");
                                        $("#admin-form-valid").click(function(){
                                            admin_dialog.dialog2("close");
                                        });
                                    }
                                }
                            });
                        });
                    } 
                    admin_dialog.dialog2("open");
                },
                datatype : "json"
            });

        });
    });
    $.each($(".btn-del"),function(){
        $(this).click(function(){
        });
    });
});
