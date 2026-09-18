// Coding Challenge 130.3: Drawing with Fourier Transform and Epicycles
// Daniel Shiffman
// https://thecodingtrain.com/CodingChallenges/130.1-fourier-transform-drawing.html
// https://thecodingtrain.com/CodingChallenges/130.2-fourier-transform-drawing.html
// https://thecodingtrain.com/CodingChallenges/130.3-fourier-transform-drawing.html
// https://youtu.be/7_vKzcgpfvU


let x = [];
let fourierX;
let time = 0;
let path = [];
let completedpath = [];
let isdrawingComplete = flase // savoir si le dessin est fin pret 

function setup() {
  createCanvas(800, 600);
  const skip = 8;
  //constante qui fais varier le nb de cercle et donc le nb de moteur
  for (let i = 0; i < drawing.length; i += skip) {
    const c = new Complex(drawing[i].x, drawing[i].y);
    x.push(c);
  }
  fourierX = dft(x);
  fourierX.sort((a, b) => b.amp - a.amp);
}

function epicycles(x, y, rotation, fourier) 
//const maxcercles =50 
//const nbcercles = min(maxcercles , fourier.length) et changer ds la boucle fourier.length par nbcercle
{
  for (let i = 0; i < fourier.length; i++) {
    let prevx = x;
    let prevy = y;
    let freq = fourier[i].freq;
    let radius = fourier[i].amp;
    let phase = fourier[i].phase;
    x += radius * cos(freq * time + phase + rotation);
    y += radius * sin(freq * time + phase + rotation);

    stroke(255, 100);
    noFill();
    ellipse(prevx, prevy, radius * 2);
    stroke(255);
    line(prevx, prevy, x, y);
  }
  return createVector(x, y);
}

function draw() {
  background(0);

  if (!isDrawingComplete){
    let v = epicycles(width / 2, height / 2, 0, fourierX);
    path.unshift(v);
  }

  beginShape();
  noFill();
  for (let i = 0; i < path.length; i++) {
    vertex(path[i].x, path[i].y);
  }
  endShape();

  const dt = TWO_PI / fourierX.length;
  time += dt;

  if (time > TWO_PI) {
    if (isDrawingComplete){
      completedpath = [...path];
      isDrawingComplete = True;

      console.log("Dessin terminé ! Nombre de points enregistrés :",completedPath.length);
    }
  }
}


