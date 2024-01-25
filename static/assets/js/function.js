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
        // Declare modal globally
        var modalInvoice = new bootstrap.Modal(document.getElementById('invoiceModal'));
        var modalQuotation = new bootstrap.Modal(document.getElementById('quotationModal'));
    
        var invoiceDetailsElement = document.getElementById('invoiceDetails');
        var agreementCheckbox = document.getElementById('termsCheckbox');
        var paymentMadeBtn = document.getElementById('paymentMadeBtn');
    
        // Attach event listener to approve buttons for invoices
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
    
                    // Show the modal
                    modalInvoice.show();
    
                    console.log('Modal displayed. Waiting for form submission...');
    
                    // Enable/disable "Payment made" button based on checkbox state
                    paymentMadeBtn.disabled = !agreementCheckbox.checked;
                })
                .catch(error => console.error('Error fetching invoice details:', error));
        });
    
        // Attach event listener to agreement checkbox for invoices
        agreementCheckbox.addEventListener('change', function () {
            // Enable/disable "Payment made" button based on checkbox state
            paymentMadeBtn.disabled = !this.checked;
        });
    
        // Function to check if both checkboxes are checked for invoices
        function areCheckboxesChecked() {
            return $('#refundCheckbox').prop('checked') && $('#termsCheckbox').prop('checked');
        }
    
        // Enable/disable button based on checkbox status for invoices
        $('#refundCheckbox, #termsCheckbox').change(function () {
            $('#paymentMadeBtn').prop('disabled', !areCheckboxesChecked());
        });
    
        // Attach event listener to approve buttons for quotations
        $('.def-btn.approve2').on('click', function () {
            var quotationId = $(this).data('quotation-id');
            console.log('Button clicked. Quotation ID:', quotationId);
    
            // Fetch and display quotation details
            console.log('Fetching quotation details...');
            fetchQuotationDetails(quotationId);
        });
    
        var quotationDetailsElement = document.getElementById('quotation-details');
    
        function fetchQuotationDetails(quotationId) {
            // Fetch details using quotationId
            fetch('/quotation-details/' + quotationId)
                .then(response => response.json())
                .then(data => {
                    console.log('Fetched quotation details:', data);
    
                    if (!quotationDetailsElement) {
                        console.error('Quotation details element is null.');
                        return;
                    }
    
                    // Update the modal content with the fetched details
                    quotationDetailsElement.innerHTML = `
                        <p>Quotation ID: <b>${data.quotation_id}</b></p>
                        <p>Quotation Number: <b>${data.quotation_number}</b></p>
    
                        <!-- Include the WalletUsageForm HTML here -->
                        <form id="walletUsageForm" data-quotation-id="${data.quotation_id}">
                            <!-- Add your form fields here -->
                            <div>
                                <label for="id_amount_used">Amount to use from wallet:</label>
                                <input type="text" name="amount_used" id="id_amount_used">
                            </div>
                            <button class="def-btn" type="submit">Submit</button>
                        </form>
                    `;
    
                    // Show the modal
                    modalQuotation.show();
    
                    // Add event listener for form submission
                    const walletUsageForm = document.getElementById('walletUsageForm');
                    walletUsageForm.addEventListener('submit', function (event) {
                        event.preventDefault();  // Ensure this line is present
    
                        // Handle form submission logic here
                        const amountUsed = document.getElementById('id_amount_used').value;
                        submitWalletUsageForm(data.quotation_id, amountUsed);
                    });
                })
                .catch(error => console.error('Error fetching quotation details:', error));
        }
    
        function submitWalletUsageForm(quotationId, amountUsed) {
            // Submit the form data using fetch
            fetch('/approve-quotation/' + quotationId + '/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({ amount_used: amountUsed }),
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Success:', data);
                    // Optionally, update the modal content or handle any additional UI updates
    
                    // Close the modal or perform other actions as needed
                    modalQuotation.hide();
                })
                .catch(error => {
                    console.error('Error:', error);
                    // Handle errors or display error messages
                });
        }
    
        // Helper function to get CSRF token from cookies
        function getCookie(name) {
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2) return parts.pop().split(';').shift();
        }
    });
    
    
    
    
    
    

});


