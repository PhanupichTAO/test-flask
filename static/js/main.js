$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        readURL(this);
    });

    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#result').text('ผลการจำแนก:');

                // Loop through data array and display each result, accuracy, and image
                data.forEach(function (item, index) {
                    var resultText = 'result ' + (index + 1) + ': ' + item.result + ' || ' + item.accuracy;

                    var imagePath = item.img_file.replace(/\\/g, '/');
                    var imageHtml = '<img src="' + imagePath + '" id="image_result" alt="Image" width="100">';
                    console.log(imageHtml);

                    // var imageHtml = '<img src="/uploads/image_1.png" alt="Image" width="200">';
                    $('#result').append('<br>' + resultText + '<br>' +
                        '<div class="image-chart-container">' +
                        '<div class="image-container">' + imageHtml + '</div>' +
                        '<div class="accuracy-chart-container">' +
                        '<canvas id="accuracyChart' + index + '" width="400" height="400"></canvas>' +
                        '</div>' +
                        '<div id="table-container' + index + '"></div>' +
                        '</div>');
                    // Parse accuracy values from percentage strings and convert to numerical values
                    var accuracyValues = data.map(function(item) {
                        return parseFloat(item.accuracy.replace('%', '')); // Remove '%' and parse as float
                    });

                    // Create a pie chart using Chart.js with accuracyValues
                    var ctx = document.getElementById('accuracyChart' + index).getContext('2d');
                    var accuracyChart = new Chart(ctx, {
                        type: 'pie',
                        data: {
                            labels: data.map(function(item) { return item.result; }), // Use result labels for the pie chart
                            datasets: [{
                                data: accuracyValues, // Use parsed accuracy values for the chart data
                                backgroundColor: [
                                    'rgba(255, 99, 132, 0.7)',
                                    'rgba(54, 162, 235, 0.7)',
                                    'rgba(255, 206, 86, 0.7)',
                                    'rgba(75, 192, 192, 0.7)',
                                    'rgba(153, 102, 255, 0.7)',
                                    'rgba(255, 159, 64, 0.7)'
                                ],
                                borderColor: [
                                    'rgba(255, 99, 132, 1)',
                                    'rgba(54, 162, 235, 1)',
                                    'rgba(255, 206, 86, 1)',
                                    'rgba(75, 192, 192, 1)',
                                    'rgba(153, 102, 255, 1)',
                                    'rgba(255, 159, 64, 1)'
                                ],
                                borderWidth: 0.1
                            }]
                        },
                        options: {
                            title: {
                                display: true,
                                text: 'Accuracy Chart'
                            }
                        }
                    });

                    // Generate the table
                    var tableHtml = '<table class="table">';
                    tableHtml += '<tr><th>Result</th><th>Accuracy</th></tr>';
                    data.forEach(function (item) {
                        tableHtml += '<tr><td>' + item.result + '</td><td>' + item.accuracy + '</td></tr>';
                    });
                    tableHtml += '</table>';

                    $('#table-container' + index).html(tableHtml);
                });

                console.log('Success!');
            },
            error: function (xhr, status, error) {
                // Handle error
                console.log(xhr.responseText);
            }
        });
    });

});
