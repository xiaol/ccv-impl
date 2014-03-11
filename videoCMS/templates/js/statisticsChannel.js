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
                fillColor : "rgba(91,182,222,0.5)",
                strokeColor : "rgba(91,182,222,1)",
                pointColor : "rgba(91,182,222,1)",
                pointStrokeColor : "#fff",
                data : dataDaily[$(chart).attr('channelId')]
            }
        ]
        };
        var myNewChart = new Chart(ctx).Line(data);
    });

}

function requestChannelChart()
{
    var data = {}
    data.startDate = $('[name="startDate"]').val();
    data.endDate = $('[name="endDate"]').val();
    data.limit = $('[name="limit"]').val();
    data.channelIdList = $('[name="channelIdList"]').val();
    data.sort = $('[name="sort"]').val();


    $.ajax({
    type:'get',
    url:'/statistics2/channelAjax',
    data:data,
    success:function(html,textStatus)
    {
        $('#content').html(html);
        //初始化图标
        initChart();
    },
    error:function(XMLHttpRequest, textStatus, errorThrown)
    {
        alert(errorThrown);
    }
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
    requestChannelChart();

}
$(document).ready(init);