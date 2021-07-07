function fetch_cart_item() {
    const mini_car_wrap = $(".mini-cart-wrap");
    $.ajax(
        {
            url: "/cart/cart_item",
            method: "GET",
            success: function (data) {
                $('.cart-list').remove();
                mini_car_wrap.append(data)
            },
            error: function (error) {
                console.log(error)
            }
        }
    )

}

function delete_product(url) {
    $.ajax(
        {
            url: url,
            method: "GET",
            success: function (data) {
                $('.cart-list').remove();
                fetch_cart_item();
                location.reload();
            },
            error: function (error) {
                console.log(error)
            }
        }
    )
}


$(document).ready(function () {
    const form = $(".form-product-ajax");
    form.submit(function (event) {
        event.preventDefault();
        const thisFrom = $(this);
        const action = thisFrom.attr('action');
        const method = thisFrom.attr('method');
        const data = thisFrom.serialize();
        $.ajax(
            {
                url: action,
                method: method,
                data: data,
                success: function (data) {

                    if (thisFrom.attr('is-wish-list-add') === 'true') {
                        if (data.add) {
                            $('.wish-list-notification').text(data.wish_list_count);
                        }
                        return;
                    }

                    $('.cart-notification').text(data.cart_item_count);

                    fetch_cart_item();
                    if (thisFrom.attr('is-wish-list') === 'true') {
                        location.reload()

                    }

                },
                error: function (error) {
                    console.log(error)
                }
            }
        )
    })

});

$(document).on('submit', '.form-product-model-ajax', function (event) {

    event.preventDefault();
    const thisFrom = $(this);
    const action = thisFrom.attr('action');
    const method = thisFrom.attr('method');
    const data = thisFrom.serialize();
    $('.modal').modal("hide");
    $.ajax(
        {
            url: action,
            method: method,
            data: data,
            success: function (data) {
                if (thisFrom.attr('is-wish-list-add') === 'true') {
                    if (data.add) {
                        $('.wish-list-notification').text(data.wish_list_count);
                    }
                    return;
                }
                $('.notification').text(data.cart_item_count);
                fetch_cart_item();
            },
            error: function (error) {
                console.log(error)
            }
        }
    )

});

function quick_view(id) {
    $.ajax(
        {
            url: '/quick_view/' + id,
            method: "GET",
            success: function (data) {

                const body = $('#quick_view');
                body.empty();
                body.append(data)


            },
            error: function (error) {
                console.log(error)
            }
        }
    )

}

$('.billing-address').hide();
$('.shipping-address').hide();

$(document).ready(function () {
    const elementBilling = $('.billing-address-toggle');
    elementBilling.click(function () {
        const billingForm = $('.billing-address form');

        billingForm.attr('action', elementBilling.attr('url'));
        $('.shipping-address').hide();
        $('.billing-address').toggle()

    });

    const element = $('.shipping-address-toggle');
    element.click(function () {
        const billingForm = $('.shipping-address form');
        billingForm.attr('action', element.attr('url'));
        $('.billing-address').hide();
        $('.shipping-address').toggle()
    })

});


$(document).ready(function () {
    window.setTimeout(function () {
        $(".alert").fadeTo(500, 0).slideUp(500, function () {
            $(this).remove();
        });
    }, 5000);
});
