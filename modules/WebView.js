setTimeout(function(){
    Java.perform(function () {

        var WebView = Java.use("android.webkit.WebView");

        WebView.loadUrl.overload("java.lang.String").implementation = function (s) {

            send(s.toString());

            this.loadUrl(s);

        };

    });

},0);