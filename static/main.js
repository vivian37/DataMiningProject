let currentDate;

function getCurrDateStr() {
    let dateStr;
    let dd = String(currentDate.getDate()).padStart(2, '0');
    let mm = String(currentDate.getMonth() + 1).padStart(2, '0'); //January is 0!
    let yyyy = currentDate.getFullYear();

    dateStr = yyyy + '/' + mm + '/' + dd;
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
    $('#dateConfirmBtn').click(function () {
        currentDate = $currDatePicker.datepicker('getDate');
        $('#currDate').text(getCurrDateStr());
    });

    $('#dateModal').on('hidden.bs.modal', function () {

        $currDatePicker.datepicker('update', getCurrDateStr());
    });
});