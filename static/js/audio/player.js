// Possible improvements:
// - Change timeline and volume slider into input sliders, reskinned
// - Change into Vue or React component
// - Be able to grab a custom title instead of "Music Song"
// - Hover over sliders to see preview of timestamp/volume change

const qaries = {
    "Abdurrahmaan_As-Sudais_192kbps": "আব্দুর রহমান আস সুদাইস",
    "Abdullaah_3awwaad_Al-Juhaynee_128kbps": "আব্দুল্লাহ আওয়াদ আল জুহাইনী",
    "Alafasy_128kbps": "মিশরী আল আফাসী",
    "Hudhaify_128kbps": "হুদাইফী",
    "MaherAlMuaiqly128kbps": "মাহের আল মুয়াইকলী",
    "Nasser_Alqatami_128kbps": "নাসের আল কাতামী",
    "Yasser_Ad-Dussary_128kbps": "ইয়াসের আদ দুসারী"
}

var qari = localStorage.getItem('qari');
$("#qari-name").text(qaries[qari]);

function makeThreeDigit(number) {
    if (number < 10) {
        return "00" + number;
    } else if (number < 100) {
        return "0" + number;
    } else {
        return number;
    }    
}

function convertToBanglaDigits(number) {
    const banglaDigits = {
      0: '০',
      1: '১',
      2: '২',
      3: '৩',
      4: '৪',
      5: '৫',
      6: '৬',
      7: '৭',
      8: '৮',
      9: '৯'
    };
  
    const englishDigits = number.toString().split('');
    let banglaNumber = '';
  
    for (let i = 0; i < englishDigits.length; i++) {
      if (banglaDigits.hasOwnProperty(englishDigits[i])) {
        banglaNumber += banglaDigits[englishDigits[i]];
      } else {
        banglaNumber += englishDigits[i];
      }
    }
  
    return banglaNumber;
  }

const audioPlayer = document.querySelector(".audio-player");
const audio = new Audio(`https://everyayah.com/data/${qari}/${makeThreeDigit(sid)}001.mp3`);
audio.sura_name = undefined;
audio.sura = sid;
audio.aya = 1;

let volume = localStorage.getItem("volume");
if (volume != null && volume.includes("muted")){
    audio.muted = true;
    audio.volume = parseFloat(volume.split("-")[1]);
    audioPlayer.querySelector(".controls .volume-percentage").style.width = parseFloat(volume.split("-")[1]) * 100 + '%';
    audioPlayer.querySelector(".volume-container .volume").classList.remove("icono-volumeHigh");
    audioPlayer.querySelector(".volume-container .volume").classList.add("icono-volumeMute");
} else {
  audioPlayer.querySelector(".volume-container .volume").classList.add("icono-volumeHigh");
  audioPlayer.querySelector(".volume-container .volume").classList.remove("icono-volumeMute");
  if (volume === null){
    localStorage.setItem("volume", 0.5);
    audio.volume = 0.5;
    audioPlayer.querySelector(".controls .volume-percentage").style.width = 0.5 * 100 + '%';
    audio.muted = false;
  } else {
    audio.volume = parseFloat(volume);
    audioPlayer.querySelector(".controls .volume-percentage").style.width = volume * 100 + '%';
    audio.muted = false;
  }
}

audio.addEventListener(
  "loadeddata",
  () => {
    audioPlayer.querySelector(".time .length").textContent = convertToBanglaDigits(getTimeCodeFromNum(
      audio.duration
    ));
    let volume = localStorage.getItem("volume");
    if (volume != null && volume.includes("muted")){
        audio.muted = true;
        audio.volume = parseFloat(volume.split("-")[1]);
        audioPlayer.querySelector(".volume-container .volume").classList.remove("icono-volumeHigh");
        audioPlayer.querySelector(".volume-container .volume").classList.add("icono-volumeMute");
    } else {
      audioPlayer.querySelector(".volume-container .volume").classList.add("icono-volumeHigh");
      audioPlayer.querySelector(".volume-container .volume").classList.remove("icono-volumeMute");
      if (volume === null){
        localStorage.setItem("volume", 0.5);
        audio.volume = 0.5;
        audio.muted = false;
      } else {
        audio.volume = volume;
        audio.muted = false;
      }
    }
  },
  false
);

//click on timeline to skip around
const timeline = audioPlayer.querySelector(".timeline");
timeline.addEventListener("click", e => {
  const timelineWidth = window.getComputedStyle(timeline).width;
  const timeToSeek = e.offsetX / parseInt(timelineWidth) * audio.duration;
  audio.currentTime = timeToSeek;
}, false);

//click volume slider to change volume
const volumeSlider = audioPlayer.querySelector(".controls .volume-slider");
volumeSlider.addEventListener('click', e => {
  const sliderWidth = window.getComputedStyle(volumeSlider).width;
  const newVolume = e.offsetX / parseInt(sliderWidth);
  audio.volume = newVolume;
  audio.muted = false;
  audioPlayer.querySelector(".volume-container .volume").classList.add("icono-volumeHigh");
  audioPlayer.querySelector(".volume-container .volume").classList.remove("icono-volumeMute");
  localStorage.setItem("volume", newVolume);
  audioPlayer.querySelector(".controls .volume-percentage").style.width = newVolume * 100 + '%';
}, false)


