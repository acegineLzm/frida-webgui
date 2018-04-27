Interceptor.attach(Module.findExportByName("libc.so" , "open"), {
    onEnter: function(args) {
        args[1] = ptr(0);
        send(Memory.readCString(args[0])+","+args[1]);

        // arg2 = Memory.readUtf8String(args[1]);

        // var buf = Memory.readByteArray(args[1], 64);
        // console.log(hexdump(buf, {
        //   offset: 0,
        //   length: 64,
        //   header: true,
        //   ansi: true
        // }));
    },
    onLeave:function(retval){

	} 
});
