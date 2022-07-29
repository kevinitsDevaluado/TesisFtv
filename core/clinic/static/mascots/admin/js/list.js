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
                'client': $('select[name="client"]').val()
            },
            dataSrc: ""
        },
        columns: [
            {data: "pos"},
            {data: "name"},
            {data: "client.user.full_name"},
            {data: "image"},
            {data: "observation"},
            {data: "id"},
        ],
        columnDefs: [
            {
                targets: [-3],
                class: 'text-center',
                render: function (data, type, row) {
                    return '<img src="' + data + '" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;">';
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                render: function (data, type, row) {
                    var buttons = '<a href="/clinic/mascots/admin/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit" aria-hidden="true"></i></a> ';
                    buttons += '<a href="/clinic/mascots/admin/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash" aria-hidden="true"></i></a>';
                    return buttons;
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

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    $('select[name="client"]').on('change', function () {
        getData();
    });

    getData();

});