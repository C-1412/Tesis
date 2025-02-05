$(function () {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "question"},
            {"data": "comp"},
            {"data": "score"},
            {"data": "score2"},
        ],
        initComplete: function (settings, json) {

        }
    });
});
