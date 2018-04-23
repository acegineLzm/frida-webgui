setTimeout(function(){
    Java.perform(function () {

        var TM = Java.use("com.jni.anto.kalip.MainActivity");

        TM.isPhoneRooted.implementation = function () {

            send("Called - isPhoneRooted()");

            return false;

        };

    });

},0);