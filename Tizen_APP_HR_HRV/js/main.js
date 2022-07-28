
window.onload = function () {
    // TODO:: Do your initialization job
	
	tizen.power.request("CPU", "CPU_AWAKE");

    // add eventListener for tizenhwkey
    document.addEventListener('tizenhwkey', function(e) {
        if(e.keyName == "back")
	try {
	    tizen.application.getCurrentApplication().exit();
	} catch (ignore) {
	}
    });
    

    function onSuccess() {
    	
       
    	

        function onchangedCB(hrmInfo) {
        	        	

                      
            var pData = {
                    rate: hrmInfo.heartRate,
                    rrinterval: hrmInfo.rRInterval
                    
                    };
            
            var  HR = pData.rate;
            var HRV = pData.rrinterval;
            var time = new Date().getTime();
            var sw = 'sw1';
            
            
           // var msg_hrm = HR + ',' + HRV;
            var msg_hrm =  JSON.stringify({"type": "hrm", "hr": HR, "hrv" : HRV , "timestamp" : (time + 7200)/1000, "sw": sw }); 
            
            //tizen.power.request("CPU", "CPU_AWAKE");
            sendMessage(msg_hrm); 
            console.log(webSocket.readyState);
            console.log(msg_hrm);
            
            
 

        }
        
        function onerrorCB(error) {
            console.log('Error occurred. Name:' + error.name + ', message: ' + error.message);
        }
    
      
        // INIZIA IL BLOCCO DEL WEBSOCKET
        // per vittoria: 192.168.10.102
        var webSocketUrl = 'ws://192.168.10.74:8088'; // THIS HAS TO BE CHANGED WITH THE IP OF THE PC WHERE THE PYTHON SCRIPT RUNS
        var webSocket = new WebSocket(webSocketUrl); 
        
        webSocket.onopen = function(e) {
    	console.log('OK!, readyState: ' + e.target.readyState);
    	   	};

    	webSocket.onerror = function(e) {
    		 console.log('Error!, readyState: ' + e.target.readyState);
    	};
        
    	webSocket.onclose = function(e) {
    		 console.log('Websocket closed, readyState: ' + e.target.readyState); 
    	    };
        
        console.log(webSocket.readyState);

                  
            
       function sendMessage(msg) {
                if (webSocket.readyState === 1) {
                    webSocket.send(msg);
                }
            }
        

       var myCallbackInterval = 1000;
       var mySampleInterval = 1000;
       
       var option = {
    		   
       	    'callbackInterval': myCallbackInterval,
       	    'sampleInterval': mySampleInterval
       	};
       	
        tizen.humanactivitymonitor.start('HRM',  onchangedCB, onerrorCB, option);
        //linearAccelerationSensor.start(onchangedCB);
        
    }
    
    
   
    function onError(e) {
        console.log("error" + JSON.stringify(e));
    }
    
    tizen.ppm.requestPermission("http://tizen.org/privilege/healthinfo",onSuccess, onError);
    
    // Sample code
    var textbox = document.querySelector('.contents');
    textbox.addEventListener("click", function(){
    	box = document.querySelector('#textbox');
    	box.innerHTML = box.innerHTML == "Collecting HR data.." ? "Collecting HR & HRV" : "Collecting HR data..";
    });
    
    
    
};
