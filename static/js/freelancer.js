(function($) {
  "use strict"; // Start of use strict

  // Smooth scrolling using jQuery easing
  $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: (target.offset().top - 70)
        }, 1000, "easeInOutExpo");
        return false;
      }
    }
  });

  // Scroll to top button appear
  $(document).scroll(function() {
    var scrollDistance = $(this).scrollTop();
    if (scrollDistance > 100) {
      $('.scroll-to-top').fadeIn();
    } else {
      $('.scroll-to-top').fadeOut();
    }
  });

  // Closes responsive menu when a scroll trigger link is clicked
  $('.js-scroll-trigger').click(function() {
    $('.navbar-collapse').collapse('hide');
  });

  // Activate scrollspy to add active class to navbar items on scroll
  $('body').scrollspy({
    target: '#mainNav',
    offset: 80
  });

  // Collapse Navbar
  var navbarCollapse = function() {
    if ($("#mainNav").offset().top > 100) {
      $("#mainNav").addClass("navbar-shrink");
    } else {
      $("#mainNav").removeClass("navbar-shrink");
    }
  };
  // Collapse now if page is not at top
  navbarCollapse();
  // Collapse the navbar when page is scrolled
  $(window).scroll(navbarCollapse);

  // Floating label headings for the contact form
  $(function() {
    $("body").on("input propertychange", ".floating-label-form-group", function(e) {
      $(this).toggleClass("floating-label-form-group-with-value", !!$(e.target).val());
    }).on("focus", ".floating-label-form-group", function() {
      $(this).addClass("floating-label-form-group-with-focus");
    }).on("blur", ".floating-label-form-group", function() {
      $(this).removeClass("floating-label-form-group-with-focus");
    });
  });

  // //Chart updating info
  // $(function(){
  //       let chart = document.querySelector('canvas').chart;
  //
  //       $(document).on('click', function(){
  //
  //           // When the document is clicked, update the chart
  //           // with a random value and animate it.
  //
  //           chart.data.datasets[0].data[2] = Math.random()*10000;
  //           chart.update();
  //       });
  // });


  $(function() {

    // ajax request to get list of regions and populate region dropdowns
    $.ajax({
      url: "/_get_all_regions",
      dataType: "json",
      success: function (data) {
        //$('#region-dropdown-regions-2').append(new Option('None', 'None'));
        $('#region-dropdown-regions-2').append('<a role="presentation" class="dropdown-item">None</a>');
        $('#region-dropdown-regions-3').append('<a role="presentation" class="dropdown-item">None</a>');
        $.each(data, function (val, text) {
          $('#region-dropdown-regions-1').append('<a role="presentation" class="dropdown-item">'+ text +'</a>');
          $('#region-dropdown-regions-2').append('<a role="presentation" class="dropdown-item">'+ text +'</a>');
          $('#region-dropdown-regions-3').append('<a role="presentation" class="dropdown-item">'+ text +'</a>');
          $('#region-dropdown-price').append('<a role="presentation" class="dropdown-item">'+ text +'</a>');
        });
      }

    });

  });

  $(document).on('click', '.dropdown-menu a', function () {
      console.log("Selected Option:"+$(this).text());
    $(this).parents(".dropdown").find('.btn').html($(this).text() + ' <span class="caret"></span>');
    $(this).parents(".dropdown").find('.btn').val($(this).data('value'));
  });

  $('#submit-button-regions').click(function () {

    //check that form is filled out properly
    if ($('#region1-btn').text() != "Select a Region" && $('#time-period-btn').text() !== "Select a Length of Time" &&
        $('#date-picker-regions').val() !== "" && $('#volume-price-btn').text() !== "Select a Region"){
        var arr = [$('#region1-btn').text(), $('#region2-btn').text(), $('#region3-btn').text(),
        $('#time-period-btn').text(), $('#date-picker-regions').val(), $('#volume-price-btn').text()]
    } else{
      alert("Please ensure all fields are filled out.")
    }

    console.log($('#date-picker-regions').val())
    console.log(JSON.stringify({html_data: arr}))

    // // send filters
    $.ajax({
        url: '/region_graph_filters',
        type: 'POST',
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify({html_data: arr}),
        success: function(data) {

            // Identify which regions are being displayed
            var region1_name =$('#region1-btn').text();
            var region2_name =$('#region2-btn').text();
            var region3_name =$('#region3-btn').text();
            var type_of_data =$('#volume-price-btn').text();
            var y_axis_label = "Volume, Number of Avocados Sold"
            var x_axis_label = ""

            // Modify type_of_data label to better fit y axis label later when creating the graph
            if (type_of_data === "Price "){
                type_of_data = "Prices";
                y_axis_label = "Price Per Avocado In Dollars ($)";
            }
            else{
                type_of_data = "Volume";
            }

            //set x-axis label
            if ($('#time-period-btn').text() === "Three Months "){
                x_axis_label = "Time (Months)";
            }
            else if ($('#time-period-btn').text() === "One Year "){
                x_axis_label = "Time (Quarterly)";
            }
            else if ($('#time-period-btn').text() === "All Time "){
                x_axis_label = "Time (Yearly)";
            }

            // Check that region 2 is not none or "Select a Region "
            // If it is and the length of the data is 3 then set region2_name equal to region3_name
            // because there's only two regions being displayed
            if (region2_name === "None " || region2_name === "Select a Region"){
                region2_name = region3_name
            }


            //Get region1 data for Chart.js
            var region1 = JSON.parse(data[0])

            for( var k = 0; k < region1.length; ++k ) {
                region1[k]['x'] = moment(region1[k]['x'])//new Date(region1[k]['x']).getTime();
            }

            // remove old canvas (chart) element and create a new one
            // this is
            $('#myChart').remove(); // this is my <canvas> element
            $('#chart_div').append('<canvas id="myChart"><canvas>');

            if (data.length == 1){
                console.log(region1);
                var ctx = document.getElementById('myChart').getContext('2d');
                var scatterChart = new Chart(ctx, {
                type: 'scatter',
                data: {
                    datasets: [{
                        label: region1_name,
                        data: region1,
                        backgroundColor: 'rgba(245, 66, 66, 0.5)'
                    }]
                },
                options: {
                    scales: {
                        xAxes: [{
                            type: 'time',
                            position: 'bottom',
                            scaleLabel: {
                                display: true,
                                labelString: x_axis_label
                            }
                        }],
                        yAxes: [{
                            ticks: {
                                // Include a dollar sign in the ticks
                                callback: function(value, index, values) {
                                    if (type_of_data == "Prices") {
                                        return '$' + value;
                                    }
                                    else{
                                        return value;
                                    }
                                }
                            },
                            scaleLabel: {
                                display: true,
                                labelString: y_axis_label
                            }
                        }]
                    },
                    title: {
                        display: true,
                        text: 'Avocado ' + type_of_data + ' In ' + region1_name + "Over Time"
                    }
                }
            });
                console.log(region1);
            };

            if (data.length == 2){

                //Get region2 data for Chart.js
                var region2 = JSON.parse(data[1])

                for( var k = 0; k < region2.length; ++k ) {
                    region2[k]['x'] = moment(region2[k]['x'])//new Date(region1[k]['x']).getTime();
                }

                var ctx = document.getElementById('myChart').getContext('2d');
                var scatterChart = new Chart(ctx, {
                type: 'scatter',
                data: {
                    datasets: [{
                        label: region1_name,
                        data:   region1,
                        backgroundColor: 'rgba(245, 66, 66, 0.5)'
                    },
                        {label: region2_name,
                        data:   region2,
                        backgroundColor: 'rgba(75, 66, 245, 0.5)'}]
                },
                options: {
                    scales: {
                        xAxes: [{
                            type: 'time',
                            position: 'bottom',
                            scaleLabel: {
                                display: true,
                                labelString: x_axis_label
                            }
                        }],
                        yAxes: [{
                            ticks: {
                                // Include a dollar sign in the ticks
                                callback: function(value, index, values) {
                                    if (type_of_data == "Prices"){
                                       return '$' + value;
                                    }
                                    else{
                                        return value;
                                    }
                                }
                            },
                            scaleLabel: {
                                display: true,
                                labelString: y_axis_label
                            }
                        }]
                    },
                    title: {
                        display: true,
                        text: 'Avocado ' + type_of_data + ' In ' + region1_name + "And " + region2_name + "Over Time"
                    }
                }
            });
            };

            if (data.length == 3){

                //Get region2 data for Chart.js
                var region2 = JSON.parse(data[1])

                for( var k = 0; k < region2.length; ++k ) {
                    region2[k]['x'] = moment(region2[k]['x'])
                }

                //Get region2 data for Chart.js
                var region3 = JSON.parse(data[2])

                for( var k = 0; k < region3.length; ++k ) {
                    region3[k]['x'] = moment(region3[k]['x'])
                }

                var ctx = document.getElementById('myChart').getContext('2d');
                var scatterChart = new Chart(ctx, {
                type: 'scatter',
                data: {
                    datasets: [{
                        label: region1_name,
                        data:   region1,
                        backgroundColor: 'rgba(245, 66, 66, 0.5)'
                    },
                        {label: region2_name,
                        data:   region2,
                         backgroundColor: 'rgba(75, 66, 245, 0.5)'},
                        {label: region3_name,
                        data:   region3,
                         backgroundColor: 'rgba(38, 255, 0, 0.5)'}]
                },
                options: {
                    scales: {
                        xAxes: [{
                            type: 'time',
                            position: 'bottom',
                            scaleLabel: {
                                display: true,
                                labelString: x_axis_label
                            }
                        }],
                        yAxes: [{
                            ticks: {

                                callback: function(value, index, values) {
                                    if (type_of_data == "Prices"){
                                       return '$' + value;
                                    }
                                    else{
                                        return value;
                                    }
                                }
                            },
                            scaleLabel: {
                                display: true,
                                labelString: y_axis_label
                            }
                        }]
                    },
                    title: {
                        display: true,
                        text: 'Avocado ' + type_of_data + ' In ' + region1_name + ", " + region2_name + ", and " + region3_name + "Over Time"
                    }
                }
            });
            };

          }
    })
  })



 
})(jQuery); // End of use strict

