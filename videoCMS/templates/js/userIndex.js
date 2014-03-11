/**
 * Created with PyCharm.
 * User: ding
 * Date: 14-2-23
 * Time: 下午10:42
 * To change this template use File | Settings | File Templates.
 */

function showTips(e)
{
	$(e.target).tooltip('show');
}

function hideTips(e)
{
	$(e.target).tooltip('hide');
}

function initTips()
{
	$('[data-toggle="tooltip"]').bind("mouseover",showTips);
	$('[data-toggle="tooltip"]').bind("mouseout",hideTips);
}

function init()
{
    initTips();

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

        var downManualColor = '238,123,0';
        var downSpiderColor = '238,123,0';
        var playManualColor = '56,119,189';
        var playSpiderColor = '56,119,189';
        var data = {
        labels : labels,
        datasets : [
            {
                fillColor : "rgba("+downManualColor+",0.5)",
                strokeColor : "rgba("+downManualColor+",1)",
                pointColor : "rgba("+downManualColor+",1)",
                pointStrokeColor : "#fff",
                data : s_channel[channelId]['data'][0]
            },
            {
                fillColor : "rgba("+downSpiderColor+",0.5)",
                strokeColor : "rgba("+downSpiderColor+",1)",
                pointColor : "rgba("+downSpiderColor+",1)",
                pointStrokeColor : "#fff",
                data : s_channel[channelId]['data'][1]
            },
            {
                fillColor : "rgba("+playManualColor+",0.5)",
                strokeColor : "rgba("+playManualColor+",1)",
                pointColor : "rgba("+playManualColor+",1)",
                pointStrokeColor : "#fff",
                data : s_channel[channelId]['data'][2]
            },
            {
                fillColor : "rgba("+playSpiderColor+",0.5)",
                strokeColor : "rgba("+playSpiderColor+",1)",
                pointColor : "rgba("+playSpiderColor+",1)",
                pointStrokeColor : "#fff",
                data : s_channel[channelId]['data'][3]
            }
        ]
        };
        var myNewChart = new Chart(ctx).Line(data);
    };


    // 显示合计下载播放数据

    var ctx = $('#myChart')[0].getContext("2d");
    var data = {
    labels : labels,
    datasets : [
        {
                fillColor : "rgba("+downManualColor+",0.5)",
                strokeColor : "rgba("+downManualColor+",1)",
                pointColor : "rgba("+downManualColor+",1)",
                pointStrokeColor : "#fff",
                data : s_sum[0]
            },
            {
                fillColor : "rgba("+downSpiderColor+",0.5)",
                strokeColor : "rgba("+downSpiderColor+",1)",
                pointColor : "rgba("+downSpiderColor+",1)",
                pointStrokeColor : "#fff",
                data : s_sum[1]
            },
            {
                fillColor : "rgba("+playManualColor+",0.5)",
                strokeColor : "rgba("+playManualColor+",1)",
                pointColor : "rgba("+playManualColor+",1)",
                pointStrokeColor : "#fff",
                data : s_sum[2]
            },
            {
                fillColor : "rgba("+playSpiderColor+",0.5)",
                strokeColor : "rgba("+playSpiderColor+",1)",
                pointColor : "rgba("+playSpiderColor+",1)",
                pointStrokeColor : "#fff",
                data : s_sum[3]
            }
    ]
    };
    var myNewChart = new Chart(ctx).Line(data);

    // 显示 合计
    var ctx = $('#createStatistics')[0].getContext("2d");
    var data = {
    labels : labels,
    datasets : [
        {
                fillColor : "rgba("+downManualColor+",0.5)",
                strokeColor : "rgba("+downManualColor+",1)",
                data : s_create_sum[0]
            },
            {
                fillColor : "rgba("+playManualColor+",0.5)",
                strokeColor : "rgba("+playManualColor+",1)",
                data : s_create_sum[1]
            }
    ]
    };
    var myNewChart = new Chart(ctx).Bar(data);
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