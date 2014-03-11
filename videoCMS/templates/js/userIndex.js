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

    var manualColor = '238,123,0';
    var spiderColor = '56,119,189';



    // 显示新增 合计
    var ctx = $('#createStatistics')[0].getContext("2d");
    var data = {
        labels : labels,
        datasets : [
            {
                fillColor : "rgba("+manualColor+",0.5)",
                strokeColor : "rgba("+manualColor+",1)",
                data : s_create_sum[0]
            },
            {
                fillColor : "rgba("+spiderColor+",0.5)",
                strokeColor : "rgba("+spiderColor+",1)",
                data : s_create_sum[1]
            }
        ]
    };
    var myNewChart = new Chart(ctx).Bar(data);

    // 显示合计播放数据
    var ctx = $('#playStatistics')[0].getContext("2d");
    var data = {
        labels : labels,
        datasets : [
            {
                fillColor : "rgba("+manualColor+",0.5)",
                strokeColor : "rgba("+manualColor+",1)",
                pointColor : "rgba("+manualColor+",1)",
                pointStrokeColor : "#fff",
                data : s_sum[2]
            },
            {
                fillColor : "rgba("+spiderColor+",0.5)",
                strokeColor : "rgba("+spiderColor+",1)",
                pointColor : "rgba("+spiderColor+",1)",
                pointStrokeColor : "#fff",
                data : s_sum[3]
            }
        ]
    };
    var myNewChart = new Chart(ctx).Bar(data);

    // 显示合计下载数据
    var ctx = $('#downStatistics')[0].getContext("2d");
    var data = {
        labels : labels,
        datasets : [
            {
                fillColor : "rgba("+manualColor+",0.5)",
                strokeColor : "rgba("+manualColor+",1)",
                pointColor : "rgba("+manualColor+",1)",
                pointStrokeColor : "#fff",
                data : s_sum[0]
            },
            {
                fillColor : "rgba("+spiderColor+",0.5)",
                strokeColor : "rgba("+spiderColor+",1)",
                pointColor : "rgba("+spiderColor+",1)",
                pointStrokeColor : "#fff",
                data : s_sum[1]
            }
        ]
    };
    var myNewChart = new Chart(ctx).Bar(data);

    //显示频道
    for(var i=0;i<channelList.length ; i++)
    {
        var channelId = channelList[i].channelId;
        var dom = $('.'+channelId);

        var ctx = dom.next().find('.channelStatistic')[0].getContext("2d");


        var data = {
            labels : labels,
            datasets : [
                {
                    fillColor : "rgba("+manualColor+",0.5)",
                    strokeColor : "rgba("+manualColor+",1)",
                    pointColor : "rgba("+manualColor+",1)",
                    pointStrokeColor : "#fff",
                    data : channelList[i]['data'][0]
                },
                {
                    fillColor : "rgba("+manualColor+",0.5)",
                    strokeColor : "rgba("+manualColor+",1)",
                    pointColor : "rgba("+manualColor+",1)",
                    pointStrokeColor : "#fff",
                    data : channelList[i]['data'][1]
                },
                {
                    fillColor : "rgba("+manualColor+",0.5)",
                    strokeColor : "rgba("+manualColor+",1)",
                    pointColor : "rgba("+manualColor+",1)",
                    pointStrokeColor : "#fff",
                    data : channelList[i]['data'][2]
                },
                {
                    fillColor : "rgba("+manualColor+",0.5)",
                    strokeColor : "rgba("+manualColor+",1)",
                    pointColor : "rgba("+manualColor+",1)",
                    pointStrokeColor : "#fff",
                    data : channelList[i]['data'][3]
                }
            ]
        };
        var myNewChart = new Chart(ctx).Bar(data);
    };

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