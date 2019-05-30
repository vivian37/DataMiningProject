let currentDate;

function getCurrDateStr() {
    let dateStr;
    let dd = String(currentDate.getDate()).padStart(2, '0');
    let mm = String(currentDate.getMonth() + 1).padStart(2, '0'); //January is 0!
    let yyyy = currentDate.getFullYear();

    dateStr = yyyy + '/' + mm + '/' + dd;
    return dateStr;
}

function getNewsDateStr() {
    let dateStr;
    let dd = String(currentDate.getDate()).padStart(2, '0');
    let mm = String(currentDate.getMonth() + 1).padStart(2, '0'); //January is 0!
    let yyyy = currentDate.getFullYear();

    dateStr = yyyy + '' + mm + '' + dd;
    return dateStr;
}

$(document).ready(function () {
    $('.datepicker').datepicker({
        format: 'yyyy/mm/dd',
        startDate: '2016/01/01',
        endDate: '2016/12/31',
        defaultViewDate: '2016/01/01'
    });
    $currDatePicker = $('#currDatePicker');
    $currDatePicker.datepicker('update', '2016/01/01');
    currentDate = $currDatePicker.datepicker('getDate');
    $('#currDate').text(getCurrDateStr());
    updateNewsBlock(getNewsDateStr());
    $('#dateConfirmBtn').click(function () {
        currentDate = $currDatePicker.datepicker('getDate');
        $('#currDate').text(getCurrDateStr());
        updateNewsBlock(getNewsDateStr());
    });

    $('#dateModal').on('hidden.bs.modal', function () {

        $currDatePicker.datepicker('update', getCurrDateStr());
    });

});

function updateNewsBlock(dateStr) {
    $.ajax({
        url: '/data/news/' + dateStr,
        success: function (d) {
            updateNewsTable(d);
        }
    })
}


function updateNewsTable(data) {
    $table = $('#newsTable');
    $('#newsCount').text(data.length);
    if (data.length === 0) {
        $("#newsTable > tbody").html('<tr><td>Nothing to show</td></tr>');
    } else {
        $("#newsTable > tbody").html('<tr><td><a href="' + data[0]['link'] + '">' + data[0]['title'] + '</a></td><td>' + data[0]['matches'][0][0] + ' ' + data[0]['matches'][0][1] + '</td></tr>');
        for (let i = 1; i < data.length; ++i) {
            $('#newsTable tr:last').after('<tr><td><a href="' + data[i]['link'] + '">' + data[i]['title'] + '</a></td><td>' + data[i]['matches'][0][0] + ' ' + data[i]['matches'][0][1] + '</td></tr>');
        }
    }

}