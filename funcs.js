var counterino = 0;

const sleep = (milliseconds) => {
  return new Promise(resolve => setTimeout(resolve, milliseconds))
}

function reqListener () {
    var jsonString = this.responseText;
    var obj = jQuery.parseJSON(jsonString);
    
    console.log(obj);
    
    if (obj.type == "url") {
        window.open(obj.content, '_blank');
    } else if (obj.type == "content") {
        document.getElementById("textarea").innerHTML = obj.content;
        localStorage.setItem("clipboard", obj.content);
    }
    
    console.log(obj.type);
    console.log(obj.content);
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
    document.getElementById("textarea").innerHTML = content;
}

function sub_load_request() {
    var xr = new XMLHttpRequest();
    var other_port = window.location.origin + ":9999";
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
            var other_port = window.location.origin + ":9999";
            xr.addEventListener("load", reqListener)
            xr.open("GET", other_port);
            xr.send();

            counterino++;
            
            console.log(xr);
            console.log(counterino);

            if (counterino == MAX_STUFF) {
                console.log("I was supposed to reload");
                window.location = window.location;
                // window.location.reload();
            }
        }, WAITING_FOR * loop);
    }

    console.log("getting out of the loop");
}

load_defaults();

load_request();
