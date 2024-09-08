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

    //-----------------TOAST MESSAGE----------------------
    const toastContainer = document.getElementById('toast2');
    const overlay = document.getElementById('overlay');
    let okClickCount = 0;
    
    function toast({ title = "", message = "", type = "warning", onConfirm, onConfirm2 }) {
        const main = toastContainer;
        if (main) {
            const toast = document.createElement("div");
            toast.style.animation = `slideInDown ease .3s`;
    
            const icons = {
                success: "fas fa-check-circle",
                warning: "fas fa-exclamation-circle",
                info: "fas fa-info-circle",
            };
            const icon = icons[type] || icons.warning;
    
            toast.innerHTML = `
                <div class="toast2 toast2--${type}">
                    <div class="toast2__icon">
                        <i class="${icon}"></i>
                    </div>
                    <div class="toast2__body">
                        <h3 class="toast2__title">${title}</h3>
                        <p class="toast2__msg">${message}</p>
                    </div>
                </div>
                <div class="toast2 toast2--btn">
                    <div class="toast2--btn btn--close">Cancel</div>
                    <div class="toast2--btn btn--next">Ok</div>
                </div>
            `;

        toast.querySelector('.btn--next').onclick = () => {
            okClickCount += 1;

            if (okClickCount === 1) {
                main.removeChild(toast);
                    onConfirm();
            } else if (okClickCount === 2) {
                main.removeChild(toast);
                    onConfirm2();
     
            } else if (okClickCount === 3) {
                main.removeChild(toast);
                overlay.classList.remove('show');
                okClickCount = 0;
                onConfirm2();
            }
        };

        toast.querySelector('.btn--close').onclick = () => {
            main.removeChild(toast);
            okClickCount = 0;
            overlay.classList.remove('show');
        };

        main.appendChild(toast);
        overlay.classList.add('show');
    }
}

let shouldToggleFireAlarm = false;

function closeToast() {
    toast({
        title: "Warning",
        message: "If you enable this rule, you will trigger a fire alarm!",
        type: "warning",
        onConfirm: () => {
            toast({
                title: "Confirmation",
                message: "Are you sure you want to enable warnings?",
                type: "info",
                onConfirm2: () => {
                    toast({
                        title: "Success",
                        message: "Click OK to enable alerts!",
                        type: "success",
                        onConfirm2: () => {
                            console.log("Fire alarm activated!");
                            shouldToggleFireAlarm = true;
                            document.getElementById("fireAlarm").checked = true;
                            firebase.database().ref("/LivingRoom/fireAlarm").set("ON");
                            overlay.classList.remove('show');
                        }
                    });
                }
            });
        }
    });
}

document.getElementById("fireAlarm").addEventListener("change", function(event) {
    const fireAlarmInput = document.getElementById("fireAlarm");
    
    if (shouldToggleFireAlarm) {
        shouldToggleFireAlarm = false;
        firebase.database().ref("/LivingRoom/fireAlarm").set(fireAlarmInput.checked ? "ON" : "OFF");
    } else if (fireAlarmInput.checked) {
        event.preventDefault();
        fireAlarmInput.checked = false;
        closeToast();
    } else {
        firebase.database().ref("/LivingRoom/fireAlarm").set("OFF");
    }
});

var fireStatus = "OFF";
var smokeStatus = "OFF";
var fireAlarmStatus = "OFF";

firebase.database().ref("/LivingRoom/fireAlarm").on("value", function(snapshot) {
    if (snapshot.exists()) {
        fireAlarmStatus = snapshot.val();
        var fireAlarmInput = document.getElementById("fireAlarm");
        var textfireAlarm = document.getElementById("textfireAlarm");
        var fireAlarm = document.getElementById("firealarm");

        if (fireAlarmInput && textfireAlarm) {
            fireAlarmInput.checked = (fireAlarmStatus === "ON");
            textfireAlarm.textContent = fireAlarmStatus;
            textfireAlarm.style.color = (fireAlarmStatus === "ON") ? "red" : "black";
            fireAlarm.style.color = (fireAlarmStatus === "ON") ? "red" : "#6a7076";
        }

        checkFireAndSmokeStatus();
    } else {
        console.log("Không có dữ liệu về fireAlarm!");
    }
});
    
