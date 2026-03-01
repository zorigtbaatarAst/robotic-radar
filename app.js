const socket = io("http://localhost:5000");

const canvas = document.getElementById("radar");
const ctx = canvas.getContext("2d");

let distance = -1;
let angle = 0;

const maxDistance = 100;
const radius = canvas.width / 2;

socket.on("radar_update", data => {
  distance = data.distance;
  angle = data.angle * Math.PI / 180;
});

function drawRadarGrid() {

  ctx.strokeStyle = "rgba(0,255,0,.3)";
  ctx.lineWidth = 1;

  for (let r = 100; r <= radius; r += 100) {
    ctx.beginPath();
    ctx.arc(0, 0, r, 0, Math.PI * 2);
    ctx.stroke();
  }

  for (let i = 0; i < 360; i += 45) {
    let x = Math.cos(i * Math.PI / 180) * radius;
    let y = Math.sin(i * Math.PI / 180) * radius;
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(x, y);
    ctx.stroke();
  }
}

function draw() {

  ctx.fillStyle = "rgba(0,0,0,.25)";
  ctx.fillRect(0,0,canvas.width,canvas.height);

  ctx.save();
  ctx.translate(radius, radius);

  drawRadarGrid();

  // Sweep line
  ctx.strokeStyle = "#00ff00";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(0,0);
  ctx.lineTo(Math.cos(angle)*radius, Math.sin(angle)*radius);
  ctx.stroke();

  // Detected object
  if(distance > 0){

    let d = distance / maxDistance * radius;
    let x = Math.cos(angle)*d;
    let y = Math.sin(angle)*d;

    ctx.fillStyle="rgba(0,255,0,.9)";
    ctx.beginPath();
    ctx.arc(x,y,8,0,Math.PI*2);
    ctx.fill();
  }

  ctx.restore();

  document.getElementById("dist").innerHTML =
    distance>0 ? `Distance: ${distance} cm` : "No object";

  requestAnimationFrame(draw);
}

draw();