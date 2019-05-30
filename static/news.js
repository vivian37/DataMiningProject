$(document).ready(function () {
    $('#newsTable').bootstrapTable({
        url: '/analysis/news',
        columns: [{
            field: 'title',
            title: 'News',
        }, {
            field: 'stock',
            title: 'Stock'
        }, {
            field: 'emotion',
            title: 'Emotion'
        }],

    })
});