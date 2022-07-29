var select_type_medicalhistory;
var select_mascot;

function getData() {
    var parameters = {
        'action': 'search',
        'mascot': select_mascot.val(),
        'type': select_type_medicalhistory.val(),
    };

    $.ajax({
        url: pathname,
        data: parameters,
        type: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        dataType: 'json',
        success: function (request) {
            if (!request.hasOwnProperty('error')) {
                var html = '';
                $.each(request, function (key, item) {
                    html += '<div class="time-label">';
                    html += '<span class="bg-green">' + item.date_joined + '</span>';
                    html += '</div>';

                    html += '<div>';
                    switch (item.type.id) {
                        case 'control_antiparasitario':
                            html += '<i class="fas fa-first-aid bg-blue"></i>';
                            break;
                        case 'control_vacuna':
                            html += '<i class="fas fa-syringe bg-success"></i>';
                            break;
                        case 'cita_medica':
                            html += '<i class="fas fa-user-md bg-warning"></i>';
                            break;
                    }
                    html += '<div class="timeline-item">';
                    html += '<span class="time"><i class="fas fa-clock"></i> ' + item.hour + '</span>';
                    html += '<h3 class="timeline-header"><a><i class="fas fa-file-medical-alt"></i> Revisión </a></h3>';
                    html += '<div class="timeline-body">';

                    html += '<dl class="row">';
                    html += '<dt class="col-sm-2">Automóvil:</dt><dd class="col-sm-10">' + item.mascot.name + '</dd>';
                    html += '<dt class="col-sm-2">Mecánico:</dt><dd class="col-sm-10">' + item.employee.user.full_name + '</dd>';
                    html += '<dt class="col-sm-2">Observación:</dt><dd class="col-sm-10">' + item.observation + '</dd>';
                    if (item.type.id === 'cita_medica') {
                        html += '<dt class="col-sm-2">Motivo:</dt><dd class="col-sm-10">' + item.symptoms + '</dd>';
                        html += '<dt class="col-sm-2">Diagnóstico:</dt><dd class="col-sm-10">' + item.diagnosis + '</dd>';
                    }
                    html += '</dl>';

                    html += '</tbody></table></div>';
                    html += '</div></div></div></div>';
                });

                $('.timeline').html(html);

                return false;
            }
            message_error(request.error);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            message_error(errorThrown + ' ' + textStatus);
        }
    });
}

$(function () {

    select_type_medicalhistory = $('select[name="type_medicalhistory"]');
    select_mascot = $('select[name="mascots"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
        sorter: function (data) {
            return data.sort(function (a, b) {
                return a.text < b.text ? -1 : a.text > b.text ? 1 : 0;
            });
        }
    });

    select_type_medicalhistory.on('change', function () {
        getData();
    });

    select_mascot
        .on('change', function () {
            getData();
        });

    getData();

});