setTimeout(function(){
        Java.perform(function () {

            var TM = Java.use("com.jni.anto.kalip.MainActivity");

            TM.encrypt.implementation = function(a,b) {

                send("Called - encrypt()"+a.toString()+"yaa"+b.toString());
                this.encrypt.call(this,a,b);

            };

        });

    },0);