var tblMascots;

function getData() {
    tblMascots = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: pathname,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: {
                'action': 'search',
            },
            dataSrc: ""
        },
        columns: [
            {data: "pos"},
            {data: "name"},
            {data: "image"},
            {data: "id"},
        ],
        columnDefs: [
            {
                targets: [-2],
                class: 'text-center',
                render: function (data, type, row) {
                    return '<img src="' + data + '" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;">';
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                render: function (data, type, row) {
                    return '<a href="/clinic/mascots/client/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit" aria-hidden="true"></i></a> ';
                    // buttons += '<a href="/clinic/mascots/client/delete/' + row.id + '/" data-toggle="tooltip" title="Eliminar registro" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash" aria-hidden="true"></i></a>';
                }
            },
        ],
        rowCallback: function (row, data, index) {

        },
        initComplete: function (settings, json) {

        }
    });
}

$(function () {
    getData();
});