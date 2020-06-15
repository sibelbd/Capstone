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
            console.log(data);

            var x_axis_label = ""
            var y_axis_label = ""

            //Get region1 data for Chart.js
            var region1 = JSON.parse(data[0])
            var region1_date = []
            var region1_vol_price = []
            var region1_data_final = {}

            for( var k = 0; k < region1.length; ++k ) {
                console.log(moment(region1[k]['x']).format('MM-YYYY'));
                region1[k]['x'] = moment(region1[k]['x'])//new Date(region1[k]['x']).getTime();

            }

            // // if (data.length == 1){
            //     var ctx = document.getElementById('myChart').getContext('2d');
            //     var myChart = new Chart(ctx, {
            //         type: 'scatter',
            //         datasets:[{
            //             label: "Region1 Data",
            //             data: region1_data_final
            //         }],
            //         options: {
            //             scales: {
            //                 xAxes: [{
            //                     type: 'time',
            //                   }],
            //             }
            //         }
            //     });

                console.log(region1);
                var ctx = document.getElementById('myChart').getContext('2d');
                var scatterChart = new Chart(ctx, {
                type: 'scatter',
                data: {
                    datasets: [{
                        label: 'Scatter Dataset',
                        data:   region1
                    }]
                },
                options: {
                    scales: {
                        xAxes: [{
                            type: 'time',
                            position: 'bottom'
                        }]
                    }
                }
            });
                console.log(region1);


            // }
            //
            // else if (data.length === 2){
            //     //Get region2 data for Chart.js
            //     var region2 = JSON.parse(data[0])
            //     var region2_date = []
            //     var region2_vol_price = []
            //
            //     var next_element = false;
            //     $.each(region2, function(axis_label, data) {
            //       //from within the date key of the region 1 json, take each element and add it to region1_date list
            //       if (next_element === false){
            //         $.each(data, function(index, element) {
            //           //from within the date key of the region 1 json, take each element and add it to region1_date list
            //           region2_date.push(new Date(element))
            //         });
            //       }
            //       if (next_element === true){
            //         $.each(data, function(index, element) {
            //           //from within the date key of the region 1 json, take each element and add it to region1_date list
            //           region2_vol_price.push(element)
            //         });
            //       }
            //
            //       next_element = true;
            //     });
            // }
            // else if (data.length === 3){
            //     //Get region3 data for Chart.js
            //     var region3 = JSON.parse(data[0])
            //     var region3_date = []
            //     var region3_vol_price = []
            //
            //     var next_element = false;
            //     $.each(region3, function(axis_label, data) {
            //       //from within the date key of the region 1 json, take each element and add it to region1_date list
            //       if (next_element === false){
            //         $.each(data, function(index, element) {
            //           //from within the date key of the region 1 json, take each element and add it to region1_date list
            //           region3_date.push(new Date(element))
            //         });
            //       }
            //       if (next_element === true){
            //         $.each(data, function(index, element) {
            //           //from within the date key of the region 1 json, take each element and add it to region1_date list
            //           region3_vol_price.push(element)
            //         });
            //       }
            //
            //       next_element = true;
            //     });}
            //
            // //condition for y-axis label to format average price nicely, since volume is already formatted
            // if (y_axis_label == "AveragePrice"){
            //     y_axis_label = "Average Price"
            // }


              // console.log(region1_date);
              // console.log(region1_vol_price);
              // console.log(region1_data_final);

          }

    })
  })

 
})(jQuery); // End of use strict

