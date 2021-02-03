// Read uploaded file
$('#file').on('change', function (e) {
  var reader = new FileReader();
  reader.onload = function (e) {
    $("#preview").attr('src', e.target.result);
  }
  reader.readAsDataURL(e.target.files[0]);
  document.getElementById("image").style.display = "none";
});

// Footer Fixed
new function(){

  var footerId = "site-footer";
  function footerFixed() {
    var dh = document.getElementsByTagName("body")[0].clientHeight;
    document.getElementById(footerId).style.top = "0px";
    var ft = document.getElementById(footerId).offsetTop;
    var fh = document.getElementById(footerId).offsetHeight;
    if (window.innerHeight) {
      var wh = window.innerHeight;
    } else if (document.documentElement && document.documentElement.clientHeight != 0) {
      var wh = document.documentElement.clientHeight;
    }
    if (ft+fh<wh) {
      document.getElementById(footerId).style.position = "relative";
      document.getElementById(footerId).style.top = (wh-fh-ft)+"px";
    }
  }

  function checkFontSize(func){
    var e = document.createElement("div");
    var s = document.createTextNode("S");
    e.appendChild(s);
    e.style.visibility="hidden"
    e.style.position="absolute"
    e.style.top="0"
    document.body.appendChild(e);
    var defHeight = e.offsetHeight;

    function checkBoxSize(){
      if(defHeight != e.offsetHeight){
      func();
      defHeight= e.offsetHeight;
      }
    }
    setInterval(checkBoxSize,1000)
  }

  function addEvent(elm,listener,fn){
    try{
      elm.addEventListener(listener,fn,false);
    }catch(e){
      elm.attachEvent("on"+listener,fn);
    }
  }

  addEvent(window,"load",footerFixed);
  addEvent(window,"load",function(){
    checkFontSize(footerFixed);
  });
  addEvent(window,"resize",footerFixed);

}

// Modal
new function() {
  const open_borrow = document.getElementById('open-borrow');
  const open_return = document.getElementById('open-return');
  const close_borrow = document.getElementById('close-borrow');
  const close_return = document.getElementById('close-return');
  const modal_borrow = document.getElementById('modal-borrow');
  const modal_return = document.getElementById('modal-return');
  const mask_borrow = document.getElementById('mask-borrow');
  const mask_return = document.getElementById('mask-return');

  // function for borrow
  if (open_borrow) {
    open_borrow.addEventListener('click', function () {
      modal_borrow.classList.remove('hidden');
      mask_borrow.classList.remove('hidden');
    });
    close_borrow.addEventListener('click', function () {
      modal_borrow.classList.add('hidden');
      mask_borrow.classList.add('hidden');
    });
    mask_borrow.addEventListener('click', function () {
      modal_borrow.classList.add('hidden');
      mask_borrow.classList.add('hidden');
    });
  }

  // function for return
  if (open_return) {
    open_return.addEventListener('click', function () {
      modal_return.classList.remove('hidden');
      mask_return.classList.remove('hidden');
    });
    close_return.addEventListener('click', function () {
      modal_return.classList.add('hidden');
      mask_return.classList.add('hidden');
    });
    mask_return.addEventListener('click', function () {
      modal_return.classList.add('hidden');
      mask_return.classList.add('hidden');
    });
  }
}