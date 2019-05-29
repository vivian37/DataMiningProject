let currData1 = [];
let currData2 = [];
let currStockId1 = 'Stock';
let currStockId2 = 'Stock';

let myChart;
let upColor = '#ec0000';
let upBorderColor = '#8A0000';
let downColor = '#00da3c';
let downBorderColor = '#008F28';
let stockList = [];
$(document).ready(function () {

    let dom = document.getElementById("chartArea");
    myChart = echarts.init(dom);

    $.ajax({
        url: '/data/stockList',
        success: function (d) {
            stockList = d;
        }
    });
    $('#showBtn').click(function () {
        let stock_id = $('#stockIdInput').val();
        let limit = $('#itemLimitInput').val();

        if (stockList.indexOf(stock_id) !== -1) {
            currStockId1 = stock_id;
            $('#stockIdDisp').val(stock_id);
            $.ajax({
                url: '/data/stock/similar/' + stock_id,
                data: {
                    limit: limit
                },
                success: function (d) {
                    updateTable(d);
                }
            })
        } else {
            alert('Stock ' + stock_id + ' not in database!');
        }
    });

    var options = {
        selectors: {
            addButtonSelector: '.btn-add',
            subtractButtonSelector: '.btn-subtract',
            inputSelector: '.counter',
        },
        settings: {
            checkValue: true,
            isReadOnly: true,
        },
    };

    $(".input-counter").inputCounter(options);


});

function updateTable(data) {
    let buttonHTML = '<button class="btn btn-warning stockBtn" data-toggle="modal" data-target="#drawModal">Detail</button>';
    $("#tbl > tbody").html('<tr><th scope="row">1</th><td>' + data[0][0] + '</td><td>' + data[0][1].toFixed(2) + '</td><td>' + buttonHTML + '</td></tr>');
    for (let i = 1; i < data.length; ++i) {
        $('#tbl tr:last').after('<tr><th scope="row">' + (i + 1) + '</th><td>' + data[i][0] + '</td><td>' + data[i][1].toFixed(2) + '</td><td>' + buttonHTML + '</td></tr>');
    }
    $('.stockBtn').click(function () {
        currStockId2 = $(this).parent().parent().children()[1].textContent;
        $.ajax({
            url: '/data/stock/day/' + currStockId1,
            success: function (d) {
                currData1 = splitData(d);
                $.ajax({
                    url: '/data/stock/day/' + currStockId2,
                    success: function (d) {
                        currData2 = splitData(d);
                        draw();
                    }
                });
            }
        });

    });

}

function splitData(rawData) {
    var categoryData = [];
    var values = [];
    for (var i = 0; i < rawData.length; i++) {
        categoryData.push(rawData[i].splice(0, 1)[0]);
        values.push(rawData[i])
    }
    return {
        categoryData: categoryData,
        values: values
    };
}

function calculateMA(dayCount, which) {
    let currData;
    if (which === 1) {
        currData = currData1;
    } else {
        currData = currData2;
    }
    var result = [];
    for (var i = 0, len = currData.values.length; i < len; i++) {
        if (i < dayCount) {
            result.push('-');
            continue;
        }
        var sum = 0;
        for (var j = 0; j < dayCount; j++) {
            sum += currData.values[i - j][1];
        }
        result.push(sum / dayCount);
    }
    return result;
}

function unique(array) {
    var res = [];
    var sortedArray = array.concat().sort();
    var seen;
    for (var i = 0, len = sortedArray.length; i < len; i++) {
        // 如果是第一个元素或者相邻的元素不相同
        if (!i || seen !== sortedArray[i]) {
            res.push(sortedArray[i])
        }
        seen = sortedArray[i];
    }
    return res.concat().sort();
}

function draw() {
    option = {
        title: {
            text: '',
            left: 0
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross'
            }
        },
        legend: {
            data: ['日K - ' + currStockId1, '日K - ' + currStockId2, 'MA10 - ' + currStockId1, 'MA10 - ' + currStockId2]
        },
        grid: {
            left: '10%',
            right: '10%',
            bottom: '15%'
        },
        xAxis: {
            type: 'category',
            data: unique(currData1.categoryData.concat(currData2.categoryData)),
            scale: true,
            boundaryGap: false,
            axisLine: {onZero: false},
            splitLine: {show: false},
            splitNumber: 20,
            min: 'dataMin',
            max: 'dataMax'
        },
        yAxis: {
            scale: true,
            splitArea: {
                show: true
            }
        },
        dataZoom: [
            {
                type: 'inside',
                start: 0,
                end: 100
            },
            {
                show: true,
                type: 'slider',
                y: '90%',
                start: 0,
                end: 100
            }
        ],
        series: [
            {
                name: '日K - ' + currStockId1,
                type: 'candlestick',
                data: currData1.values,
                itemStyle: {
                    normal: {
                        color: upColor,
                        color0: downColor,
                        borderColor: upBorderColor,
                        borderColor0: downBorderColor
                    }
                }
            },
            {
                name: '日K - ' + currStockId2,
                type: 'candlestick',
                data: currData2.values,
                itemStyle: {
                    normal: {
                        color: upColor,
                        color0: downColor,
                        borderColor: upBorderColor,
                        borderColor0: downBorderColor
                    }
                }
            },
            {
                name: 'MA10 - ' + currStockId1,
                type: 'line',
                data: calculateMA(10, 1),
                smooth: true,
                lineStyle: {
                    normal: {opacity: 0.5}
                }
            },
            {
                name: 'MA10 - ' + currStockId2,
                type: 'line',
                data: calculateMA(10, 2),
                smooth: true,
                lineStyle: {
                    normal: {opacity: 0.5}
                }
            }


        ]
    };

    if (option && typeof option === "object") {
        myChart.setOption(option, true);
    }
}