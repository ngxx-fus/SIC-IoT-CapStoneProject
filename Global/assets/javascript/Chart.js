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

var nhietdo = [];
var doamkk = [];
var khigas = [];
var previousNhietDo = null;
var previousDoAmKK = null;
var previousKhiGas = null;
var updateInterval = null;

const initialLabels = ['Initial'];
//-----------------CREATE CHARTS-----------------------------
const tempchart = new Chart(temperatureChartCanvas, {
  type: 'line',
  data: {
    labels: initialLabels,
    datasets: [{
      label: 'Temperature',
      data: nhietdo,
      borderColor: 'rgba(255, 99, 132, 1)',
      backgroundColor: 'rgba(255, 99, 132, 0.2)',
      fill: true
    }]
  },
  options: {
    responsive: true,
    scales: {
      x: {
        ticks: {
          font: {
            size: 14
          }
        }
      },
      y: {
        ticks: {
          font: {
            size: 14
          },
          maxTicksLimit: 6,
          stepSize: 20
        }
      }
    }
  }
});

let humichart = new Chart(humidityChartCanvas, {
  type: 'line',
  data: {
    labels: initialLabels,
    datasets: [{
      label: 'Humidity',
      data: doamkk,
      borderColor: 'blue',
      backgroundColor: 'rgba(185, 249, 244, 0.8)',
      fill: true
    }]
  },
  options: {
    responsive: true,
    scales: {
      x: {
        ticks: {
          font: {
            size: 14
          }
        }
      },
      y: {
        ticks: {
          font: {
            size: 14
          },
          maxTicksLimit: 6,
          stepSize: 1
        }
      }
    }
  }
});

// let gaschart = new Chart(gasChartCanvas, {
//   type: 'line',
//   data: {
//     labels: initialLabels,
//     datasets: [{
//       label: 'CO2',
//       data: khigas,
//       borderColor: 'orange',
//       backgroundColor: 'rgba(250, 232, 198, 0.8)',
//       fill: true
//     }]
//   },
//   options: {
//     responsive: true,
//     scales: {
//       x: {
//         ticks: {
//           font: {
//             size: 14
//           }
//         }
//       },
//       y: {
//         ticks: {
//           font: {
//             size: 14
//           },
//           maxTicksLimit: 6,
//           stepSize: 1
//         }
//       }
//     }
//   }
// });

//---------------LOCAL STORAGE------------------
function saveDataToLocalStorage() {
  localStorage.setItem('nhietdo_history', JSON.stringify(nhietdo));
  localStorage.setItem('doamkk_history', JSON.stringify(doamkk));
  localStorage.setItem('khigas_history', JSON.stringify(khigas));
}

function getDataFromLocalStorage() {
  nhietdo = JSON.parse(localStorage.getItem('nhietdo_history')) || [];
  doamkk = JSON.parse(localStorage.getItem('doamkk_history')) || [];
  khigas = JSON.parse(localStorage.getItem('khigas_history')) || [];
}

function updateDataAndSaveToLocalStorage() {
  saveDataToLocalStorage();
}

getDataFromLocalStorage();

//-------------------AUTO LOAD SENSOR-------------------------
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

firebase.database().ref("/LivingRoom/nhietdo").on("value", function(snapshot) {
  var nd = snapshot.val();
  if (nd !== null) {
    if (nhietdo.length > 0 && nhietdo[nhietdo.length - 1].value === nd) {
      console.log("Duplicate data, skipping update.");
      return;
    }
    nhietdo.push({ value: nd, timestamp: new Date().getTime() });
    document.getElementById("nhietdo").innerHTML = nd;
    console.log("nhietdo: " + nd);
    tempchart.data.datasets[0].data = nhietdo.slice(-8).map(item => item.value);
    tempchart.data.labels = generateLabels(nhietdo.slice(-8));
    tempchart.update();
    updateDataAndSaveToLocalStorage();
  }
});

firebase.database().ref("/LivingRoom/doamkk").on("value", function(snapshot) {
  var da = snapshot.val();
  if (da !== null) {
    if (doamkk.length > 0 && doamkk[doamkk.length - 1].value === da) {
      console.log("Duplicate data, skipping update.");
      return;
    }
    doamkk.push({ value: da, timestamp: new Date().getTime() });
    document.getElementById("doamkk").innerHTML = da;
    console.log("doamkk: " + da);
    humichart.data.datasets[0].data = doamkk.slice(-8).map(item => item.value);
    humichart.data.labels = generateLabels(doamkk.slice(-8));
    humichart.update();
    updateDataAndSaveToLocalStorage();
  }
});

firebase.database().ref("/LivingRoom/khigas").on("value", function(snapshot) {
  var gas = snapshot.val();
  if (gas !== null) {
    if (khigas.length > 0 && khigas[khigas.length - 1].value === gas) {
      console.log("Duplicate data, skipping update.");
      return;
    }
    khigas.push({ value: gas, timestamp: new Date().getTime() });
    document.getElementById("khigas").innerHTML = gas;
    console.log("khí gas: " + gas);
    gaschart.data.datasets[0].data = khigas.slice(-8).map(item => item.value);
    gaschart.data.labels = generateLabels(khigas.slice(-8));
    gaschart.update();
    updateDataAndSaveToLocalStorage();
  }
});

//-----------CREATE TIMESTAMP--------------------
function generateLabels(data) {
  return data.map(item => {
    let time = new Date(item.timestamp);
    return `${time.getHours()}:${time.getMinutes()}:${time.getSeconds()}`;
  });
}

function initializeData() {
  firebase.database().ref("/LivingRoom/nhietdo").once("value", function(snapshot) {
    var nd = snapshot.val();
    if (nd !== null) {
      nhietdo.push({ value: nd, timestamp: new Date().getTime() });
      document.getElementById("nhietdo").innerHTML = nd;
      console.log("Initial nhietdo: " + nd);
      tempchart.data.datasets[0].data = nhietdo.slice(-8).map(item => item.value);
      tempchart.data.labels = generateLabels(nhietdo.slice(-8));
      tempchart.update();
      updateDataAndSaveToLocalStorage();
    }
  });

  firebase.database().ref("/LivingRoom/doamkk").once("value", function(snapshot) {
    var da = snapshot.val();
    if (da !== null) {
      doamkk.push({ value: da, timestamp: new Date().getTime() });
      document.getElementById("doamkk").innerHTML = da;
      console.log("Initial doamkk: " + da);
      humichart.data.datasets[0].data = doamkk.slice(-8).map(item => item.value);
      humichart.data.labels = generateLabels(doamkk.slice(-8));
      humichart.update();
      updateDataAndSaveToLocalStorage();
    }
  });

  firebase.database().ref("/LivingRoom/khigas").once("value", function(snapshot) {
    var gas = snapshot.val();
    if (gas !== null) {
      khigas.push({ value: gas, timestamp: new Date().getTime() });
      document.getElementById("khigas").innerHTML = gas;
      console.log("Initial khigas: " + gas);
      gaschart.data.datasets[0].data = khigas.slice(-8).map(item => item.value);
      gaschart.data.labels = generateLabels(khigas.slice(-8));
      gaschart.update();
      updateDataAndSaveToLocalStorage();
    }
  });
}

initializeData();   