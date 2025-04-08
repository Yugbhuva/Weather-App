// script.js - Client-side functionality for the Weather App

$(document).ready(function() {
    // Get location from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const location = urlParams.get('location');
    
    // Set the location input field value if it exists in the URL
    if (location) {
        $('#location').val(location);
    }
    
    // Initialize autocomplete for the location input
    $('#location').autocomplete({
        source: function(request, response) {
            $.ajax({
                url: '/api/city-suggestions',
                dataType: 'json',
                data: {
                    q: request.term
                },
                success: function(data) {
                    response(data);
                }
            });
        },
        minLength: 2, // Only trigger autocomplete after 2 characters
        select: function(event, ui) {
            $('#location').val(ui.item.value);
            // If you want to auto-submit after selection
            // $('form').submit();
        }
    }).autocomplete("instance")._renderItem = function(ul, item) {
        // Customize the appearance of dropdown items
        return $("<li>")
            .append("<div class='autocomplete-item'>" + item.label + "</div>")
            .appendTo(ul);
    };
    
    // Optional: Implement geolocation functionality
    const geolocateUser = () => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(position => {
                const coords = `${position.coords.latitude},${position.coords.longitude}`;
                $('#location').val(coords);
                // Auto-submit the form with the coordinates
                $('form').submit();
            }, error => {
                console.error('Error getting location:', error);
            });
        }
    };
    
    // Add geolocation button if you want to implement this feature
    // $('#geolocate-btn').on('click', geolocateUser);
});