// payment.js

async function processPayment(clientSecret) {
    const stripe = Stripe('your_stripe_public_key');

    const result = await stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: await stripe.createToken('card', {
                number: '4242424242424242',
                exp_month: '12',
                exp_year: '2030',
                cvc: '123',
            }),
        },
    });

    if (result.error) {
        // Error handling
        console.error(result.error.message);
    } else {
        // Payment succeeded
        window.location.href = '/success/';
    }
}
