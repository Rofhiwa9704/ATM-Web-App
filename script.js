const API = "http://127.0.0.1:5000";

function login() {
    const pin = document.getElementById("pin").value;

    fetch(API + "/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ pin })
    })
    .then(res => {
        if (res.status === 200) {
            document.getElementById("menu").style.display = "block";
            document.getElementById("output").innerText = "Login successful";
        } else {
            document.getElementById("output").innerText = "Wrong PIN";
        }
    });
}

function checkBalance() {
    fetch(API + "/balance")
    .then(res => res.json())
    .then(data => {
        document.getElementById("output").innerText =
            "Balance: R" + data.balance;
    });
}

function deposit() {
    const amount = document.getElementById("amount").value;

    fetch(API + "/deposit", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ amount })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("output").innerText = data.message;
    });
}

function withdraw() {
    const amount = document.getElementById("amount").value;

    fetch(API + "/withdraw", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ amount })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("output").innerText = data.message;
    });
}