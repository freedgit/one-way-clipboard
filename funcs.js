var counterino = 0;

const sleep = (milliseconds) => {
  return new Promise(resolve => setTimeout(resolve, milliseconds))
}

function reqListener () {
    var jsonString = this.responseText;
    var obj = jQuery.parseJSON(jsonString);
    
    if (obj.type == "url") {
        window.open(obj.content, '_blank');
    } else if (obj.type == "content") {
        document.getElementById("textarea").innerHTML = obj.content;
        localStorage.setItem("clipboard", obj.content);
    }
}

function copy_to_clipboard() {
    var content = document.getElementById("textarea").innerHTML;
    navigator.clipboard.writeText(content);
}

function copy_to_remote_clipboard() {
    var form = document.getElementById("submit_form");
    form.submit();
}


function load_defaults() {
    content = localStorage.getItem("clipboard");
    if (content == null) {
        content = "";
    }
    textarea = document.getElementById("textarea");
    textarea.innerHTML = content;
}

function sub_load_request() {
    var xr = new XMLHttpRequest();
    var other_port = window.location.origin;
    xr.addEventListener("load", reqListener)
    xr.open("GET", other_port);
    xr.send();
}

async function load_request() {
    WAITING_FOR = 5 * 1000;
    
    while (true) {
        await sleep(WAITING_FOR);
        sub_load_request();
    }
}

function load_request_old() {
    var loop = 1;

    MAX_STUFF = 7;
    WAITING_FOR = 5 * 1000;

    while (true) {
        if (loop > MAX_STUFF) {
            break;
        }

        loop++;
        
        setTimeout(function() {
            var xr = new XMLHttpRequest();
            var other_port = window.location.origin;
            xr.addEventListener("load", reqListener)
            xr.open("GET", other_port);
            xr.send();

            counterino++;
            
            if (counterino == MAX_STUFF) {
                window.location = window.location;
            }
        }, WAITING_FOR * loop);
    }
}
