function initChart()
{

    $(".myChart").each(function(i,chart)
    {
        console.log(daySequence);
        console.log($(chart).attr('channelId'));
        console.log(dataDaily[$(chart).attr('channelId')]);
        var ctx = chart.getContext("2d");
        var data = {
        labels : daySequence,
        datasets : [
            {
                fillColor : "rgba(151,187,205,0.5)",
                strokeColor : "rgba(151,187,205,1)",
                pointColor : "rgba(151,187,205,1)",
                pointStrokeColor : "#fff",
                data : dataDaily[$(chart).attr('channelId')]
            }
        ]
        }
        var myNewChart = new Chart(ctx).Line(data);
    });

}

function init()
{
	$('#datetimepicker1').datetimepicker({
      language: 'pt-BR'
    });
    $('#datetimepicker2').datetimepicker({
      language: 'pt-BR'
    });

    //初始化图标
    initChart();
}
$(document).ready(init);