let currData = [];
let currStockId = 'Stock';
let myChart;
let upColor = '#ec0000';
let upBorderColor = '#8A0000';
let downColor = '#00da3c';
let downBorderColor = '#008F28';
let stockList = [];
$(document).ready(function () {
    let dom = document.getElementById("ec-container");
    myChart = echarts.init(dom);
    $.ajax({
        url: '/data/stockList',
        success: function (d) {
            stockList = d;

        }
    });
    $('#showBtn').click(function () {
        let stock_id = $('#stockIdInput').val();
        if (stockList.indexOf(stock_id) !== -1) {
            $.ajax({
                url: '/data/stock/detail/' + stock_id,
                success: function (d) {
                    currData = d;
                    currStockId = stock_id;
                    draw();
                }
            })
        } else {
            alert('Stock ' + stock_id + ' not in database!');
        }
    });
    draw();
});


function draw() {
    var option = {
        dataset: {
            source: currData
        },
        title: {
            text: currStockId
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'line'
            }
        },
        toolbox: {
            feature: {
                dataZoom: {
                    yAxisIndex: false
                },
            }
        },
        grid: [
            {
                left: '10%',
                right: '10%',
                bottom: 200
            },
            {
                left: '10%',
                right: '10%',
                height: 80,
                bottom: 80
            }
        ],
        xAxis: [
            {
                type: 'category',
                scale: true,
                boundaryGap: false,
                // inverse: true,
                axisLine: {onZero: false},
                splitLine: {show: false},
                splitNumber: 20,
                min: 'dataMin',
                max: 'dataMax'
            },
            {
                type: 'category',
                gridIndex: 1,
                scale: true,
                boundaryGap: false,
                axisLine: {onZero: false},
                axisTick: {show: false},
                splitLine: {show: false},
                axisLabel: {show: false},
                splitNumber: 20,
                min: 'dataMin',
                max: 'dataMax'
            }
        ],
        yAxis: [
            {
                scale: true,
                splitArea: {
                    show: true
                }
            },
            {
                scale: true,
                gridIndex: 1,
                splitNumber: 2,
                axisLabel: {show: false},
                axisLine: {show: false},
                axisTick: {show: false},
                splitLine: {show: false}
            }
        ],
        dataZoom: [
            {
                type: 'inside',
                xAxisIndex: [0, 1],
                start: 10,
                end: 100
            },
            {
                show: true,
                xAxisIndex: [0, 1],
                type: 'slider',
                bottom: 10,
                start: 10,
                end: 100,
                handleIcon: 'M10.7,11.9H9.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4h1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
                handleSize: '105%'
            }
        ],
        visualMap: {
            show: false,
            seriesIndex: 1,
            dimension: 6,
            pieces: [{
                value: 1,
                color: upColor
            }, {
                value: -1,
                color: downColor
            }]
        },
        series: [
            {
                type: 'candlestick',
                itemStyle: {
                    color: upColor,
                    color0: downColor,
                    borderColor: upBorderColor,
                    borderColor0: downBorderColor
                },
                encode: {
                    x: 0,
                    y: [1, 4, 3, 2]
                }
            },
            {
                name: 'Volumn',
                type: 'bar',
                xAxisIndex: 1,
                yAxisIndex: 1,
                itemStyle: {
                    color: '#7fbe9e'
                },
                large: true,
                encode: {
                    x: 0,
                    y: 5
                }
            }
        ]
    };

    if (option && typeof option === "object") {
        myChart.setOption(option, true);
    }
}