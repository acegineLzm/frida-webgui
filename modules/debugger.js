setTimeout(function(){
        Java.perform(function () {
            var TM = Java.use("android.os.Debug");
            TM.isDebuggerConnected.implementation = function () {
                send("Called - isDebuggerConnected()");
            return false;
            };
        });
},0);