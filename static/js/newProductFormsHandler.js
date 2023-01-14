$(document).ready(function(){
    $(".select-category").change(function(){
        let value = $(this).val()
        console.log(value);
        let list = $(".select-subcategory")
        if (list[0].hasChildNodes()) {
            list.empty();
            $.ajax({
                url: '',
                type: 'get',
                data: {
                    category: value
                },
                success: function(response){
                    let subcategories = response.subcategories_to_return
                    $.each(subcategories,function(key, value){ 
                    $(".select-subcategory").append('<option class="subcategory-value">' + value + '</option>');
                    });
                }
            });
        };    
    });
    $("#enviroment_tax").change(function(){
        if ($("#enviroment_tax").is(':checked')) {
            $('.env-tax-input-field').removeClass("hidden")
        } else {
            $('.env-tax-input-field').addClass("hidden")
        }
    });
    $("#toggle_add_category_btn").click(function(){
        $("#category-form").removeAttr('hidden');
        $("#toggle_add_category_h").prop('hidden', true);
        $("#toggle_add_category_btn").prop('hidden', true);
        console.log("clicked")
    });
    $("#close-category-form").click(function(){
        $("#toggle_add_category_h").removeAttr('hidden');
        $("#toggle_add_category_btn").removeAttr('hidden');
        $("#category-form").prop('hidden', true);
        console.log("clicked")
    });
    $("#toggle_add_subcategory_btn").click(function(){
        $("#subcategory-form").removeAttr('hidden');
        $("#toggle_add_subcategory_h").prop('hidden', true);
        $("#toggle_add_subcategory_btn").prop('hidden', true);
        console.log("clicked")
    });
    $("#close-subcategory-form").click(function(){
        $("#toggle_add_subcategory_h").removeAttr('hidden');
        $("#toggle_add_subcategory_btn").removeAttr('hidden');
        $("#subcategory-form").prop('hidden', true);
        console.log("clicked")
    });
});