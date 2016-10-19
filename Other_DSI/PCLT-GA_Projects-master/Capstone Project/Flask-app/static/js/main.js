console.log('linked')


var text_ltv = $("#cookie1");
var submit = document.getElementById("submit");
var ctx = document.getElementById("chart");


submit.addEventListener("click", function(){
  console.log("click")

    var dataToSend = {
      'age' : $('#age').val(),
      'dog_name' : $('#dog_name').val(),
      'sex' : $('#sex').val(),
      'neuter' : $('#neuter').val(),
      'colour' : $('#colour').val(),
      'mix' : $('#mix').val(),
      'breed1' : $('#breed1').val(),
      'breed2' : $('#breed2').val(),
      'intake' : $('#intake').val(),
      'condition' : $('#condition').val(),
      'month' : $('#month').val(),
      'total_number_dogs' : $('#total_number_dogs').val(),

    };
    $.ajax({
      'url' : 'result',
      'type' : 'GET',
      'data': dataToSend,
      'dataType' : 'JSON'
    })
      .done(function(response){
        var pred_string = response["prediction"]
        var labels = response["labels"]
        var vals = response["values"]
        var grp_vals = response["grp_values"]
        var dogs_name = response["dog_name"]
        help_text(pred_string);
        grapher(dogs_name, labels, vals, grp_vals)
        console.log(response);
      }
    )

//does this on click
function help_text(help){
  text_ltv.text(help)
}

function grapher(dog_name, labels, vals, grp_vals){


  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
    labels: labels,
    datasets: [
        {
            label: dog_name,
            fill: true,
            lineTension: 0.1,
            backgroundColor: "rgba(255,215,0,0.4)",
            borderColor: "rgba(255,215,0,1)",
            borderCapStyle: 'butt',
            borderDash: [],
            borderDashOffset: 0.0,
            borderJoinStyle: 'miter',
            pointBorderColor: "rgba(255,215,0,1)",
            pointBackgroundColor: "#fff",
            pointBorderWidth: 1,
            pointHoverRadius: 1,
            pointHoverBackgroundColor: "rgba(255,215,0,1)",
            pointHoverBorderColor: "rgba(220,220,220,1)",
            pointHoverBorderWidth: 2,
            pointRadius: 1,
            pointHitRadius: 10,
            data: vals,
            spanGaps: false,
        },
        {
            label: "Baseline",
            fill: true,
            lineTension: 0.1,
            backgroundColor: "rgba(169,169,169,0.4)",
            borderColor: "rgba(169,169,169,1)",
            borderCapStyle: 'butt',
            borderDash: [],
            borderDashOffset: 0.0,
            borderJoinStyle: 'miter',
            pointBorderColor: "rgba(169,169,169,1)",
            pointBackgroundColor: "#fff",
            pointBorderWidth: 1,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "rgba(169,169,169,1)",
            pointHoverBorderColor: "rgba(169,169,169,1)",
            pointHoverBorderWidth: 2,
            pointRadius: 1,
            pointHitRadius: 10,
            data: grp_vals,
            spanGaps: false,
        }

        // {
        //     label: "Lower Confidence",
        //     fill: false,
        //     lineTension: 0.1,
        //     backgroundColor: "rgba(255,255,255,0.4)",
        //     borderColor: "rgba(169,169,169,1)",
        //     borderCapStyle: 'butt',
        //     borderDash: [1,1],
        //     borderWidth: 2,
        //     borderDashOffset: 0.0,
        //     borderJoinStyle: 'miter',
        //     pointBorderColor: "rgba(169,169,169,1)",
        //     pointBackgroundColor: "#fff",
        //     pointBorderWidth: 1,
        //     pointHoverRadius: 5,
        //     pointHoverBackgroundColor: "rgba(169,169,169,1)",
        //     pointHoverBorderColor: "rgba(169,169,169,1)",
        //     pointHoverBorderWidth: 2,
        //     pointRadius: 1,
        //     pointHitRadius: 10,
        //     data: vals,
        //     spanGaps: false,
        // }

    ]
},
options: {
        scales: {
            yAxes: [{
                scaleLabel: {
                    display:true,
                    labelString: 'Probability of Still Being in Shelter'
                }
            }],
            xAxes: [{
                scaleLabel: {
                    display:true,
                    labelString: 'Days After Shelter Arrival'
                }
            }]
        }
    }

});

}



}, false);
