/**
 * Created with PyCharm.
 * User: ding
 * Date: 14-2-23
 * Time: 下午10:42
 * To change this template use File | Settings | File Templates.
 */



function init()
{
    $('#datetimepicker1').datetimepicker({
      language: 'pt-BR'
    });
    $('#datetimepicker2').datetimepicker({
      language: 'pt-BR'
    });

    
    for(var i=0;i<channelList.length ; i++)
    {
        var channelId = channelList[i].channelId;
        var dom = $('.'+channelId);
        dom.find('.download').text('下'+s_channel[channelId]['download']);
        dom.find('.play').text('播'+s_channel[channelId]['play']);

        var ctx = dom.next().find('.channelStatistic')[0].getContext("2d");
        var data = {
        labels : labels,
        datasets : [
            {
                fillColor : "rgba(41,43,54,0.5)",
                strokeColor : "rgba(41,43,54,1)",
                pointColor : "rgba(41,43,54,1)",
                pointStrokeColor : "#fff",
                data : s_channel[channelId]['data'][1]
            },
            {
                fillColor : "rgba(7,89,156,0.5)",
                strokeColor : "rgba(7,89,156,1)",
                pointColor : "rgba(7,89,156,1)",
                pointStrokeColor : "#fff",
                pointStrokeColor : "#fff",
                data : s_channel[channelId]['data'][0]
            }
        ]
        };
        var myNewChart = new Chart(ctx).Line(data);
    };


    // 显示合计数据

    var ctx = $('#myChart')[0].getContext("2d");
    var data = {
    labels : labels,
    datasets : [
        {
            fillColor : "rgba(41,43,54,0.5)",
            strokeColor : "rgba(41,43,54,1)",
            pointColor : "rgba(41,43,54,1)",
            pointStrokeColor : "#fff",
            data : s_sum[1]
        },
        {
            fillColor : "rgba(7,89,156,0.5)",
            strokeColor : "rgba(7,89,156,1)",
            pointColor : "rgba(7,89,156,1)",
            pointStrokeColor : "#fff",
            pointStrokeColor : "#fff",
            data : s_sum[0]
        }
    ]
    };
    var myNewChart = new Chart(ctx).Line(data);
}


function showCanvas(object)
{
    $(object).parents('tr').next().find('canvas').slideToggle();
}

function toggleChannel(object)
{
    var object = $(object);
    if(object.text() == "全部展开")
    {
        $('#channelStatistic canvas').slideDown();
        object.text('全部收起');
    }else
    {
        $('#channelStatistic canvas').slideUp();
        object.text('全部展开');
    }
}

$('document').ready(init)