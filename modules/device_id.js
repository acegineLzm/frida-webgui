setTimeout(function(){
        Java.perform(function () {
            var TM = Java.use("android.telephony.TelephonyManager");
            TM.getDeviceId.implementation = function () {
                send("Called - deviceID() , returning 007");
                return "007";
            };
        });
},0);