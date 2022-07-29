var fv;
var input_birthdate;
var date_current;
var select_breed;
var select_typepet;

document.addEventListener('DOMContentLoaded', function (e) {
    const form = document.getElementById('frmForm');
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
            },
            fields: {
                name: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                    }
                },
                observation: {
                    validators: {
                        // notEmpty: {},
                    }
                },
                typepet: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un tipo de animal'
                        },
                    }
                },
                breed: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione una raza'
                        },
                    }
                },
                color: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un color'
                        },
                    }
                },
                gender: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un genero'
                        },
                    }
                },
                image: {
                    validators: {
                        file: {
                            extension: 'jpeg,jpg,png',
                            type: 'image/jpeg,image/png',
                            maxFiles: 1,
                            message: 'Introduce una imagen válida'
                        }
                    }
                },
                birthdate: {
                    validators: {
                        notEmpty: {
                            message: 'La fecha es obligatoria'
                        },
                        date: {
                            format: 'YYYY-MM-DD',
                            message: 'La fecha no es válida'
                        }
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
            submit_formdata_with_ajax_form(fv);
        });
});

$(function () {

    date_current = new moment().format("YYYY-MM-DD");
    input_birthdate = $('input[name="birthdate"]');
    select_typepet = $('select[name="typepet"]');
    select_breed = $('select[name="breed"]');

    input_birthdate.datetimepicker({
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
        defaultDate: date_current,
        maxDate: date_current
    });

    input_birthdate.on('change.datetimepicker', function (e) {
        fv.revalidateField('birthdate');
    });

    $('input[name="name"]').keypress(function (e) {
        return validate_form_text('letters', e, null);
    });

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    select_typepet.on('change', function () {
        fv.revalidateField('typepet');
        $.ajax({
            url: pathname,
            data: {
                'action': 'search_breed',
                'typepet': $(this).val(),
            },
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            dataType: 'json',
            success: function (request) {
                if (!request.hasOwnProperty('error')) {
                    select_breed.html('').select2({
                        data: request,
                        theme: 'bootstrap4',
                        language: "es"
                    });
                    select_breed.trigger('change');
                    return false;
                }
                message_error(request.error);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                message_error(errorThrown + ' ' + textStatus);
            },
            complete: function () {

            }
        });
    });

    select_breed.on('change', function () {
        fv.revalidateField('breed');
    });

    $('select[name="gender"]').on('change.select2', function () {
        fv.revalidateField('gender');
    });

    $('select[name="color"]').on('change.select2', function () {
        fv.revalidateField('color');
    });
});
