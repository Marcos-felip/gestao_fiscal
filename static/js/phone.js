(function() {
    function initPhoneWidget() {
        if (typeof jQuery === 'undefined' || typeof window.intlTelInput === 'undefined') {
            setTimeout(initPhoneWidget, 50);
            return;
        }

        jQuery(document).ready(function($) {
            const errorMap = [
                "Número inválido",
                "Código de país inválido",
                "Numero incompleto",
                "Numero muito comprido",
                "Número inválido"
            ];

            const reset = (element_name) => {
                $("#error-msg-" + element_name).html("");
                $('#error-msg-' + element_name).prop("hidden", true);
                $('#valid-msg-' + element_name).prop("hidden", true);
            };

            $(".international_phone").each(function() {
                var element_name = $(this).attr("name");
                var input = document.querySelector("#id_" + element_name);
                
                if (!input) return;
                
                var iti = window.intlTelInput(input, {
                    utilsScript: '/static/intl_tel_input/js/utils.js',
                    initialCountry: "br",
                    nationalMode: false,
                    separateDialCode: true,
                    preferredCountries: ['br'],
                });

                input.addEventListener('blur', () => {
                    reset(element_name);
                    if (input.value.trim()) {
                        if (iti.isValidNumber()) {
                            $('#valid-msg-' + element_name).prop("hidden", false);
                        } else {
                            const errorCode = iti.getValidationError();
                            $('#error-msg-' + element_name).html(errorMap[errorCode]);
                            $('#error-msg-' + element_name).prop("hidden", false);
                        }
                    }
                });

                input.addEventListener('change', () => reset(element_name));
                input.addEventListener('keyup', () => reset(element_name));
            });
        });
    }

    // Inicia o processo
    initPhoneWidget();
})();
