console.log("Hello World from function.js!")


$(document).ready(function() {
    console.log("I'm in")

    $(document).on("submit", "#contact-form-ajax", function(){

        // e.preventDefault()
        console.log("Contact us form submitted")
    
        let first_name = $("#first_name").val()
        let last_name = $("#last_name").val()
        let email = $("#email").val()
        let phone_number = $("#phone_number").val()
        let address = $("#address").val()
        let floor_level = $("#floor_level").val()
        let furniture_type = $("#furniture_type").val()
        let description = $("#description").val()
    
        console.log("FIRST NAME: ", first_name)
        console.log("LAST NAME: ", last_name)
        console.log("EMAIL: ", email)
        console.log("PHONE NUMBER: ", phone_number)
        console.log("ADDRESS: ", address)
        console.log("FLOOR LEVEL: ", floor_level)
        console.log("FURNITURE TYPE: ", furniture_type)
        console.log("DESCRIPTION: ", description)
    
        $.ajax({
            url: '/ajax-contact-form',
            data: {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone_number': phone_number,
                'address': address,
                'floor_level': floor_level,
                'furniture_type': furniture_type,
                'description': description,
            },
            dataType: 'json',
            beforeSend: function(){
                console.log("Sending message...")
            },
            success: function(response){
                console.log("Message sent")
                $("#contact-form-ajax").hide()
                $("#message-response").html("Thank you for reaching out, we will contact you shortly.")
            }
        })
    })




    // $(".filter-checkbox").on("click", function(){
    //     console.log("a checkbox has been clicked")

    //     let filter_object = {}

    //     $(".filter-checkbox").each(function() {
    //         let filter_value = $(this).val()
    //         let filter_key = $(this).data("filter")

    //         filter_object[filter_key] = Array.from(document.querySelectorAll(`input[data-filter="${filter_key}"]:checked`)).map(function(el) {
    //             return el.value
    //         })
    //     })
    //     console.log("Filter Object: ", filter_object)
    //     $.ajax({
    //         url: '/filter-products',
    //         data: filter_object,
    //         dataType: 'json',
    //         beforeSend: function() {
    //             console.log("loading...")
    //         },
    //         success: function(response) {
    //             $("#filtered-product").html(response.data)
    //         }
    //     })

    // })


    // Info from Contact Us page

});