let intervalId; // declare the variable to store the interval ID

function startInterval() {
  intervalId = setInterval(() => {
    const progressBar = audioPlayer.querySelector(".progress");
    progressBar.style.width = audio.currentTime / audio.duration * 100 + "%";
    audioPlayer.querySelector(".time .current").textContent = (convertToBanglaDigits(getTimeCodeFromNum(audio.currentTime)));
    if (audio.currentTime / audio.duration * 100 == 100){
      const pBtn = audioPlayer.querySelector(".controls .toggle-play");
      pBtn.classList.remove("pause");
      pBtn.classList.add("play");
    }
  }, 1);
}

function stopInterval(){
  clearInterval(intervalId);
}

function playNext() {
  if (document.getElementById("auto-next").checked && audio.aya < tv) {
    play(audio.sura_name, audio.sura, parseInt(audio.aya)+1);
  } else {
    stopInterval();
  }
}

function playPrevious() {
  if (audio.aya > 1) {
    play(audio.sura_name, audio.sura, parseInt(audio.aya)-1);
  }
}

audio.addEventListener('play', startInterval);
audio.addEventListener('ended', playNext);

const playBtn = audioPlayer.querySelector(".controls .toggle-play");
playBtn.addEventListener(
  "click",
  () => {
    if (audio.paused) {
      playBtn.classList.remove("play");
      playBtn.classList.add("pause");
      audio.play();
    } else {
      playBtn.classList.remove("pause");
      playBtn.classList.add("play");
      audio.pause();
    }
  },
  false
);

audioPlayer.querySelector(".volume-button").addEventListener("click", () => {
  const volumeEl = audioPlayer.querySelector(".volume-container .volume");
  audio.muted = !audio.muted;
  if (audio.muted) {
    let volume = localStorage.getItem("volume").split("-");
    if (volume.length === 1){
      volume = volume[0];
    } else {
      volume = volume[1];
    }
    audio.muted = true;
    localStorage.setItem("volume", `muted-${volume}`);
    volumeEl.classList.remove("icono-volumeHigh");
    volumeEl.classList.add("icono-volumeMute");
  } else {
    let volume = localStorage.getItem("volume").split("-");
    if (volume.length === 1){
      volume = volume[0];
    } else {
      volume = volume[1];
    }
    audio.muted = false;
    localStorage.setItem("volume", `${volume}`)
    volumeEl.classList.add("icono-volumeHigh");
    volumeEl.classList.remove("icono-volumeMute");
  }
});

//turn 128 seconds into 2:08
function getTimeCodeFromNum(num) {
  let seconds = parseInt(num);
  let minutes = parseInt(seconds / 60);
  seconds -= minutes * 60;
  const hours = parseInt(minutes / 60);
  minutes -= hours * 60;

  if (hours === 0) return `${minutes}:${String(seconds % 60).padStart(2, 0)}`;
  return `${String(hours).padStart(2, 0)}:${minutes}:${String(
    seconds % 60
  ).padStart(2, 0)}`;
}

function play(sura_name=undefined, sura, aya) {
    if (audio) {
        audio.pause(); // Pause any existing audio
    }
    var qari = localStorage.getItem('qari');
    var audioSrc = `https://everyayah.com/data/${qari}/${makeThreeDigit(sura)}${makeThreeDigit(aya)}.mp3`;
    audio.src = audioSrc;
    audio.load(); // reloads the audio element with the new source
    playBtn.classList.remove("play");
    playBtn.classList.add("pause");
    if (sura_name != undefined){
      $("#sura-name").text(sura_name);
    }
    $("#referance").text(`(${convertToBanglaDigits(sura)}:${convertToBanglaDigits(aya)})`)
    $("#qari-name").text(qaries[qari]);
    audioPlayer.querySelector(".progress").style.width = "0%";
    if (aya === tv){
      $("#next-aya").removeClass("cursor-pointer").addClass("cursor-not-allowed");
    } else {
      $("#next-aya").addClass("cursor-pointer").removeClass("cursor-not-allowed");
    }
    if (aya === 1){
      $("#previous-aya").removeClass("cursor-pointer").addClass("cursor-not-allowed");
    } else {
      $("#previous-aya").addClass("cursor-pointer").removeClass("cursor-not-allowed");
    }
    audio.play();
    audio.sura_name = sura_name;
    audio.sura = sura;
    audio.aya = aya;
}

$("#previous-aya").click(function(){
  playPrevious();
})

$("#next-aya").click(function(){
  playNext();
})

function pronunsiation(sid, a, b, c){
    if (audio) {
        audio.pause();
        playBtn.classList.add("play");
        playBtn.classList.remove("pause");
    }
    var pronunsiation_audio = new Audio(`https://words.audios.quranwbw.com/${sid}/${a}_${b}_${c}.mp3`);
    pronunsiation_audio.play();
}