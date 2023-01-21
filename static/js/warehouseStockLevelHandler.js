$(document).ready(function(){
    $(".warehouse-list-item").click(function(){
        let allWarehouseLists = $(".warehouse-list-item-content")
        $.each(allWarehouseLists, function(){
            allWarehouseLists.empty()
        })
        let warehouseId = $(this).attr('id')
        let warehouseProductList = $(this).next('.warehouse-list-item-content')
        if (warehouseProductList[0].hasChildNodes()) {
            warehouseProductList.empty()
        };
        $.ajax({
            url: '',
            type: 'get',
            data: {
                warehouseId: warehouseId
            },
            success: function(response){
                let product_list_name = response.stock_items_to_return_name
                console.log(typeof product_list_name)
                if (typeof product_list_name === 'object') {

                    let product_list_name = response.stock_items_to_return_name
                    let product_list_quantity = response.stock_items_to_return_quantity
                    let product_list_price = response.stock_items_to_return_price
                    let product_list_value = response.stock_items_to_return_value

                    let nameCount=0
                    $.each(product_list_name,function(key, value){
                        warehouseProductList.append('<div class="row stock-list-per-warehouse mt-4 mb-3"><div class="col-3 text-brown fs-5">' + value + '</div></div><hr>');
                        nameCount += 1
                    });
                    let quantityCount = 0
                    $.each(product_list_quantity,function(key, value){
                        $(".stock-list-per-warehouse").eq(quantityCount).append('<div class="col-3 text-brown fs-5">' + value + '</div>');
                        quantityCount +=1
                    });
                    let priceCount = 0
                    $.each(product_list_price,function(key, value){
                        $(".stock-list-per-warehouse").eq(priceCount).append('<div class="col-3 text-brown fs-5">' + value + '</div>');
                        priceCount +=1
                    });
                    let valueCount = 0
                    $.each(product_list_value,function(key, value){
                        $(".stock-list-per-warehouse").eq(valueCount).append('<div class="col-3 text-brown fs-5">' + value + '</div>');
                        valueCount +=1
                    });

                } else {
                    warehouseProductList.append('<div class="row stock-list-per-warehouse mt-4 mb-3"><div class="col-3 text-red fs-3 text">No Entries Found</div></div><hr>');
                }
            }
        });
    });
})