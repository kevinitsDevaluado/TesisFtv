var input_datejoined;
var input_hour;
var current_date;
var select_employee;
var select_mascot;
var fv;
var tblQuotes;
var medical_appointment = {};

document.addEventListener('DOMContentLoaded', function (e) {
    const form = document.getElementById('frmDateMedical');
    fv = FormValidation.formValidation(form, {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
                // excluded: new FormValidation.plugins.Excluded(),
            },
            fields: {
                date_joined: {
                    validators: {
                        notEmpty: {
                            message: 'La fecha es obligatoria'
                        },
                        date: {
                            format: 'YYYY-MM-DD',
                            message: 'La fecha no es válida'
                        }
                    },
                },
                hour: {
                    validators: {
                        notEmpty: {
                            message: 'Debe seleccionar una hora'
                        },
                        regexp: {
                            regexp: /^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$/,
                            message: 'El formato de la hora no es el correcto'
                        },
                    },
                },
                symptoms: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                    }
                },
                employee: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un médico'
                        },
                    }
                },
                mascot: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione una mascota'
                        },
                    }
                },
            },
        }
    )
        .on('core.element.validated', function (e) {
            if (e.valid) {
                const groupEle = FormValidation.utils.closest(e.element, '.form-group');
                if (groupEle) {
                    FormValidation.utils.classSet(groupEle, {
                        'has-success': false,
                    });
                }
                FormValidation.utils.classSet(e.element, {
                    'is-valid': false,
                });
            }
            const iconPlugin = fv.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            var parameters = {};
            $.each($(fv.form).serializeArray(), function (key, item) {
                parameters[item.name] = item.value;
            });
            parameters['hour'] = input_hour.val();
            submit_with_ajax('Alerta', '¿Estas seguro de agendar la siguiente cita?', pathname, parameters, function (request) {
                alert_sweetalert('success', 'Notificación', request.msg, function () {
                    location.href = fv.form.getAttribute('data-url');
                }, 3000, null);
            });
        });
});

$(function () {

    input_datejoined = $('input[name="date_joined"]');
    input_hour = $('input[name="hour"]');
    current_date = new moment().format("YYYY-MM-DD");
    select_employee = $('select[name="employee"]');
    select_mascot = $('select[name="mascot"]');

    input_datejoined.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
        date: current_date,
        minDate: current_date,
    });

    input_datejoined.on('change.datetimepicker', function (e) {
        fv.revalidateField('date_joined');
        input_hour.val('');
        medical_appointment = {};
    });

    $('.select2').select2({
        theme: 'bootstrap4',
        language: 'es'
    });

    select_employee.on('change.select2', function () {
        fv.revalidateField('employee');
        input_hour.val('');
        if (!$.isEmptyObject(medical_appointment)) {
            var cells = tblQuotes.cells().nodes();
            $(cells).find('input[type="checkbox"][name="schedule"]').prop('checked', false);
            medical_appointment = {};
        }
    });

    select_mascot.on('change.select2', function () {
        fv.revalidateField('mascot');
    });

    input_datejoined.datetimepicker('date', input_datejoined.val());

    $('.btnScheduling').on('click', function () {
        $('#datecite').html(input_datejoined.val());

        var parameters = {
            'action': 'search_quotes',
            'employee': select_employee.val(),
            'date_joined': input_datejoined.val()
        };

        if ($.isEmptyObject(parameters.employee)) {
            alert_sweetalert('info', 'Notificación', 'Debe seleccionar un doctor para ver el horario disponible', function () {

            }, 1500, null);
            return false;
        }

        $('.doctor').html('<b>Mecánico: </b> ' + $('select[name="employee"] option:selected').text());

        tblQuotes = $('#tblQuotes').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: parameters,
                dataSrc: ""
            },
            // paging: false,
            // ordering: false,
            info: false,
            columns: [
                {data: "hour"},
                {data: "status"},
                {data: "status"},
            ],
            columnDefs: [
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var html = '';
                        switch (row.status) {
                            case 'vacant':
                                html = '<span class="badge badge-success">Libre</span>';
                                break;
                            case 'reserved':
                                html = '<span class="badge badge-warning">Ocupado</span>';
                                break;
                            case 'time_not_available':
                                html = '<span class="badge badge-danger">No disponible</span>';
                                break;
                        }
                        return html;
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.status === 'vacant') {
                            return '<input type="checkbox" name="schedule">';
                        }
                        return '<i class="fas fa-calendar-check"></i>';
                    }
                }
            ],
            rowCallback: function (row, data, index) {
                var tr = $(row).closest('tr');
                if (medical_appointment !== null) {
                    if (data.pos === parseInt(medical_appointment.pos)) {
                        tr.find('input[name="schedule"]').prop('checked', 'checked');
                    }
                }
                /*switch (data.status) {
                    case 'vacant':
                        break;
                    case 'reserved':
                        $(tr).css({'background': '#a57c1a', 'color': 'white'});
                        break;
                    case 'time_not_available':
                        $(tr).css({'background': '#0681b1', 'color': 'white'});
                        break;
                }*/
            },
            initComplete: function (settings, json) {

            }
        });
        $('#myModalScheduling').modal('show');
    });

    $('#tblQuotes tbody')
        .on('change', 'input[name="schedule"]', function () {
            var tr = tblQuotes.cell($(this).closest('td, li')).index();
            var row = tblQuotes.row(tr.row).data();
            var cells = tblQuotes.cells().nodes();
            $(cells).find('input[type="checkbox"][name="schedule"]').prop('checked', false);
            $.each(data = tblQuotes.rows().data(), function (key, value) {
                value.state = false;
            });
            $(this).prop('checked', true);
            row.state = this.checked;
            row.pos = tr.row;
            input_hour.val(row.hour);
            medical_appointment = row;
            fv.revalidateField('hour');
        });

    $('.btnCurriculum').on('click', function () {
        if (select_employee.val() === '') {
            message_error('Debe seleccionar un médico')
            return false;
        }

        $.ajax({
            url: pathname,
            data: {
                'action': 'search_employee',
                'id': select_employee.val()
            },
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            dataType: 'json',
            success: function (request) {
                if (!request.hasOwnProperty('error')) {
                    if (!$.isEmptyObject(request.curriculum)) {
                        window.open(request.curriculum);
                        return false;
                    }
                    message_error('No tiene hoja de vida');
                    return false;
                }
                message_error(request.error);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                message_error(errorThrown + ' ' + textStatus);
            }
        });
    });

    input_hour.val('');
});