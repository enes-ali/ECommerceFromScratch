let number = document.getElementById("CreditCardNumber");


number.addEventListener("keydown", (event) => {
    const max_length = 16;
    if (event.target.value.length >= max_length) {
        event.target.value = event.target.value.slice(0, max_length - 1);
    }
});

