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


// bind the admin dialog add
var get_model_to_create = (function(hiddens){
    $.ajax({
        type: 'POST',
        url: contentblocks_ajax_receiver,
        data: "st=add-req",
        success: function(json){
            // get all posibles objects
            if (json.st == "error"){
                admin_dialog_reset(json.data);

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
                admin_dialog_reset("Une erreur est survenue.");
            }else{
                admin_dialog_reset(create_form(hiddens+json.form));
                $("#admin-form-valid").click(function(){
                    admin_dialog.dialog2("close");
                    //le form est envoyé via la iframe a cause des fichiers >> formUploadCallback
                });
            }
            admin_dialog.dialog2("open");
        },
        datatype : "json"
    });
});
//bind the remove event
var get_model_to_remove = (function(module,app,id){
    data = "st=del-content&app_name="+app+"&module_name="+module+"&obj_id="+id;
    $.ajax({
        type: 'POST',
        url: contentblocks_ajax_receiver,
        data: data,
        success: function(json){
            if (json.st == "error"){
                admin_dialog_reset(json.data);
                admin_dialog.dialog2("open");
            }else{
                containeur = $('.config[module_name="'+module+'"][app_name="'+app+'"][obj_id="'+id+'"]').parent();
                containeur.remove();
            }
        },
        datatype : "json"
    });

});

var add_to_containeur = (function(id,html){
    containeur = $('.config[module_name="pagecontaineur"][app_name="contentblocks"][obj_id="'+id+'"]');
    containeur.after(html);
    $(".contentblocks.containeur").sortable("refresh");
    //$( ".contentblocks.admin-resizable" ).resizable("refresh");
});

//callback
var formUploadCallback = (function(result) {
    admin_dialog.dialog2("close");
    if(result.st =="ok"){
        if (result.data.type == "add"){
            add_to_containeur(result.data.containeur_id,result.data.html);
        }else {
            admin_dialog_reset("unknow succes type. reload page to see the changes?");
            admin_dialog.dialog2("open");
        }
    }else{//err"refresh");r
        if (result.data.type == "form"){
            admin_dialog_reset(create_form(result.data.form));
        }else {
            admin_dialog_reset("unknow error");
        }
        admin_dialog.dialog2("open");
    }
});

$(function(){
    var uploaders = [];
    $.each($(".contentblocks.containeur.admin-drop"),function(){
        elem = $(this).children(".drop-zone")[0];
        conf = $($(this).children(".config")[0]);

        module = conf.attr("module_name");
        app = conf.attr("app_name");
        id = conf.attr("obj_id");
        pos = conf.attr("obj_position");
        parent_id = conf.attr("obj_id");
        data = {"app_name" :app, "module_name":module,"obj_id":id,"parent_id":parent_id,"st" :"upload-file"};

        var uploader = new qq.FileUploader({
            element: elem,
            params : data,
            //uploadButtonText : "",
            action: contentblocks_ajax_uploader,
            customHeaders : {"X-CSRFToken" : $.cookie('csrftoken')},
            showMessage : function(data){
                //console.log(data);
            },
            onComplete: function(id,fileName,json){
                if (json.st == "error"){
                    admin_dialog_reset(json.data);
                    admin_dialog.dialog2("open");
                }else{
                    add_to_containeur(json.data.containeur_id,json.data.html);
                }
            }
        });          
        uploaders.push(uploader);
    });

    $(document).on("click",".btn-add",function(){
        conf = $($(this).parent().children(".config")[0]);
        module = conf.attr("module_name");
        app = conf.attr("app_name");
        id = conf.attr("obj_id");
        hiddens = create_hidden("st","add-content") + create_hidden("app_name",app) + create_hidden("module_name",module) + create_hidden("obj_id",id);

        get_model_to_create(hiddens);
        return false;
    });

    $(document).on("click",".btn-del",function(){
        conf = $($(this).parent().children(".config")[0]);
        module = conf.attr("module_name");
        app = conf.attr("app_name");
        id = conf.attr("obj_id");
        get_model_to_remove(module,app,id);
        return false;
    });

    $(".contentblocks.containeur.admin-drop").sortable({
        connectWith: ".contentblocks.containeur",
        //handle : "div",
        items : ".contentblocks.object.admin-dragg",
        forceHelperSize: true,
        forcePlaceholderSize: true,
        opacity: 0.6,
        placeholder: 'highlight',
        stop : function(event,data){
            maj_dragg_object(data);
        }
    });



    /*$(".ui-resizable").sortable("disable");

    $( ".contentblocks.admin-resizable" ).resizable({
        maxWidth: 900,
        containment: "parent",
        stop : function(event,data){
            maj_dragg_object(data);
        }
    });*/
});

var maj_dragg_object = (function(data){
    obj = data.item;
    pre = obj.prev();
    c = pre.attr("class");
    pos = 0;
    if(c != "config" && c!= "drop-zone" && c!= "btn btn-success btn-add"){
        pos = parseInt(pre.children(".config").attr("obj_position")) + 1;
    }

    conf = $($(obj).children(".config")[0]);
    conf.attr("obj_position",pos);

    obj.nextAll().each(function(i){
        c = $($(this).children(".config")[0]);
        c.attr("obj_position",++pos);
    });

    module = conf.attr("module_name");
    app = conf.attr("app_name");
    id = conf.attr("obj_id");
    pos = conf.attr("obj_position");
    parent_id = $(obj.parent().children(".config")[0]).attr("obj_id");
    data = "app_name="+app+"&module_name="+module+"&obj_id="+id+"&obj_position="+pos+"&parent_id="+parent_id;
    send_maj_object(data);
});

var send_maj_object = (function(data){
    $.ajax({
        type: 'POST',
        url: contentblocks_ajax_receiver,
        data: "st=obj-maj&"+data,
        success: function(json){
            if (json.st == "error"){
                admin_dialog_reset(json.data);
                admin_dialog.dialog2("open");
            }
        }
    });
});
