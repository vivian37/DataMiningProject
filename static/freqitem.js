let data;
let info = {
    'Reason': [],
    'Result': []
};
$(document).ready(function () {
    $.ajax({
        url: '/data/frequent_items',
        success: function (d) {
            updateFreqItemTable(d);
            data = d;
        }

    })
});


function buttonHandler(type) {
    if (type === 'Reason') {

    } else if (type === 'Result') {


    } else {
        return null;
    }

    var handler = function (e) {
        let $this = $(e.target);
        let index = parseInt($this.parent().parent().children()[0].textContent);
        let displayText = data[index - 1][0] + ' ' + data[index - 1][1];
        if ($this.prop('selected') !== '1') {
            $this.text($this.text().replace('Add', 'Added'));
            $this.prop('selected', '1');
            $this.removeClass('btn-info');
            $this.addClass("btn-warning");
            info[type].push(index);
        } else {
            $this.text($this.text().replace('Added', 'Add'));
            $this.prop('selected', '0');
            $this.removeClass('btn-warning');
            $this.addClass("btn-info");
            info[type].splice(info[type].indexOf(index), 1);
        }
        if (info['Reason'].length > 0 && info['Result'].length > 0) {
            $.ajax({
                type: 'POST',
                url: '/data/rules',
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                data: JSON.stringify({
                    reasons: info['Reason'],
                    results: info['Result']
                }),
                success: function (d) {
                    let confidence = d[0].toFixed(3);
                    let interest = d[1].toFixed(3);
                    $('#confidence').text(confidence);
                    $('#interest').text(interest);
                }
            });
        }
    };
    return handler;
}

function updateFreqItemTable(data) {
    let btnText = '<td><button class="btn btn-info addReason">Add as Reason</button></td><td><button class="btn btn-info addResult">Add as Cause</button></td>';
    $("#freqItemTable > tbody").html('<tr><td>' + data[0][2] + '</td><td>' + data[0][0] + '</td><td>' + data[0][1] + '</td>' + btnText + '</tr>');
    for (let i = 1; i < data.length; ++i) {
        $('#freqItemTable tr:last').after('<tr><td>' + data[i][2] + '</td><td>' + data[i][0] + '</td><td>' + data[i][1] + '</td>' + btnText + '</tr>');
    }
    $('button.addReason').click(buttonHandler('Reason'));
    $('button.addResult').click(buttonHandler('Result'));

}