CKEDITOR.plugins.add("file_manager", {
    requires: ["dialog"],
    lang: ["en"],
    init: function (a) {
        var b = "file_manager";
        var c = a.addCommand(b, new CKEDITOR.dialogCommand(b));
        c.modes = {
            wysiwyg: 1,
            source: 1
        };
        c.canUndo = false;
        a.ui.addButton("Fmanager", {
            label: 'File manager',
            command: b,
            icon: this.path + "jezz.png"
        });
        CKEDITOR.dialog.add(b, this.path + "dialogs/file_manager.js")
    }
});