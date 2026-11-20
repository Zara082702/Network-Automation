
document.addEventListener("DOMContentLoaded", function () {

    const forms = document.querySelectorAll(".command-form");

    forms.forEach(function (form) {

        form.addEventListener("submit", function () {

            const button = form.querySelector("button");
            const originalText = button.innerHTML;

            button.disabled = true;

            button.innerHTML = `
                <i class="fas fa-spinner fa-spin"></i>
                <span>
                    <strong>Executing Command...</strong>
                    <small>Please wait for router response</small>
                </span>
            `;

            // Re-enable the button after a short delay.
            // The page will normally reload when the response arrives.
            setTimeout(function () {
                button.disabled = false;
                button.innerHTML = originalText;
            }, 30000);

        });

    });

});