window.addEventListener('load', function() {
firebase.database().ref("/LivingRoom/fireAlarm").once('value').then(function(snapshot) {
  if (snapshot.exists()) {
      fireAlarmStatus = snapshot.val();
      checkFireAndSmokeStatus();
  }
}).catch(error => console.error('Error fetching fireAlarm status:', error));
});

function checkFireAndSmokeStatus() {
    const alarmSound = document.getElementById('alarmSound');

    if (fireAlarmStatus === "ON" && (fireStatus === "ON" || smokeStatus === "ON")) {
        if (alarmSound.paused) {
        alarmSound.play().catch(error => console.error('Error playing sound:', error));
    }
} else {
    alarmSound.pause();
    alarmSound.currentTime = 0;
}
}
firebase.database().ref("/LivingRoom/smoke").on("value", function(snapshot) {
    smokeStatus = snapshot.val();
    var smokeStatusElem = document.getElementById("smoke_node1");
    var smokeNode1 = document.getElementById("smoke_node1_id");

    if (smokeStatus === "ON") {
    smokeStatusElem.innerHTML = "DETECTED";
    smokeStatusElem.style.color = "red";
    smokeNode1.classList.add("zooming2");
} else {
    smokeStatusElem.innerHTML = "NOT DETECTED";
    smokeStatusElem.style.color = "black";
    smokeNode1.classList.remove("zooming2");
}

console.log("khói: " + smokeStatus);
checkFireAndSmokeStatus();
});

firebase.database().ref("/LivingRoom/fire").on("value", function(snapshot) {
fireStatus = snapshot.val();
var fireStatusElem = document.getElementById("fire_node1");
var fireNode1 = document.getElementById("firesensor_node1_id");

if (fireStatus === "ON") {
    fireStatusElem.innerHTML = "DETECTED";
    fireStatusElem.style.color = "red";
    fireNode1.classList.add("zooming1");
} else {
    fireStatusElem.innerHTML = "NOT DETECTED";
    fireStatusElem.style.color = "black";
    fireNode1.classList.remove("zooming1");
}

console.log("lửa: " + fireStatus);
checkFireAndSmokeStatus();
});

  //-------------------AUTO LOAD SENSOR-------------------------
    firebase.database().ref("/LivingRoom/nhietdo").on("value",function(snapshot){
      var nd = snapshot.val();  
      document.getElementById("nhietdo").innerHTML = nd;
      console.log("nhiệt độ: " + nd);
    });
    
    firebase.database().ref("/LivingRoom/doamkk").on("value",function(snapshot){
      var da = snapshot.val();  
      document.getElementById("doamkk").innerHTML = da;
      console.log("độ ẩm: " + da);
    });
  
    firebase.database().ref("/LivingRoom/khigas").on("value",function(snapshot){
      var gas = snapshot.val();  
      document.getElementById("khigas").innerHTML = gas;
      console.log("khí gas: " + gas);
    });


  //----------------CONNECT LIGHT TO FIREBASE-----------------
  firebase.database().ref("/LivingRoom/light").on("value", function(snapshot) {
    if (snapshot.exists()) {
        console.log(snapshot.val());
        var lightStatus = snapshot.val();
        var lightInput = document.getElementById("light");
        var textLight = document.getElementById("textlight");
        var theLight = document.getElementById("thelight");
  
        if (lightInput && textLight && theLight) {
            lightInput.checked = (lightStatus === "ON");
            textLight.textContent = lightStatus;
            textLight.style.color = (lightStatus === "ON") ? "red" : "black";
            theLight.style.color = (lightStatus === "ON") ? "#dbdb0bed" : "#6a7076";
        }
    } else {
        console.log("No data available for light!");
    }
  });
  
  
  //-----------------CONTROL LIGHT FROM THE WEB----------------------
  var lightInput = document.getElementById('light');
  if (lightInput) {
    lightInput.addEventListener('change', function() {
        var lightState = this.checked ? "ON" : "OFF";
        firebase.database().ref("/LivingRoom").update({
            "light": lightState
        });
        var textLight = document.getElementById("textlight");
        if (textLight) {
            textLight.textContent = lightState;
            textLight.style.color = (lightState === "ON") ? "red" : "black";
        }
    });
  }