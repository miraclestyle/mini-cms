CKEDITOR.dialog.add("file_manager", function (c) {
    var e = function (f) {
        var f = new Object();
        f.code = "";
        return f
    };
 
    return {
        title: 'File Manager Form',
        minWidth: 835,
        minHeight: 450,
        resizable : CKEDITOR.DIALOG_RESIZE_BOTH,
        onShow: function () {
            var i = this.getParentEditor();
            var h = i.getSelection();
            var g = h.getStartElement();
            var k = g && g.getAscendant("span", true);
            var j = "";
            var f = null;
            if (k) {
                code = k.getHtml();
                f = new Object();
                f.code = code
            } else {
                f = e()
            }
            this.setupContent(f)
        },
        onOk: function () {
            var h = this.getParentEditor();
            var g = h.getSelection();
            var f = g.getStartElement();
            var k = f && f.getAscendant("span", true);
            var i = e();
            this.commitContent(i);
            if (k) {
                k.setHtml(i.code)
            } else {
                var l = new CKEDITOR.dom.element("span");
                l.setHtml(Elvin.filemanager.ckeditorHandle());
                h.insertElement(l)
            }
        },
        contents: [{
            id: "source",
            label: 'Managment',
            accessKey: "S",
            elements: [{
                type: "hbox",
                children: [
                {
                type: "html",
                html: '<div align="center">'+Elvin.filemanager.open({'size': 0, 'array' : false, 'ckeditor' : true, 'custom' : ' '})+'</div>' 
             }]
        }]
    }]
}});