$(function(){
    $.each($(".btn-add"),function(){
        $(this).click(function(){
            conf = $(this).parent().children(".config");
            module = conf.children(".module_name").html();
            app = conf.children(".app_name").html();
            id = conf.children(".obj_id").html();

            console.log(module);
            console.log(app);
            console.log(id);

        });
    });
    $.each($(".btn-del"),function(){
        $(this).click(function(){
            console.log(this);
        });
    });
});
