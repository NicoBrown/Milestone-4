document.addEventListener('DOMContentLoaded', async () => {
var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);

const stripe = Stripe(stripePublicKey, {
    apiVersion: '2020-08-27',
});

var elements = stripe.elements();

var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
var card = elements.create('card', {
    style: style
});
card.mount('#card-element');

// Handle realtime validation errors on the card element
card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// When the form is submitted...
const form = document.getElementById('payment-form');
let submitted = false;
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Disable double submission of the form
    if (submitted) {
        return;
    }
    submitted = true;
    form.querySelector('button').disabled = true;

    // Make a call to the server to create a new
    // payment intent and store its client_secret.
    stripe.createToken('bank_account', {
            country: 'GB',
            currency: 'gbp',
            sort_code: form.querySelector('input[name=sort_code]').value,
            account_number: form.querySelector('input[name=account_number]').value,
            account_holder_name: form.querySelector('input[name=account_holder_name]').value,
            account_holder_type: form.querySelector('selector[name = account_holder_type]').value,
        })
        .then(function (result) {
            response = result.json()

            print(response)

            if (backendError) {
                addMessage(backendError.message);

                // reenable the form.
                submitted = false;
                form.querySelector('button').disabled = false;
                return;
            }
        })
});

// Duplicated below from page -------------------------------------------
var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);

const stripe = Stripe(stripePublicKey, {
    apiVersion: '2020-08-27',
});

const options = {
    clientSecret: 'client_secret',
    // Fully customizable with appearance API.
};

// Set up Stripe.js and Elements to use in checkout form, passing the client secret obtained in step 3
const elements = stripe.elements(options);

var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};

// Create and mount the Payment Element
const paymentElement = elements.create('payment');
paymentElement.mount('#payment-element');

// var card = elements.create('iban', {
//     style: style
// });
// card.mount('#ideal-bank-element');


// // Create and mount the Payment Element
// const paymentElement = elements.create('payment');
// paymentElement.mount('#payment-element');

card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
                    <span class="icon" role="alert">
                        <i class="fas fa-times"></i>
                    </span>
                    <span>${event.error.message}</span>
                    `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// When the form is submitted...
const form = document.getElementById('payment-form');
let submitted = false;
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Disable double submission of the form
    if (submitted) {
        return;
    }
    submitted = true;
    form.querySelector('button').disabled = true;

    // Make a call to the server to create a new
    // payment intent and store its client_secret.
    stripe.createToken('card', {
            country: 'GB',
            currency: 'gbp',
            sort_code: form.querySelector('input[name=sort_code]').value,
            account_number: form.querySelector('input[name=account_number]')
                .value,
            account_holder_name: form.querySelector(
                'input[name=account_holder_name]').value,
            account_holder_type: form.querySelector(
                'selector[name = account_holder_type]').value,
        })
        .then(function (result) {
            response = result.json()

            print(response)

            if (backendError) {
                addMessage(backendError.message);

                // reenable the form.
                submitted = false;
                form.querySelector('button').disabled = false;
                return;
            }
        })
});
});


});