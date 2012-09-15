(function($) {
    $.extend($.fn, {
        controls: function(options) {
            var element = this;
            
            $.each($.fn.controls.bindings, function(selector, action) {
                element
                    .find(selector)
                    .each(action)
                    .end();
            });

            return this;
        }
    });

    $.fn.controls.bindings = {
    };
})(jQuery);
