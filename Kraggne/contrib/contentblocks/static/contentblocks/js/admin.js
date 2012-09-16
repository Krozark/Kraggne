//utils for creat form
var create_selector = (function(choices){
    res = '<select id="admin-selector" name="admin-selector">';
    for(u in choices){
        res += '<option value="'+choices[u][0]+'">'+choices[u][1]+'</option>';
    }
    res += '</select>';
    return res;
});

var create_hidden = (function(name,value){
    return '<input type="hidden" value="'+value+'" name="'+name+'">'
});


var create_ajax_form = (function(input){
    form = input;
    form +='<div class="form-actions"><a class="btn btn-success" type="submit" id="admin-form-valid">Send<a/></div>';
    return form;
});


// bind the admin dialog
var get_model_to_create = (function(hiddens){
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
                    hiddens += create_hidden("contenttype_pk",v);

                    create_form_from_contenttype(hiddens,v);
                });
            } 
            admin_dialog.dialog2("open");
        },
        datatype : "json"
    });

});

var create_form_from_contenttype = (function(hiddens,contenttype_pk){
    $.ajax({
        type: 'POST',
        url: contentblocks_ajax_receiver,
        data: "st=get-form&contenttype_pk="+contenttype_pk,
        success: function(json){
            if (json.st == "error"){
                admin_dialog_reset("Une erreur est suvenue.");
            }else{
                admin_dialog_reset(create_form(hiddens+json.form));
                $("#admin-form-valid").click(function(){
                    admin_dialog.dialog2("close");
                    //le form est envoyé via la iframe a cause des fichiers >> formUploadCallback
                });
            }
            admin_dialog.dialog2("open");
        }
    });
});

var formUploadCallback = (function(result) {
    admin_dialog.dialog2("close");
    if(result.st =="ok"){
        if (result.data.type == "add"){
            admin_dialog_reset("success");
        }else {
            admin_dialog_reset("unknow succes type. reload page to see the changes?");
        }
    }else{//error
        if (result.data.type == "form"){
            admin_dialog_reset(create_form(result.data));
        }else {
            admin_dialog_reset("unknow error");
        }
    }
    admin_dialog.dialog2("open");
});

$(function(){
    $.each($(".btn-add"),function(){
        // + on containeur
        $(this).click(function(){
            conf = $(this).parent().children(".config");
            module = conf.children(".module_name").html();
            app = conf.children(".app_name").html();
            id = conf.children(".obj_id").html();
            hiddens = create_hidden("st","add-content") + create_hidden("app_name",app) + create_hidden("module_name",module) + create_hidden("obj_id",id);

            get_model_to_create(hiddens);
        });
    });

    $.each($(".btn-del"),function(){
        $(this).click(function(){
        });
    });
});
