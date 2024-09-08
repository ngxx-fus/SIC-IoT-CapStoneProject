const firebaseConfig = {
    apiKey: "AIzaSyD5pqDw2o4AyjiARrFEP8nBwG4g2kmRStQ",
    authDomain: "nhan-3660d.firebaseapp.com",
    databaseURL: "https://nhan-3660d-default-rtdb.firebaseio.com",
    projectId: "nhan-3660d",
    storageBucket: "nhan-3660d.appspot.com",
    messagingSenderId: "1054276103106",
    appId: "1:1054276103106:web:428ec651a347fa0b39045b",
    measurementId: "G-27TGW7MZDB"
  };
  firebase.initializeApp(firebaseConfig);

var fireStatus = "OFF";
var smokeStatus = "OFF";

function checkFireAndSmokeStatus() {
    const alarmSound = document.getElementById('alarmSound');

    if (fireStatus === "ON" || smokeStatus === "ON") {
        if (alarmSound.paused) {
            alarmSound.play();
        }
    } else {
        alarmSound.pause();
        alarmSound.currentTime = 0;
    }
}

firebase.database().ref("/LivingRoom/smoke").on("value", function(snapshot) {
    var smk = snapshot.val();
    var smokeStatusElem = document.getElementById("smoke_node1");
    var smokeNode1 = document.getElementById("smoke_node1_id");

    if (smk === "ON") {
        smokeStatusElem.innerHTML = "DETECTED";
        smokeStatusElem.style.color = "red";
        smokeNode1.classList.add("zooming2");
        smokeStatus = "ON";
    } else {
        smokeStatusElem.innerHTML = "NOT DETECTED";
        smokeStatusElem.style.color = "black";
        smokeNode1.classList.remove("zooming2");
        smokeStatus = "OFF";
    }

    console.log("khói: " + smk);
    checkFireAndSmokeStatus();
});

firebase.database().ref("/LivingRoom/fire").on("value", function(snapshot) {
    var fire = snapshot.val();
    var fireStatusElem = document.getElementById("fire_node1");
    var fireNode1 = document.getElementById("firesensor_node1_id");

    if (fire === "ON") {
        fireStatusElem.innerHTML = "DETECTED";
        fireStatusElem.style.color = "red";
        fireNode1.classList.add("zooming1");
        fireStatus = "ON";  
    } else {
        fireStatusElem.innerHTML = "NOT DETECTED";
        fireStatusElem.style.color = "black";
        fireNode1.classList.remove("zooming1");
        fireStatus = "OFF";

    console.log("lửa: " + fire);
    checkFireAndSmokeStatus();
  }
});

const alarmSound = document.getElementById('alarmSound');

firebase.database().ref("/LivingRoom/fireAlarm").on("value", function(snapshot) {
    if (snapshot.exists()) {
        const fireAlarmStatus = snapshot.val();
        
        if (fireAlarmStatus === "ON" && (fireStatus === "ON" || smokeStatus === "ON")) {
            if (alarmSound.paused) {
                alarmSound.play().catch(error => console.error('Error playing sound:', error));
            }
        } else {
            alarmSound.pause();
            alarmSound.currentTime = 0;
        }
    }
});