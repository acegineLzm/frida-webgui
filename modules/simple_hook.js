setTimeout(function(){
    Java.perform(function () {
        var hookClass1 = Java.use("");
        hookClass.aaa.overload("java.lang.String").implementation = function (s) {
            send(s.toString());
            return this.aaa(s);
        };

        var hookClass2 = Java.use("");
        hookClass2.bbb.implementation = function (s) {
            send(s.toString());
            return this.bbb(s);
        };
    });
},0);