console.log("Hello World from function.js!")


$(document).ready(function() {
    console.log("I'm in")

    // Adding to wishlist
    $(document).on("click", ".add-to-wishlist", function(){
        let product_id = $(this).attr("data-product-item")
        let this_val = $(this)

        console.log("PRODUCT ID: ", product_id)

        $.ajax({
            url: '/add-to-wishlist',
            data: {
                'id': product_id,
            },
            dataType: 'json',
            beforeSend: function(){
                console.log("Adding to wishlist...")
            },
            success: function(response){
                this_val.html("✓")
                if (response.boolean === true){
                    console.log("Added to wishlist")
                }
                
            }
        })

    
    })

    // Removing from wishlist
    $(document).on("click", ".delete-wishlist-product", function(){
        let wishlist_id = $(this).attr("data-wishlist-product")
        let this_val = $(this)

        console.log("WISHLIST ID: ", wishlist_id)

        $.ajax({
            url: "/remove-from-wishlist",
            data: {
                'id': wishlist_id,
            },
            dataType: 'json',
            beforeSend: function(){
                console.log("Removing from wishlist...")
            },
            success: function(response){
                $("#wishlist-list").html(response.data)
            }
        });
    })

    // Add to cart
    $(".add-to-cart-btn").on("click", function(){

        let this_val = $(this)
        let index = this_val.attr("data-index")
        let quantity = $(".product-quantity-"+ index).val()
        let product_title = $(".product-title-"+ index).val()
        let product_image = $(".product-image-"+ index).val()
        let product_pid = $(".product-pid-"+ index).val()
        let product_id = $(".product-id-"+ index).val()
        let product_price = $("#current-product-price-"+ index).text()
    
    
        console.log("PRODUCT ID: ", product_id);
        console.log("PRODUCT PID: ", product_pid);
        console.log("PRODUCT QUANTITY: ", quantity);
        console.log("PRODUCT IMAGE: ", product_image);
        console.log("PRODUCT TITLE: ", product_title);
        console.log("PRODUCT PRICE: ", product_price);
    
        $.ajax({
            url: '/add-to-cart',
            data: {
                'id': product_id,
                'pid': product_pid,
                'qty': quantity,
                'image': product_image,
                'title': product_title,
                'price': product_price
            },
            dataType: 'json',
            beforeSend: function(){
                console.log('Adding products to cart...');
            },
            success: function(response){
                this_val.html("✓")
                console.log('Added products to cart!');
                $(".cart-items-count").text(response.totalcartitems)
                his_val.attr('disabled',false);

            }
        })
    })
    
    
    // To delete items from cart page
    
    $(".delete-product").on("click", function(){
    
        let product_id = $(this).attr("data-product")
        let this_val = $(this)
        console.log("PRODUCT ID: ", product_id)
    
        $.ajax({
            url:"/delete-from-cart",
            data:{
                "id":product_id,
            },
            dataType:'json',
            beforeSend:function(){
                this_val.hide();
            },
            success:function(response){
                this_val.show();
                $(".cart-items-count").text(response.totalcartitems)
                location.reload()
                // $("#cart-list").html(response.data)
            }
        })
    
    });
    
    
    // To update items from cart page
    
    $(".update-product").on("click", function(){
    
        let product_id = $(this).attr("data-product")
        let this_val = $(this)
        let product_qty = $(".product-qty-"+ product_id).val()
    
        console.log("PRODUCT ID: ", product_id);
        console.log("PRODUCT QTY: ", product_qty);
    
        $.ajax({
            url:'/update-cart',
            data:{
                'id':product_id,
                'qty':product_qty,
            },
            dataType:'json',
            beforeSend:function(){
                this_val.hide()
            },
            success:function(response){
                this_val.show()
                $(".cart-items-count").text(response.totalcartitems)
                location.reload()
                // $("#cart-list").html(response.data)
            }
        })
    
    });

 

    $(document).ready(function () {
        var modal = new bootstrap.Modal(document.getElementById('invoiceModal'));
        var invoiceDetailsElement = document.getElementById('invoiceDetails');
    
        // Attach event listener to approve buttons
        $('.def-btn.approve').on('click', function () {
            var invoiceId = $(this).data('invoice-id');
            var invoiceUrl = $(this).data('invoice-url');
            console.log('Button clicked. Invoice ID:', invoiceId);
            console.log('Invoice URL:', invoiceUrl);
    
            // Fetch and display invoice details
            console.log('Fetching invoice details...');
            fetch(invoiceUrl)
                .then(response => response.json())
                .then(data => {
                    console.log('Fetched data:', data);
    
                    if (!invoiceDetailsElement) {
                        console.error('Invoice details element is null.');
                        return;
                    }
    
                    // Update the modal content with the fetched details
                    invoiceDetailsElement.innerHTML = `
                        <p>Account name: <b>${data.account_name}</b></p>
                        <p>Account number: <b>${data.account_number}</b></p>
                        <p>Amount to be Paid: <b>Rs ${data.amount_to_be_paid}</b></p>
                    `;
    
                    modal.show();
                })
                .catch(error => console.error('Error fetching invoice details:', error));
        });
    });
    

    // $(document).ready(function () {
    //     // Function to check if both checkboxes are checked
    //     function areCheckboxesChecked() {
    //         return $('#refundCheckbox').prop('checked') && $('#termsCheckbox').prop('checked');
    //     }
    
    //     // Enable/disable button based on checkbox status
    //     $('#refundCheckbox, #termsCheckbox').change(function () {
    //         $('#paymentMadeBtn').prop('disabled', !areCheckboxesChecked());
    //     });
    
    //     // Handle button click
    //     $('#paymentMadeBtn').click(function () {
    //         if (areCheckboxesChecked()) {
    //             // Log payload data before sending AJAX request
    //             var payloadData = {
    //                 csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
    //             };
    
    //             // Get the invoice ID (replace 'your_invoice_id_field' with the correct field)
    //             var invoiceId = $('#your_invoice_id_field').val();
                
    //             // Include invoice_id in the payload data
    //             payloadData.invoice_id = invoiceId;
    
    //             console.log('AJAX Request Payload:', payloadData);
    
    //             // Send email and handle redirection
    //             sendPaymentConfirmation(payloadData);
    //         } else {
    //             alert('Please check the checkboxes before proceeding.');
    //         }
    //     });
    
    //     // Function to send payment confirmation email and handle redirection
    //     function sendPaymentConfirmation(payloadData) {
    //         // AJAX request to send email
    //         $.ajax({
    //             url: '/send-payment-confirmation/',
    //             type: 'POST',
    //             data: payloadData,
    //             success: function (response) {
    //                 // Redirect to payment confirmation page using invoice_id from the response
    //                 window.location.href = '/payment-confirmation/' + response.invoice_id + '/';
    //             },
    //             error: function (error) {
    //                 console.error('Error sending payment confirmation email:', error);
    //                 alert('An error occurred. Please try again later.');
    //             }
    //         });
    //     }
    // });
    
    
    $(document).ready(function () {
        // Function to check if both checkboxes are checked
        function areCheckboxesChecked() {
            return $('#refundCheckbox').prop('checked') && $('#termsCheckbox').prop('checked');
        }
    
        // Enable/disable button based on checkbox status
        $('#refundCheckbox, #termsCheckbox').change(function () {
            $('#paymentMadeBtn').prop('disabled', !areCheckboxesChecked());
        });
    });
    


    
    
    
    
    

});


